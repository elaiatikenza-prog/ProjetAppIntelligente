# ADR 000 : Choix de l'architecture du modèle de prédiction de panne (MaintAI)

Date : 28/10/2026 · Auteurs : KENZA ELAIATI, CHAIMAA HADDAD

---

## Contexte
L'équipe de maintenance d'une usine doit prioriser chaque matin les machines industrielles à inspecter. Une panne manquée entraîne l'arrêt d'une ligne de fabrication pendant 24 heures (coût très élevé), alors qu'une fausse alerte coûte seulement une heure d'inspection par un technicien.

---

## Options étudiées
1. **Option A (Système expert à base de règles et seuils manuels) :**
   - *Avantages :* Simple à concevoir sans données d'entraînement.
   - *Inconvénients :* Incapable de capturer les interactions croisées entre capteurs (par exemple une température modérée mais combinée à de fortes vibrations et une charge élevée).
2. **Option B (Apprentissage automatique supervisé tabulaire avec pipeline scikit-learn) :**
   - *Avantages :* Modèle probabiliste évaluant le risque global de panne, intégration d'un seuil de décision modulable (0,3) pour maximiser le rappel, reproductibilité avec pipeline et sérialisation standard `.joblib`.
   - *Inconvénients :* Nécessite un jeu de données historiques représentatif et une surveillance continue des dérives.

---

## Décision
Nous retenons l'**Option B** :
- Un pipeline scikit-learn complet associant prétraitement standard et modèle de classification binaire supervisé.
- Un réglage du seuil de décision à **0,3** pour privilégier le **rappel (`recall` $\ge 0,75$)** conformément à la contrainte de coût métier (éviter à tout prix les arrêts de production).
- Une sauvegarde sérialisée dans `models/model.joblib` accompagnée de son contrat d'entrée dans `models/model_info.json`.

---

## Conséquences
- Détection anticipée efficace des pannes avec un rappel mesuré de **0,750** et une précision de **0,622**.
- Le modèle est directement chargeable en mémoire par l'API FastAPI au démarrage (`lifespan`) pour servir des prédictions réseau en temps réel via la route `/v1/predict`.
