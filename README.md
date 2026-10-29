# Développement et Déploiement d'Applications Intelligentes — Séances 3 & 4

**Binôme :**  
- **KENZA ELAIATI**  
- **CHAIMAA HADDAD**  

**Module :** Développement et déploiement d'applications intelligentes  
**Année académique :** 2025 – 2026  

---

## 1. Vue d'ensemble du projet

Ce dépôt contient l'ensemble des travaux pratiques et livrables pour les **Séances 3 et 4** du module :

- **Séance 3 — Projet CantineAI (Prévision des repas scolaires) :**
  - Problème adapté au véritable contenu du CSV (`repas_servis`, `date`, `jour`, `inscrits`, `menu`, `temperature_c`, `pluie_mm`, `examens`, `sortie_scolaire`, `veille_vacances`, `repas_semaine_precedente`) ;
  - Modélisation en **régression** avec métrique principale **MAE (Mean Absolute Error)**, complétée par RMSE et $R^2$ ;
  - Découpage **chronologique** rigoureux (entraînement sur les 80 % passés, test sur les 20 % futurs) sans fuite de données ;
  - Prétraitement automatisé (`ColumnTransformer`) gérant l'imputation des valeurs manquantes et l'encodage One-Hot ;
  - Comparaison expérimentale d'une baseline (`DummyRegressor`) avec 4 modèles de régression (Régression linéaire, Forêt aléatoire, Gradient boosting, k-NN) ;
  - **14 tests automatisés `pytest` réussis** (`14 passed`), étude de conception, plan de tests et rapport de choix de modèle.

