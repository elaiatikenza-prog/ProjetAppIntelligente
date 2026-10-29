# Séance 4 — Git, HTTP, REST et FastAPI

**Module :** Développement et déploiement d'applications intelligentes  
**Binôme :** KENZA ELAIATI — CHAIMAA HADDAD  

---

## Organisation des dossiers

Ce dossier regroupe tous les travaux demandés pour la Séance 4 :

1. **`TP/TP0/` — Rapports d'évaluation MaintAI**
   - Rapports individuels de chaque membre du binôme (`Kenza_Elaiati.md`, `Chaimaa_Haddad.md`) ;
   - Modèle de référence [`Rapport_modele.md`](./TP/TP0/Rapport_modele.md) ;
   - Respect strict des consignes Git (commis dans `TP/TP0`).

2. **`activite4_demo/` — Première API FastAPI**
   - Implémentation du script de découverte [`demo_api.py`](./activite4_demo/demo_api.py) (routes `/health` et `/v1/predict`) ;
   - Fichiers d'exemples de requêtes [`releve.json`](./activite4_demo/releve.json) et [`releve_invalide.json`](./activite4_demo/releve_invalide.json) ;
   - Guide d'exécution sous Windows PowerShell avec `uvicorn` et `curl.exe`.

3. **`TP/TP1/` — API de production MaintAI**
   - Code complet du module `maintai` (API FastAPI, schémas Pydantic avec bornes physiques, cycle de vie `lifespan`, prédiction avec `Predictor`) ;
   - Suite de 13 tests automatisés (`tests/test_api.py`, `tests/test_data.py`, `tests/test_train.py`) — **13 passed** ;
   - Décision d'architecture [`docs/adr/002-validation.md`](./TP/TP1/docs/adr/002-validation.md) justifiant les bornes physiques et le code 503 ;
   - Compte rendu officiel complet [`COMPTE_RENDU.md`](./TP/TP1/COMPTE_RENDU.md) avec sorties réelles de test et réponses aux questions théoriques.

---

## Commandes d'exécution rapide (Windows PowerShell)

```powershell
# 1. Se positionner dans TP/TP1
cd S4\TP\TP1

# 2. Générer les données d'entraînement et entraîner le modèle
python -m maintai.dataset
python -m maintai.train

# 3. Lancer la suite des 13 tests
python -m pytest

# 4. Lancer le serveur d'API
uvicorn maintai.api.main:app --reload
```
Accéder ensuite à la documentation Swagger interactive sur : [http://localhost:8000/docs](http://localhost:8000/docs)
