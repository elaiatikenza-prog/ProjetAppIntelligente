# ADR 003 — Sécurité : transmission de la clé API et politique CORS

- **Statut :** Accepté
- **Date :** 05/11/2026
- **Décideurs :** Kenza ELAIATI, Chaimaa HADDAD

---

## 1. Contexte

L'API MaintAI expose un modèle de maintenance prédictive industriel. Seuls les clients autorisés doivent pouvoir interroger la route `/v1/predict`. De plus, des clients web exécutés dans le navigateur (ex: tableau de bord hébergé sur un port local ou un serveur dédié) doivent pouvoir communiquer avec l'API sans exposer le système à des attaques CSRF ou des accès non autorisés.

Deux questions architecturales majeures se posent :
1. Par quel canal transmettre la clé API d'authentification ?
2. Quelle politique CORS (*Cross-Origin Resource Sharing*) adopter et comment la configurer ?

---

## 2. Décision 1 : Transmission de la clé API via un en-tête HTTP (`X-API-Key`)

### Choix retenu
La clé API est transmise obligatoirement dans l'en-tête HTTP standard `X-API-Key`.

### Alternatives rejetées et pertes évitées
- **Alternative rejetée : Dans l'URL (ex: `/v1/predict?api_key=...`)**  
  *Ce que l'on perdrait :* Les URLs sont enregistrées en clair dans tous les journaux d'accès (logs Nginx, reverse proxies, pare-feu), dans l'historique du navigateur web, dans les en-têtes `Referer` et les favoris. Une fuite de clé serait inévitable et irréversible sans régénération complète.
- **Alternative rejetée : Dans le corps de la requête JSON (ex: `{"key": "...", ...}`)**  
  *Ce que l'on perdrait :* La responsabilité de l'authentification serait mélangée avec le schéma métier (`SensorReading`). La clé devrait être analysée et validée par Pydantic à chaque requête, et les requêtes HTTP `GET` ou `DELETE` ne disposent pas de corps standard pour s'authentifier. De plus, les frameworks et passerelles d'API (API Gateways) filtrent les requêtes au niveau des en-têtes sans avoir à parser l'intégralité du corps JSON.

---

## 3. Décision 2 : Politique CORS avec liste blanche stricte configurée via variables d'environnement

### Choix retenu
L'API active le middleware FastAPI `CORSMiddleware` avec une liste d'origines autorisées explicitement définie (`MAINTAI_CORS_ORIGINS`), lue depuis les variables d'environnement (`.env`). Par défaut en développement : `http://localhost:5500,http://127.0.0.1:5500`.

### Alternatives rejetées et pertes évitées
- **Alternative rejetée : Autoriser toutes les origines avec un joker (`allow_origins=["*"]`)**  
  *Ce que l'on perdrait :* Tout site tiers malveillant (ex: `http://evil.example`) exécuté dans le navigateur d'un opérateur connecté pourrait envoyer des requêtes et récupérer des données industrielles sensibles ou déclencher de faux diagnostics. L'isolation du navigateur serait totalement neutralisée.
- **Alternative rejetée : Origines écrites en dur dans le code Python**  
  *Ce que l'on perdrait :* La flexibilité des déploiements. En pré-production ou production (Séance 8), les domaines et ports changent. Forcer une modification du code pour changer une origine enfreindrait le principe *Twelve-Factor App*. Grâce à Pydantic Settings (`maintai/config.py`), les origines sont modifiables sans recompiler ni toucher au code source.

---

## 4. Conséquences

- Les requêtes `/v1/*` sans clé ou avec une clé invalide reçoivent immédiatement `401 Unauthorized` (protégé par `secrets.compare_digest` à temps constant contre les attaques temporelles).
- La route `/health` reste publique pour permettre aux sondes d'orchestration (Kubernetes, Docker healthchecks) de tester l'état de l'API.
- Les navigateurs tiers accédant hors liste blanche voient leur requête pré-vol (`OPTIONS`) bloquée sans en-tête `Access-Control-Allow-Origin`.
