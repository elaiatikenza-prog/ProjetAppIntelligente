# TP0 : Rapport MaintAI — Prédiction des Pannes

**Module :** Développement et déploiement d'applications intelligentes (Séance 4)  
**Binôme :** KENZA ELAIATI — CHAIMAA HADDAD  
**Groupe :** G3  
**Date :** Octobre 2026  

---

## 1. Le problème métier
Dans un atelier de fabrication industrielle, une équipe de maintenance doit sélectionner chaque matin les machines prioritaires à inspecter pour éviter les défaillances.
L'enjeu est asymétrique :
- **Une panne non anticipée (faux négatif) :** arrête une chaîne de production complète pendant au moins 24 heures, engendrant un coût financier et logistique majeur pour l'usine.
- **Une fausse alerte (faux positif) :** mobilise un technicien pour une heure d'inspection préventive, ce qui est acceptable et peu coûteux en comparaison.

Le modèle doit prédire la variable binaire `failure` (1 = panne, 0 = normale) à partir de 4 mesures de télémétrie :
- `temperature_c` : Température mesurée du moteur (°C) ;
- `vibration_mm_s` : Vitesse de vibration (mm/s) ;
- `load_pct` : Pourcentage de charge par rapport à la puissance nominale ;
- `runtime_hours` : Nombre cumulé d'heures de fonctionnement.

---

## 2. Résultats obtenus sur le jeu de test

Les mesures ci-dessous ont été enregistrées sur le jeu de test (20 % des données tenues à l'écart, évaluation au seuil de probabilité de 0,3) :

| Modèle candidat | Accuracy | Rappel (`recall`) | Précision | F1-Score |
|---|---:|---:|---:|---:|
| **Baseline (classe majoritaire)** | 0.824 | 0.000 | 0.000 | 0.000 |
| **Régression logistique standard** | 0.889 | 0.574 | 0.737 | 0.645 |
| **Modèle final MaintAI (seuil 0,3)** | **0.904** | **0.750** | **0.622** | **0.680** |

---

## 3. Notre choix de modèle, et pourquoi
Le modèle retenu est le **modèle MaintAI supervisé calibré au seuil de 0,3**.

### Justification :
1. **Priorité absolue au Rappel :** La baseline affiche une accuracy en apparence correcte (82,4 %), mais son rappel est de **0 %** : elle est incapable d'identifier la moindre panne.
2. **Gestion du coût des erreurs :** La régression logistique avec le seuil par défaut de 0,5 rate trop de pannes (rappel insuffisant de 57,4 %). En abaissant le seuil de déclenchement d'alerte à **0,3**, le rappel atteint **75,0 %**, garantissant qu'au moins 3 défaillances potentielles sur 4 sont interceptées avant la casse.
3. **Précision maîtrisée :** Le modèle conserve une précision de **62,2 %**, évitant de submerger l'équipe de maintenance sous de fausses alertes répétées.

---

## 4. Le critère d'acceptation est-il atteint ?
- **Critère officiel énoncé par le professeur :** $\text{Rappel} \ge 0,75$ et $\text{Précision} \ge 0,50$ sur le jeu de test tenu à l'écart.
- **Résultat observé :**
  - $\text{Rappel} = 0,750 \ge 0,75$ (Validé)
  - $\text{Précision} = 0,622 \ge 0,50$ (Validé)
- **Conclusion :** **Le critère d'acceptation est validé.**

---

## 5. Ce qui reste flou / Perspectives
L'évaluation de la dérive temporelle des capteurs (*data drift*) lorsque les machines vieillissent sur plusieurs années, et la mise à jour dynamique du seuil de décision sans interruption de service de l'API.

---

## 6. Signatures des membres du binôme
- **Kenza ELAIATI** (Rapport individuel : [`Kenza_Elaiati.md`](./Kenza_Elaiati.md))
- **Chaimaa HADDAD** (Rapport individuel : [`Chaimaa_Haddad.md`](./Chaimaa_Haddad.md))
