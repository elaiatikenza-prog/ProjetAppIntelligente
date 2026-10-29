# TP0 : MaintAI

**Nom :** À compléter · **Groupe :** À compléter

## Le problème
Prédire une panne à partir de quatre mesures de capteurs (`temperature_c`, `vibration_mm_s`, `load_pct`, `runtime_hours`). Une panne manquée peut arrêter une ligne de production ; il faut détecter les pannes tout en limitant les fausses alertes.

## Résultats sur le jeu de test
Le tableau ci-dessous est un exemple indicatif donné dans le polycopié, pas le résultat garanti de votre exécution.

| Modèle | Accuracy | Rappel | Précision |
|---|---:|---:|---:|
| Baseline | 0,824 | 0,000 | 0,000 |
| Régression logistique | 0,889 | 0,574 | 0,737 |

## Mon choix, et pourquoi
À compléter à partir du tableau produit par votre entraînement. Pour ce contexte, le rappel est important car les pannes manquées ont un coût élevé ; la précision doit aussi être considérée afin de limiter les fausses alertes.

## Le critère (rappel ≥ 0,75) est-il atteint ?
Dans l'exemple du polycopié, le rappel de 0,574 ne satisfait pas le critère de 0,75. Vérifier et remplacer cette phrase selon vos résultats réels.

## Ce qui reste flou
À compléter avec votre propre question ou difficulté.
