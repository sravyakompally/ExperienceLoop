"""Isolated Hindsight integration. Uses the official SDK when configured.

Install the SDK and configure HINDSIGHT_API_KEY / HINDSIGHT_URL.
This module deliberately reports unavailable rather than pretending SQLite is memory.
"""
import os

class HindsightMemory:
    def __init__(self):
        self.api_key = os.getenv("HINDSIGHT_API_KEY", "")
        self.base_url = os.getenv("HINDSIGHT_URL", "https://api.hindsight.vectorize.io")
        self.bank_id = os.getenv("HINDSIGHT_BANK_ID", "experienceloop")

    def retain(self, record):
        if not self.api_key:
            return {"stored": False, "status": "not_configured",
                    "message": "Hindsight is not configured; saved locally only."}
        try:
            from hindsight_client import Hindsight  # official package import; verify against installed SDK version
            client = Hindsight(base_url=self.base_url, api_key=self.api_key)
            content = "\n".join(f"{k}: {v}" for k, v in record.items() if v)
            result = client.retain(bank_id=self.bank_id, content=content)
            return {"stored": True, "status": "stored", "memory_id": str(result)}
        except Exception as exc:
            return {"stored": False, "status": "unavailable", "message": str(exc)}
