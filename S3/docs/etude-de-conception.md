# Étude de Conception — Projet CantineAI
**Module :** Développement et déploiement d'applications intelligentes (Séance 3)  
**Binôme :** KENZA ELAIATI — CHAIMAA HADDAD  
**Date :** Octobre 2026  

---

## 1. Utilisateur principal
Le **gestionnaire de la cantine scolaire** d'un lycée d'environ 650 élèves inscrits. Chaque matin d'école du lundi au vendredi à 10 h, il doit passer commande auprès de la cuisine centrale pour le déjeuner du lendemain.

---

## 2. Décision prise et fréquence
- **Décision :** Déterminer le nombre précis de repas à commander et à préparer pour le lendemain midi (`repas_servis`).
- **Fréquence :** Quotidienne (du lundi au vendredi à 10 h, pour le jour scolaire suivant).

---

## 3. Coût d'une erreur
Deux types d'erreurs aux impacts asymétriques :
1. **Sur-estimation (préparer trop de repas) :**
   - *Impact financier :* Environ **15 DH de matière première perdus** par repas non consommé jeté.
   - *Impact environnemental et moral :* Gaspillage alimentaire inacceptable pour l'établissement.
2. **Sous-estimation (préparer trop peu de repas) :**
   - *Impact opérationnel :* Élèves sans déjeuner servi au self.
   - *Impact d'urgence :* Commande en catastrophe de sandwichs de substitution (coût unitaire plus élevé, logistique dégradée).
   - *Impact réputationnel :* Plaintes des parents d'élèves et mécontentement de la direction.

---

## 4. Approche retenue
- **Technologie choisie :** Apprentissage automatique supervisé tabulaire (**Machine Learning — Régression**).
- **Pourquoi pas des règles manuelles ?** La méthode actuelle (reprendre le chiffre du même jour de la semaine précédente) échoue dès qu'un facteur externe intervient : plat du jour apprécié (ex. couscous le vendredi vs poisson ou végétarien), météo pluvieuse (élèves ne sortant pas déjeuner à l'extérieur), sorties scolaires vidant une classe d'âge, ou périodes de révision d'examens.
- **Pourquoi pas le Deep Learning ou un LLM ?**
  - Le jeu de données contient 340 observations (environ 2 années scolaires). Un réseau de neurones profond (Deep Learning) sur-apprendrait immédiatement (overfitting).
  - Un modèle LLM serait lent, disproportionné, coûteux, difficile à héberger localement et non déterministe pour prédire un simple nombre de repas.
  - Les algorithmes de régression tabulaire (Régression Linéaire, Forêt Aléatoire, Gradient Boosting) sont légers, déterministes, rapides à entraîner et hautement interprétables.

---

## 5. Données
- **Fichier :** `data/exemple_pannes.csv` (et copie miroir `data/cantine_repas.csv`).
- **Volume :** 340 jours d'école (septembre 2024 à juin 2026).
- **Absence de données personnelles (RGPD) :** Aucune donnée nominative, identifiant d'élève ou information sensible n'est présente dans le jeu de données.
- **Variables prédictives ($X$) :**
  - `jour` (catégorielle : lundi à vendredi) ;
  - `inscrits` (numérique : effectif inscrit à la cantine, 620 à 700) ;
  - `menu` (catégorielle : poulet, viande, poisson, végétarien, couscous) ;
  - `temperature_c` (numérique : prévision météo °C) ;
  - `pluie_mm` (numérique : prévision de précipitations en mm) ;
  - `examens` (binaire : 0 ou 1) ;
  - `sortie_scolaire` (binaire : 0 ou 1, sortie d'un niveau complet) ;
  - `veille_vacances` (binaire : 0 ou 1) ;
  - `repas_semaine_precedente` (numérique : repas servis 7 jours plus tôt, contient des valeurs manquantes au retour des vacances, imputées par médiane).
- **Variable cible ($y$) :** `repas_servis` (nombre entier de repas servis ce jour-là, entre 250 et 700).
- **Variable temporelle :** `date` (format AAAA-MM-JJ), utilisée exclusivement pour ordonner la série temporelle et exclue des variables d'entrée.
- **Disponibilité à l'inférence :** À 10 h la veille, le menu est arrêté, les prévisions météorologiques du lendemain sont connues, le calendrier des sorties et examens est validé, et l'historique de la semaine passée est archivé. Il n'y a **aucune fuite de données (data leakage)**.

---

## 6. Baseline, Métriques et Critères d'acceptation
- **Baseline de référence :** `DummyRegressor(strategy="mean")`, qui prédit systématiquement la moyenne historique des repas servis.
- **Métrique principale :** **MAE (Mean Absolute Error)** en nombre de repas.
  - *Justification :* La MAE mesure directement en unité métier (nombre de repas) l'écart moyen par jour. Chaque unité de MAE équivaut directement à 15 DH de gaspillage ou à un sandwich de remplacement.
- **Métriques complémentaires :**
  - **RMSE (Root Mean Squared Error) :** Pénalise plus lourdement les gros écarts exceptionnels.
  - **$R^2$ (Coefficient de détermination) :** Mesure la part de variance expliquée par le modèle.
- **Découpage des données :** **Chronologique** (`SPLIT = "chronologique"`), avec les premiers 80 % en entraînement (272 jours passés) et les 20 % les plus récents en test (68 jours futurs).
- **Critère d'acceptation :**
  - Une MAE inférieure d'au moins 30 % à celle de la baseline sur le jeu de test chronologique tenu à l'écart.
  - Dans notre évaluation expérimentale réelle :
    - MAE Baseline : **70.27 repas**
    - MAE Régression Linéaire : **22.24 repas**
    - **Gain obtenu : Réduction de 68.35 % de l'erreur**, le critère d'acceptation est très largement validé !
