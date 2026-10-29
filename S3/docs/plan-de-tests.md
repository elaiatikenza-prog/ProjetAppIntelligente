# Plan de Tests Automatisés — Projet CantineAI
**Module :** Développement et déploiement d'applications intelligentes (Séance 3)  
**Binôme :** KENZA ELAIATI — CHAIMAA HADDAD  
**Date :** Octobre 2026  

---

## 1. Objectifs du plan de tests
Le plan de tests garantit la **reproductibilité**, l'**intégrité des données** et la **fiabilité des prédictions** du projet CantineAI avant tout déploiement.
Il répond aux exigences du polycopié de la Séance 3 :
1. Aucun chemin en dur hors de `config.py` ;
2. Découpage chronologique sans fuite de données futures vers le passé ;
3. Exclusion stricte de la cible de l'espace des caractéristiques ;
4. Vérification que le meilleur modèle bat la baseline de référence ;
5. Gestion robuste des valeurs manquantes et des formats CSV.

---

## 2. Matrice des tests implémentés

Les tests sont répartis dans le dossier `tests/` et exécutés automatiquement avec `pytest` :

### A. Tests des données (`tests/test_data.py`)
| Nom du test | Objectif vérifié | Type |
|---|---|---|
| `test_load_data_renvoie_un_tableau_avec_la_cible` | Vérifie que `load_data()` renvoie un DataFrame non vide avec la colonne `repas_servis` sans NaN. | Unitaire / Intégration |
| `test_load_data_drops_missing_target` | Vérifie que les lignes sans valeur cible sont automatiquement filtrées. | Cas limite |
| `test_load_data_missing_target_raises` | Vérifie qu'une `ValueError` explicite est levée si la colonne cible est absente du fichier. | Robustesse |
| `test_feature_columns_excludes_time_and_target` | Vérifie qu'aucune fuite de données n'est possible (`repas_servis` et `date` ne figurent jamais dans les entrées). | Sécurité ML |
| `test_split_separe_entrainement_et_test` | Vérifie que l'union des indices d'entraînement et de test reconstitue le jeu complet sans chevauchement. | Découpage |
| `test_split_chronologique_teste_sur_le_futur` | Vérifie que pour un découpage temporel, $\max(\text{train.date}) \le \min(\text{test.date})$. | Cohérence temporelle |

### B. Tests des modèles (`tests/test_models.py`)
| Nom du test | Objectif vérifié | Type |
|---|---|---|
| `test_la_baseline_est_le_premier_modele` | Vérifie que le premier estimateur de `candidates()` est une baseline (`DummyRegressor`). | Pédagogique |
| `test_au_moins_trois_modeles_en_plus_de_la_baseline` | Vérifie la présence d'au moins 4 modèles au total dans le banc de comparaison. | Exigence du TP |

### C. Tests d'entraînement et d'évaluation (`tests/test_train.py`)
| Nom du test | Objectif vérifié | Type |
|---|---|---|
| `test_evaluate_renvoie_la_metrique_principale` | Vérifie que `evaluate()` retourne un dictionnaire contenant la clé `mae` en type float. | Métriques |
| `test_main_ecrit_les_resultats` | Vérifie la génération sur le disque de `model.joblib` et `metrics.json`. | Sauvegarde |
| `test_le_meilleur_modele_bat_la_baseline` | Vérifie que le modèle sélectionné a une MAE strictement inférieure à la baseline. | Performance |
| `test_evaluate_regression_metrics_complete` | Vérifie que MAE, RMSE et $R^2$ sont correctement calculées et positives pour les erreurs. | Métriques |
| `test_preprocessing_handles_missing_values_and_categories` | Vérifie que le pipeline gère les NaN de `repas_semaine_precedente` et l'encodage One-Hot sans planter. | Prétraitement |
| `test_meilleur_modele_reduit_l_erreur_d_au_moins_trente_pourcent` | Vérifie l'atteinte du critère métier (réduction d'erreur $\ge 30\,\%$, réel : $68.35\,\%$) | Métier / Acceptation |

---

## 3. Procédure d'exécution sous Windows PowerShell

```powershell
# 1. Se positionner dans le dossier S3
cd S3

# 2. Lancer la suite complète de tests
python -m pytest -v

# 3. Lancer l'entraînement et la comparaison
python -m monprojet.train
```

**Résultat attendu :** 14 tests réussis (`14 passed`), 0 échec.
