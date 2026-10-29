# Réponses Complètes aux Activités et Bilans — Séances 3 et 4
**Module :** Développement et déploiement d'applications intelligentes  
**Binôme :** KENZA ELAIATI — CHAIMAA HADDAD  
**Date :** Octobre 2026  

---

# SÉANCE 3 — Conception, Reproductibilité et Entraînement

## Activité 1 — Faire tourner le projet d'un autre (Karim)
**Affirmation de Karim :** *« Ça marche chez moi, on obtient 14,2 % d'alertes. »*

En inspectant le notebook `analyse.ipynb` du dossier `projet_a_reparer.zip`, voici les **6 anomalies majeures** qui empêchent toute reproductibilité :

1. **Chemin absolu propriétaire en dur :**  
   `df = pd.read_csv("C:/Users/Karim/Desktop/PFE/donnees_capteurs.csv")`  
   Ce fichier est situé sur le bureau privé de la machine de Karim. Sur tout autre ordinateur, le notebook plante dès la ligne 2 avec un `FileNotFoundError`.
2. **Cellules exécutées dans le désordre :**  
   La cellule 4 appelle `model = LogisticRegression().fit(X_train, y_train)` alors que les variables `X_train` et `y_train` ne sont créées que dans la cellule 5 (`train_test_split`) ! Karim a ré-exécuté des cellules vers le haut sans redémarrer le noyau.
3. **Variables manquantes (état mémoire résiduel) :**  
   Les variables `colonnes` (dans `X = df[colonnes]`) et `seuil` (dans `proba >= seuil`) ne sont jamais définies ni instanciées dans le notebook. Elles proviennent d'une manipulation interactive non sauvegardée.
4. **Absence de graine aléatoire (`random_state`) :**  
   L'appel `train_test_split(X, y, test_size=0.2)` n'utilise aucun `random_state`. Le découpage change à chaque exécution du kernel, rendant le taux de 14,2 % impossible à reproduire.
5. **Absence de gestion des dépendances :**  
   Aucun fichier `requirements.txt` avec versions épinglées (`==`). Une version différente de scikit-learn ou pandas peut changer les comportements par défaut.
6. **Absence de tests automatisés :**  
   Aucun test `pytest` ne vient valider la justesse du prétraitement ou du pipeline.

---

## Activité 2 — Environnement et lancement du squelette
1. **Pourquoi `python monprojet/train.py` peut-il échouer ?**  
   Lorsqu'on lance directement un script dans un sous-dossier, Python positionne `sys.path[0]` dans ce sous-dossier. Les imports relatifs comme `from . import config` ou `from monprojet import config` échouent alors avec `ModuleNotFoundError: No module named 'monprojet'` ou `ImportError: attempted relative import with no known parent package`.  
   Il faut impérativement lancer depuis la racine avec la syntaxe de module : `python -m monprojet.train`.
