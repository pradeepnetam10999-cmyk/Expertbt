from pathlib import Path
from dotenv import set_key

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"

def store_provider_key(provider: str, key: str):
    names = {"finnhub": "FINNHUB_API_KEY", "twelve_data": "TWELVE_DATA_API_KEY"}
    if provider not in names or not key.strip():
        raise ValueError("Unsupported provider or empty API key")
    ENV_PATH.touch(exist_ok=True)
    set_key(str(ENV_PATH), names[provider], key.strip())
    return {"provider": provider, "configured": True,
            "message": "Saved in backend/.env. Restart backend to load updated settings."}
