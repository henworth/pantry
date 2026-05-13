# pantry — Pantry Items Service

FastAPI + SQLAlchemy + Postgres CRUD service for pantry items. Managed with `uv`.

## Endpoints

All endpoints are served under `${API_PREFIX}` (default `/pantry`). When deployed to an ephemeral environment, the prefix becomes `/<envName>/pantry`.

| Method | Path | Description |
| --- | --- | --- |
| GET | `/healthz` | Liveness |
| POST | `/items` | Create a pantry item |
| GET | `/items` | List items (filters: `category`, `location`, `expiring_within_days`) |
| GET | `/items/{id}` | Read one |
| PATCH | `/items/{id}` | Partial update |
| DELETE | `/items/{id}` | Delete |

## Environment

- `DATABASE_URL` — SQLAlchemy URL, e.g. `postgresql+psycopg://app:app@localhost:5432/pantry_db`
- `API_PREFIX` — path prefix (default `/pantry`)

## Local dev

Natively with `uv` (just this service + your own Postgres):

```bash
uv sync
cp .env.example .env   # edit DATABASE_URL if needed
uv run uvicorn app.main:app --reload --port 8000
```

For the full cross-service stack (postgres + pantry + shopping-list with hot reload), check out the [infra repo](https://github.com/your-org/infra) as a sibling of this one and run:

```bash
cd ../infra
docker compose -f docker-compose.dev.yaml up --build
curl http://localhost:8000/pantry/healthz
```

## Build the container

```bash
uv lock                        # first time only, commits uv.lock
docker build -t pantry .
```
