# Tally-CA SaaS — Desktop Client

## Setup

```bash
cd apps/desktop-client
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env          # fill in CLIENT_TOKEN + BACKEND_UPLOAD_URL
```

## Run mock / offline test (no Tally required)

```bash
python src/tally_client.py --mock
```

## Run a one-off live sync

```bash
python src/tally_client.py --sync all
```

## Start the background scheduler (every 60 min)

```bash
python src/scheduler.py
```

## Build a standalone Windows executable

```bash
pyinstaller --onefile --noconsole src/tally_client.py
```