2. **Quelles fonctions écrire et dans quels fichiers ?**  
   - `data.py` : `load_data()` (chargement robuste, contrôle cible) et `split()` (découpage chronologique/aléatoire) ;
   - `models.py` : `candidates()` (baseline en premier + au moins 3 modèles) ;
   - `train.py` : `evaluate()` (calcul des métriques) et `main()` (boucle d'entraînement, tableau comparatif, sauvegarde `model.joblib` et `metrics.json`).

---

## Activité 3 — Fiche de conception : MaintAI vs CantineAI
*(Voir également le document complet [`S3/docs/etude-de-conception.md`](./S3/docs/etude-de-conception.md))*

### Questions de synthèse par prototype :
- **MaintAI : un modèle qui ne prédit jamais de panne aurait quelle accuracy ? Pourquoi cette métrique ne convient-elle pas ?**  
  Dans le jeu de 5 000 relevés, 17,6 % des lignes sont des pannes et 82,4 % sont saines. Un modèle qui prédit toujours « pas de panne » (0) atteint donc une accuracy de **82,4 % (0,824)**.  
  Cette métrique est inacceptable car le rappel de ce modèle est de **0 %** : il ne prévient aucune défaillance et laisse toutes les lignes de production s'arrêter. Sur des classes déséquilibrées, l'accuracy masque complètement l'inefficacité sur la classe critique.
- **CantineAI : pourquoi ne faut-il pas tirer les jours de test au hasard ?**  
  Les repas servis forment une série temporelle. Un tirage aléatoire (`SPLIT = "random"`) mélangerait le futur et le passé : le modèle utiliserait des informations postérieures pour prédire des journées antérieures (**fuite de données temporelle / data leakage**). Le découpage chronologique (`SPLIT = "chronologique"`) garantit que le modèle est évalué dans les conditions réelles de la production : entraîné sur le passé, testé sur le futur.

---

## Activité 4 — Le tableau des résultats
- **Question : le groupe au meilleur score a-t-il le meilleur modèle ?**  
  Pas nécessairement. Un score ne peut être comparé que si les groupes utilisent :
  1. Le même jeu de données et le même découpage chronologique ;
  2. La même métrique adaptée aux enjeux métiers (ex. MAE vs MSE) ;
  3. Des protocoles sans fuite de données. Un score anormalement bas peut cacher un surapprentissage ou une fuite d'informations futures.

---

## Lab 2.1 — Résultats réels obtenus sur CantineAI
Exécution réelle de `python -m monprojet.train` sur `data/exemple_pannes.csv` :

| Modèle candidat | MAE (repas) | RMSE (repas) | $R^2$ |
|---|---:|---:|---:|
| **Régression linéaire** | **22.239** | **28.170** | **0.883** |
| Forêt aléatoire | 31.845 | 41.540 | 0.746 |
| k plus proches voisins | 36.212 | 46.037 | 0.688 |
| Gradient boosting | 39.015 | 51.049 | 0.616 |
| Baseline (moyenne) | 70.271 | 88.416 | -0.151 |

- **Meilleur modèle :** Régression linéaire.
- **Gain par rapport à la baseline :** Réduction de **68.35 %** de la MAE ($70.27 \rightarrow 22.24$ repas).
- **Critère d'acceptation métier ($\ge 30\,\%$) :** Largement validé.

---

## Ticket de sortie — Séance 3
1. **Quelle est la baseline de votre projet, et son score ?**  
   La baseline est `DummyRegressor(strategy="mean")`, qui prédit la moyenne historique des repas. Son score est une MAE de **70.271 repas** sur le jeu de test chronologique.
2. **Pourquoi évaluer tous les modèles sur le même jeu de test ?**  
   Pour que la comparaison soit strictement équitable. Si chaque modèle était évalué sur des échantillons différents, les écarts mesurés refléteraient la variance des sous-ensembles plutôt que la qualité propre de l'algorithme.
3. **Dans quel cas l'accuracy peut-elle tromper ?**  
   Quand les classes sont très déséquilibrées : un modèle prédisant bêtement la classe majoritaire affiche une très haute accuracy tout en ayant un rappel de zéro sur la classe d'intérêt.
4. **Qu'est-ce qui reste flou ?**  
   La prise en compte fine des jours fériés mobiles et des ponts scolaires dans la série temporelle.

---
---

# SÉANCE 4 — Git, HTTP, REST et FastAPI

## Activité 3 — Le web vu de près & Quiz Codes HTTP
- **Méthode :** GET ou POST  
- **URL :** ex. `http://localhost:8000/v1/predict`  
- **Deux en-têtes :** `Content-Type: application/json`, `User-Agent: curl/8.x`  
- **Une requête hors 200 :** 404 Not Found (ressource ou route inexistante), 422 Unprocessable Entity (donnée invalide).

### Quiz : Quel code renvoie l'API MaintAI ?
| Situation | Code HTTP | Explication |
|---|:---:|---|
| (a) Une température de 500 °C | **422** | Validation Pydantic échouée (`Field(le=150)`) |
| (b) L'URL `/v1/predcit` | **404** | Route inconnue (faute de frappe dans l'URI) |
| (c) Le modèle n'est pas chargé | **503** | Service Unavailable (`predictor is None`) |
| (d) La clé API est absente | **401** | Unauthorized (non authentifié) |
| (e) Un bug dans le code de l'API | **500** | Internal Server Error |

---

## Activité 4 — Démonstration FastAPI (`demo_api.py`)
- `GET /health` renvoie le statut **200** avec `{"status": "ok"}`.
- `POST /v1/predict` avec `{"temperature_c": 70}` renvoie le statut **200** avec `{"alert": false}`.
- `POST /v1/predict` avec une température de 500 renvoie **422 Unprocessable Entity**. Le contrôle est effectué par Pydantic avant même l'appel de la fonction.

---

## TP1 — API MaintAI : Résultats et Synthèse

### Résultats réels obtenus sur les tests du TP1 (`python -m pytest`) :
- **Tests initiaux :** 10 passed, 3 failed (échec car `schemas.py` et `main.py` non implémentés).
- **Tests après écriture de `schemas.py` :** 10 passed, 3 failed avec `NotImplementedError` (signe que la validation Pydantic accepte les relevés corrects).
- **Tests finaux après écriture de `predict()` :** **13 passed, 0 failed** en 3.68 s.

### Résultats des 4 requêtes réelles :
1. `GET /health` $\rightarrow$ **200** `{"status": "ok", "model_loaded": true}`
2. `POST /v1/predict` (relevé normal) $\rightarrow$ **200** `{"failure_probability": 0.9553, "alert": true, "threshold": 0.3, "model_version": "..."}`
3. `POST /v1/predict` (température 500 °C) $\rightarrow$ **422** `{"detail": [{"type": "less_than_equal", "loc": ["body", "temperature_c"], ...}]}`
4. `POST /v1/predicte` (faute de frappe) $\rightarrow$ **404** `{"detail": "Not Found"}`

---

## Ticket de sortie — Séance 4
1. **Que fait `git pull`, et quand faut-il le lancer ?**  
   `git pull` télécharge les commits distants depuis GitHub et les fusionne dans la branche locale. Il faut le lancer au début de chaque session de travail et systématiquement avant d'effectuer un `git push`.
2. **Quel code renvoie l'API pour une température de 500 °C, et qui écrit ce contrôle ?**  
   Code **422 Unprocessable Entity**. Le contrôle est généré automatiquement par FastAPI grâce aux contraintes de bornes déclarées dans le schéma Pydantic (`Field(ge=-40, le=150)`).
3. **Pourquoi rendre le TP par une pull request plutôt que pousser sur main ?**  
   Pour permettre la relecture de code croisée (code review), la vérification des tests d'intégration par le binôme, et garantir que la branche `main` reste toujours propre et fonctionnelle.
4. **Qu'est-ce qui reste flou ?**  
   L'authentification sécurisée des micro-services via des jetons JWT ou OAuth2.