- **Séance 4 — Git, HTTP, REST et API FastAPI (MaintAI) :**
  - `TP/TP0` : Rapports d'évaluation MaintAI individuels pour Kenza ELAIATI et Chaimaa HADDAD ;
  - `activite4_demo/` : Démonstration interactive FastAPI avec validation Pydantic (`demo_api.py`) ;
  - `TP/TP1` : API REST de production complète sous FastAPI pour MaintAI (`POST /v1/predict`, `GET /health`, cycle de vie `lifespan`, renvoi HTTP 503 en l'absence de modèle, validation des capteurs par schéma Pydantic avec bornes physiques réelles) ;
  - Décision d'architecture [`docs/adr/002-validation.md`](./S4/TP/TP1/docs/adr/002-validation.md) ;
  - Compte rendu officiel exhaustif [`COMPTE_RENDU.md`](./S4/TP/TP1/COMPTE_RENDU.md) ;
  - **13 tests automatisés `pytest` réussis** (`13 passed`).

- **Documents transversaux :**
  - [`REPONSES_ACTIVITES.md`](./REPONSES_ACTIVITES.md) : Réponses détaillées à toutes les activités, questions de réflexion et tickets de sortie des polycopiés S3 et S4.

---

## 2. Structure détaillée des fichiers

```text
solution_deux_seances/
│
├── README.md                      # Guide principal du projet (ce fichier)
├── requirements.txt               # Dépendances globales épinglées
├── REPONSES_ACTIVITES.md          # Réponses écrites aux questions des polycopiés S3 et S4
│
├── S3/                            # SéanCe 3 : Projet CantineAI (Régression)
│   ├── data/
│   │   ├── exemple_pannes.csv     # Données CantineAI (340 jours d'école)
│   │   └── cantine_repas.csv      # Copie conforme pour compatibilité
│   ├── monprojet/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration (TARGET='repas_servis', TASK='regression', SPLIT='chronologique')
│   │   ├── data.py                # Chargement sécurisé CSV et split temporel
│   │   ├── models.py              # Baseline + 4 modèles candidats
│   │   └── train.py               # Entraînement, évaluation MAE/RMSE/R2, sauvegarde
│   ├── models/                    # Artefacts sauvegardés (model.joblib, metrics.json, model_info.json)
│   ├── docs/
│   │   ├── etude-de-conception.md # Fiche de conception CantineAI
│   │   ├── choix-modele.md        # Analyse des résultats et justification
│   │   └── plan-de-tests.md       # Matrice de validation logicielle
│   └── tests/                     # 14 tests automatisés
│       ├── test_data.py
│       ├── test_models.py
│       └── test_train.py
│
└── S4/                            # SéanCe 4 : Git, HTTP, REST & FastAPI
    ├── README.md                  # Présentation générale de la séance 4
    ├── activite4_demo/            # Première API FastAPI (Activité 4)
    │   ├── demo_api.py            # API autonome avec validation
    │   ├── releve.json            # Payload de test normal (200)
    │   ├── releve_invalide.json   # Payload de test 500 °C (422)
    │   └── README.md              # Instructions de test curl et /docs
    └── TP/
        ├── TP0/                   # Rendu GitHub TP0
        │   ├── README.md
        │   ├── Kenza_Elaiati.md   # Rapport individuel de Kenza ELAIATI
        │   ├── Chaimaa_Haddad.md  # Rapport individuel de Chaimaa HADDAD
        │   └── Rapport_modele.md  # Modèle générique
        └── TP1/                   # API de prédiction MaintAI (13 tests)
            ├── pytest.ini
            ├── requirements.txt
            ├── COMPTE_RENDU.md    # Compte rendu officiel rempli
            ├── maintai/
            │   ├── config.py      # Paramètres et chargement environnement
            │   ├── dataset.py     # Générateur synthétique data/sensors.csv
            │   ├── data.py        # Chargement et partitionnement stratifié
            │   ├── predict.py     # Classe Predictor avec seuil 0.3
            │   ├── train.py       # Entraînement et sauvegarde du modèle
            │   └── api/
            │       ├── schemas.py # SensorReading avec bornes physiques
            │       └── main.py    # Application FastAPI, /health, /v1/predict
            ├── docs/adr/
            │   └── 002-validation.md # Justification des bornes et code 503
            └── tests/             # 13 tests unitaires et d'API
                ├── conftest.py
                ├── test_api.py
                ├── test_data.py
                └── test_train.py
```

---

## 3. Guide d'exécution sous Windows PowerShell

Toutes les commandes ci-dessous sont vérifiées et exécutables directement dans **Windows PowerShell**.

### Étape 1 : Création et activation de l'environnement virtuel

Ouvrez un terminal PowerShell à la racine du projet (`solution_deux_seances`) :

```powershell
# 1. Créer l'environnement virtuel .venv
python -m venv .venv

# 2. Autoriser l'exécution de scripts si nécessaire (une seule fois par machine)
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# 3. Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1
# L'invite de commande affiche désormais (.venv)

# 4. Installer les dépendances
pip install -r requirements.txt
```

---

### Étape 2 : Exécution de la Séance 3 (CantineAI)

```powershell
# Se positionner dans le dossier S3
cd S3

# Lancer la suite de 14 tests automatisés
python -m pytest

# Lancer l'entraînement et l'évaluation comparative des modèles
python -m monprojet.train
```

#### Résultats réels observés sur le jeu de test chronologique :
```text
=================================================================
TABLEAU DE COMPARAISON DES MODÈLES (Séance 3 - CantineAI)
=================================================================
                           mae    rmse     r2
régression linéaire     22.239  28.170  0.883
forêt aléatoire         31.845  41.540  0.746
k plus proches voisins  36.212  46.037  0.688
gradient boosting       39.015  51.049  0.616
baseline (moyenne)      70.271  88.416 -0.151
-----------------------------------------------------------------
Meilleur modèle retenu selon MAE : régression linéaire
```
- Le modèle de régression linéaire réduit l'erreur moyenne de **68.35 %** par rapport à la baseline ($70.27 \rightarrow 22.24$ repas).
- Le modèle entraîné est sauvegardé dans `S3/models/model.joblib` et les métriques dans `S3/models/metrics.json`.

---

### Étape 3 : Exécution de la Séance 4 (FastAPI & MaintAI)

#### A. Démonstration de l'Activité 4
```powershell
# Revenir à la racine puis entrer dans activite4_demo
cd ..\S4\activite4_demo

# Lancer le serveur de démonstration
uvicorn demo_api:app --reload
```
Ouvrez votre navigateur sur : [http://localhost:8000/docs](http://localhost:8000/docs)  
Faites `Ctrl + C` dans le terminal pour arrêter le serveur.

#### B. API de production MaintAI (TP1)
```powershell
# Entrer dans le dossier TP1
cd ..\TP\TP1

# 1. Générer les données synthétiques de capteurs
python -m maintai.dataset
# Écrit 5 000 relevés dans data/sensors.csv

# 2. Entraîner le modèle de maintenance
python -m maintai.train
# Entraîne le classifieur, atteint un rappel de 0.75 au seuil 0.3 et sauvegarde models/model.joblib

# 3. Lancer la suite complète des 13 tests de conformité
python -m pytest
# Résultat : 13 passed en ~3.7 secondes

# 4. Lancer le serveur d'API uvicorn
uvicorn maintai.api.main:app --reload
```

---

### Étape 4 : Test des routes HTTP via `curl.exe`

Pendant qu'`uvicorn` tourne sur le port 8000, ouvrez un **deuxième terminal PowerShell** :

```powershell
# 1. Route de diagnostic /health (renvoie 200)
curl.exe http://localhost:8000/health
# Réponse : {"status":"ok","model_loaded":true}

# 2. Prédiction valide avec seuil d'alerte (renvoie 200)
$body = '{"temperature_c": 72.5, "vibration_mm_s": 6.1, "load_pct": 85.0, "runtime_hours": 15000.0}'
$body | Out-File -Encoding utf8 releve_temp.json
curl.exe -X POST http://localhost:8000/v1/predict -H "Content-Type: application/json" -d "@releve_temp.json"
# Réponse : {"failure_probability":0.9553,"alert":true,"threshold":0.3,"model_version":"..."}

# 3. Test de rejet Pydantic pour valeur hors-bornes (500 °C, renvoie 422)
$invalide = '{"temperature_c": 500.0, "vibration_mm_s": 6.1, "load_pct": 85.0, "runtime_hours": 15000.0}'
$invalide | Out-File -Encoding utf8 invalide_temp.json
curl.exe -X POST http://localhost:8000/v1/predict -H "Content-Type: application/json" -d "@invalide_temp.json"
# Réponse HTTP 422 : Input should be less than or equal to 150

# Nettoyage des fichiers temporaires de test
Remove-Item releve_temp.json, invalide_temp.json -ErrorAction SilentlyContinue
```

---

### Étape 5 : Commandes Git pour la remise finale (Séance 4)

Conformément aux directives de la Séance 4 (pages 4 et 9 du polycopié) :

```powershell
# 1. Créer la branche tp1 pour le TP1
git switch -c tp1

# 2. Ajouter les modifications en excluant les artefacts temporaires
git add TP/TP1
git commit -m "TP1 : API de prédiction MaintAI et validation des tests"
git push -u origin tp1

# 3. Sur GitHub : Ouvrir la Pull Request, faire relire par le binôme, approuver et merger dans main

# 4. Revenir sur main, mettre à jour et poser le tag officiel de rendu
git switch main
git pull
git tag tp1
git push --tags
```
