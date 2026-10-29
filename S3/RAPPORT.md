# Rapport de Projet — Séance 3 : CantineAI (Prévision des Repas Scolaires)

**Module :** Développement et déploiement d'applications intelligentes (Séance 3)  
**Binôme :** KENZA ELAIATI — CHAIMAA HADDAD  
**Groupe :** G3  
**Date :** Octobre 2026  

---

## 1. Contexte et Objectifs
La cantine d'un lycée d'environ 650 élèves sert les déjeuners du lundi au vendredi. Chaque matin à 10 h, le gestionnaire doit commander à la cuisine centrale le nombre précis de repas pour le lendemain midi (`repas_servis`).
- **Sur-estimation :** 15 DH jetés par repas non consommé et gaspillage alimentaire ;
- **Sous-estimation :** élèves sans repas, achat d'urgence de sandwichs de remplacement et plaintes des familles.

L'objectif était de concevoir un système d'apprentissage automatique de type **régression supervisée** sur une série temporelle tabulaire pour battre la méthode actuelle (reprendre le chiffre de la semaine passée).

---

## 2. Données et Préparation (Zéro Fuite de Données)
- **Fichier de données :** `data/exemple_pannes.csv` / `data/cantine_repas.csv` (340 jours d'école de septembre 2024 à juin 2026).
- **Variables prédictives ($X$) :** `jour`, `inscrits`, `menu`, `temperature_c`, `pluie_mm`, `examens`, `sortie_scolaire`, `veille_vacances`, `repas_semaine_precedente`.
- **Exclusion stricte :** La cible (`repas_servis`) et la colonne temporelle (`date`) sont exclues des variables d'apprentissage pour éviter tout surapprentissage ou fuite de données (*data leakage*).
- **Découpage chronologique :** 80 % passés en entraînement (272 jours), 20 % futurs en test (68 jours).
- **Gestion des valeurs manquantes :** Imputation par la médiane pour les lundis de reprise post-vacances où `repas_semaine_precedente` est vide. Encodage One-Hot des variables qualitatives (`jour`, `menu`).

---

## 3. Résultats Expérimentaux Réels (`python -m monprojet.train`)

| Modèle candidat | MAE (repas) ↓ | RMSE (repas) ↓ | $R^2$ ↑ |
|---|---:|---:|---:|
| **Régression linéaire** | **22.239** | **28.170** | **0.883** |
| Forêt aléatoire | 31.845 | 41.540 | 0.746 |
| k plus proches voisins | 36.212 | 46.037 | 0.688 |
| Gradient boosting | 39.015 | 51.049 | 0.616 |
| Baseline (moyenne) | 70.271 | 88.416 | -0.151 |

---

## 4. Modèle Sélectionné et Économies Réalisées
- **Modèle retenu :** **Régression linéaire avec préprocesseur complet**.
- **Amélioration :** Réduction de l'erreur moyenne de **68.35 %** par rapport à la baseline ($70.27 \rightarrow 22.24$ repas).
- **Économie financière :** Gain moyen estimé à environ **720 DH par jour de classe** ($48 \times 15\text{ DH}$).
- **Validation du critère métier :** Le seuil imposé était de réduire la MAE d'au moins 30 %. Avec 68.35 %, le critère est **largement validé**.

---

## 5. Validation Logicielle
- **14 tests automatisés `pytest` réussis sur 14 (100 % passants).**
- Respect strict de l'architecture sans chemin en dur hors de `config.py`.
- Modèle sérialisé et sauvegardé dans `models/model.joblib` avec `metrics.json`.

---

## 6. Documents Associés
- Étude de conception détaillée : [`docs/etude-de-conception.md`](./docs/etude-de-conception.md)
- Choix et analyse détaillée du modèle : [`docs/choix-modele.md`](./docs/choix-modele.md)
- Plan de tests et matrice de couverture : [`docs/plan-de-tests.md`](./docs/plan-de-tests.md)
