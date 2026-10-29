# ADR 002 : Validation des entrées de l'API et gestion du cycle de vie du modèle

Date : 28/10/2026 · Auteurs : KENZA ELAIATI, CHAIMAA HADDAD

---

## 1. Décision 1 : Définition des bornes physiques pour la validation des capteurs

### Contexte
L'API MaintAI reçoit des requêtes JSON contenant les relevés de capteurs industriels d'un moteur. Si une valeur aberrante (par exemple une sonde déconnectée renvoyant 500 °C ou -999) est transmise au modèle scikit-learn, les prédictions produites n'ont plus aucune validité physique.
De plus, si l'on se contentait de restreindre les bornes aux valeurs minimum et maximum observées dans le fichier historique `sensors.csv`, une machine saine mais fonctionnant dans des conditions légèrement plus chaudes (ex. canicule) serait indûment rejetée avec une erreur 422.

### Options étudiées
1. **Option A (Bornes calquées sur les données du dataset) :**
   - *Avantages :* Simple à calculer automatiquement.
   - *Inconvénients :* Fragile. Rejette des cas réels légitimes dès qu'un capteur dépasse légèrement l'échantillon historique d'entraînement.
2. **Option B (Bornes physiques basées sur le fonctionnement matériel réel d'un moteur) :**
   - *Avantages :* Robuste. Rejette les erreurs de mesure évidentes (500 °C) tout en autorisant les variations thermiques et mécaniques normales d'un atelier.
   - *Inconvénients :* Nécessite une réflexion sur les limites physiques de fonctionnement.

### Décision
Nous retenons l'**Option B** avec un schéma Pydantic (`SensorReading`) appliquant les bornes suivantes :
- `temperature_c` ($\ge -40\,^\circ\text{C}, \le 150\,^\circ\text{C}$) :
  - *Justification physique :* Une usine peut être située en région froide (démarrage à $-40\,^\circ\text{C}$). Un moteur industriel peut monter en surchauffe jusqu'à $120\text{--}150\,^\circ\text{C}$ avant destruction des isolants. Au-delà de $150\,^\circ\text{C}$, ou en cas de 500 °C, il s'agit d'une sonde rompue ou en court-circuit.
- `vibration_mm_s` ($\ge 0.0\text{ mm/s}, \le 50.0\text{ mm/s}$) :
  - *Justification physique :* Une vitesse de vibration quadratique (RMS) est par définition positive ou nulle ($\ge 0$). Selon la norme ISO 10816, des vibrations au-delà de 20 mm/s indiquent un danger critique, et 50 mm/s correspond à une rupture mécanique immédiate.
- `load_pct` ($\ge 0.0\,\%, \le 120.0\,\%$) :
  - *Justification physique :* La charge ne peut être négative. Les moteurs industriels autorisent une surcharge temporaire (facteur de service typique de 1.15 à 1.20, soit 115 % à 120 %) avant déclenchement thermique.
- `runtime_hours` ($\ge 0.0\text{ h}, \le 100\,000.0\text{ h}$) :
  - *Justification physique :* Un compteur horaire démarre à 0. Une durée de 100 000 heures représente plus de 11 ans de fonctionnement continu 24h/24, ce qui correspond à la durée de vie maximale d'une ligne de production avant remplacement.

### Conséquences
- L'API rejette automatiquement les requêtes corrompues avec un code HTTP **422 Unprocessable Entity** explicite.
- Le modèle n'est jamais sollicité inutilement avec des données absurdes.

---

## 2. Décision 2 : Gestion de l'absence du modèle (Code HTTP 503 vs Refus de démarrage)

### Contexte
Si l'application FastAPI est déployée ou lancée dans un environnement où le modèle `models/model.joblib` n'a pas encore été généré par l'entraînement (`python -m maintai.train`), quelle attitude l'API doit-elle adopter ?

### Options étudiées
1. **Option 1 (Refuser de démarrer en levant une exception au lancement) :**
   - *Avantages :* Évite d'exposer un service qui ne peut pas prédire.
   - *Inconvénients :* Le conteneur ou serveur crashe immédiatement (CrashLoopBackOff). Impossible d'interroger la route `/health` pour diagnostiquer la cause, ni d'accéder à la documentation `/docs`.
2. **Option 2 (Démarrer quand même et renvoyer HTTP 503 Service Unavailable sur `/v1/predict`) :**
   - *Avantages :* Le serveur démarre normalement. L'administrateur peut interroger `GET /health` qui répond avec statut 200 et `{"model_loaded": false}`. La route `/v1/predict` renvoie un code standard 503 avec un message clair indiquant la commande à lancer.
   - *Inconvénients :* Les requêtes de prédiction échouent temporairement tant que le modèle n'a pas été produit.

### Décision
Nous retenons l'**Option 2** :
- Le gestionnaire de contexte `lifespan` intercepte `FileNotFoundError` au démarrage et initialise `state["predictor"] = None`.
- La route `GET /health` permet aux sondes de supervision (Kubernetes, AWS HealthCheck) de constater que le conteneur est vivant mais que le modèle manque.
- Toute requête sur `POST /v1/predict` lève immédiatement une `HTTPException(status_code=503)` :
  `detail="Modèle absent. Entraînez d'abord le modèle avec python -m maintai.train"`.

### Conséquences
- Sécurité et maintenabilité accrues : un ingénieur DevOps comprend instantanément pourquoi la prédiction échoue sans avoir à éplucher les logs de crash du système.
- Conformité totale avec le standard HTTP REST (503 = service temporairement indisponible, 500 réservé aux anomalies logiques non prévues).
