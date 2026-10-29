# Activité 4 — Démonstration FastAPI (`demo_api.py`)

Ce dossier contient l'exercice préparatoire de la Séance 4 (page 7 du polycopié étudiant).

## 1. Lancement du serveur

Depuis ce dossier dans PowerShell :

```powershell
uvicorn demo_api:app --reload
```

Le serveur démarre sur [http://localhost:8000](http://localhost:8000).

## 2. Documentation interactive Swagger UI

Ouvrez votre navigateur sur :
[http://localhost:8000/docs](http://localhost:8000/docs)

- Testez `GET /health` (cliquez sur "Try it out" puis "Execute") : renvoie le code **200** avec `{"status": "ok"}`.
- Testez `POST /v1/predict` avec une température de `70` : renvoie le code **200** avec `{"alert": false}`.
- Testez `POST /v1/predict` avec une température de `500` : Pydantic bloque la requête avant d'appeler la fonction Python et renvoie le code **422 Unprocessable Entity**.

## 3. Test sans navigateur avec `curl.exe`

Dans un second terminal PowerShell :

```powershell
# Vérification de santé (GET)
curl.exe http://localhost:8000/health

# Prédiction valide (renvoie 200)
curl.exe -X POST http://localhost:8000/v1/predict -H "Content-Type: application/json" -d "@releve.json"

# Prédiction hors-bornes (renvoie 422)
curl.exe -X POST http://localhost:8000/v1/predict -H "Content-Type: application/json" -d "@releve_invalide.json"
```

*Note importante Windows PowerShell :* Ne jamais entourer le corps JSON d'apostrophes sous Windows dans `curl.exe`, car les guillemets internes sont déformés. Utilisez toujours `-d "@nom_fichier.json"`.
