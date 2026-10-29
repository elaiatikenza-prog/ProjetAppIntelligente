# Choix du Modèle — Projet CantineAI
**Module :** Développement et déploiement d'applications intelligentes (Séance 3)  
**Binôme :** KENZA ELAIATI — CHAIMAA HADDAD  
**Date :** Octobre 2026  

---

## 1. Contexte et Problème
Le problème consiste à prédire le nombre de déjeuners servis chaque jour ouvré (`repas_servis`) pour une cantine scolaire comptant entre 620 et 700 élèves inscrits.
L'équipe de gestion doit passer la commande la veille à 10 h. Une mauvaise estimation coûte soit du gaspillage alimentaire direct (15 DH par repas en trop), soit des élèves sans plateau et l'achat précipité de sandwichs de substitution.

---

## 2. Résultats expérimentaux réels sur le jeu de test

Les résultats ci-dessous ont été mesurés directement en exécutant `python -m monprojet.train` sur le jeu de données `data/exemple_pannes.csv` (découpage chronologique : 80 % en entraînement soit 272 jours, 20 % en test soit 68 jours futurs, graine 42) :

| Modèle candidat | MAE (repas) ↓ | RMSE (repas) ↓ | $R^2$ ↑ |
|---|---:|---:|---:|
| **Régression linéaire** | **22.239** | **28.170** | **0.883** |
| **Forêt aléatoire** | 31.845 | 41.540 | 0.746 |
| **k plus proches voisins** | 36.212 | 46.037 | 0.688 |
| **Gradient boosting** | 39.015 | 51.049 | 0.616 |
| **Baseline (moyenne)** | 70.271 | 88.416 | -0.151 |

*Note sur la métrique principale :* Plus la MAE est faible, meilleure est la prédiction (`HIGHER_IS_BETTER["mae"] = False`).

---

## 3. Modèle retenu et justification

### Modèle sélectionné : **Régression linéaire (avec préprocesseur ColumnTransformer)**

### Pourquoi ce choix ?
1. **Performance supérieure :** La régression linéaire obtient la MAE la plus basse (**22.239 repas**) et explique **88.3 %** de la variance sur le jeu de test ($R^2 = 0.883$).
2. **Gain par rapport à la baseline :**
   $$\text{Écart absolu} = 70.271 - 22.239 = 48.032 \text{ repas}$$
   $$\text{Réduction relative de l'erreur} = \frac{70.271 - 22.239}{70.271} \times 100 = 68.35\,\%$$
   L'erreur quotidienne moyenne passe de ~70 repas à ~22 repas, ce qui représente une économie journalière estimée à :
   $$48 \text{ repas} \times 15\text{ DH} \approx 720\text{ DH par jour d'école}.$$
3. **Excellente régularité et absence de surapprentissage :**
   Sur un échantillon modeste (272 lignes d'entraînement), les modèles ensemblistes (Forêt Aléatoire, Gradient Boosting) souffrent légèrement de la variance liée au découpage temporel. Le modèle linéaire avec variables standardisées et One-Hot Encoding capture de façon optimale les contributions additives du menu (effet couscous vs végétarien), de la météo et des sorties scolaires.
4. **Interprétabilité et robustesse :**
   Les coefficients du modèle linéaire sont directement explicables aux cuisiniers et au gestionnaire de l'établissement.

---

## 4. Critère d'acceptation métier
- **Critère fixé :** Obtenir une MAE inférieure d'au moins 30 % à la baseline sur les 20 % de jours les plus récents (jeu de test chronologique).
- **Constat :** Avec une amélioration de **68.35 %**, le critère d'acceptation est **largement validé**.

---

## 5. Limites et pistes d'amélioration
1. **Événements exceptionnels non répertoriés :** En cas d'intempérie extrême imprévue ou d'épidémie soudaine, le modèle dépend de la qualité des prévisions saisies la veille à 10 h.
2. **Périodes post-vacances :** Au retour de congés scolaires, `repas_semaine_precedente` est indisponible ; l'imputation par médiane fonctionne mais une modélisation dédiée au premier jour de reprise pourrait affiner l'estimation.
3. **Ré-entraînement continu :** Le modèle doit être ré-entraîné au minimum une fois par trimestre pour intégrer les évolutions d'effectifs et les tendances culinaires des élèves.
