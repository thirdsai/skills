"""Start a PDF from a saved thirds.ai template."""

import os

import requests

response = requests.post(
    "https://thirds.ai/v1/pdf",
    headers={
        "Authorization": f"Bearer {os.environ['THIRDS_API_KEY']}",
        "Idempotency-Key": "report-2026-09",
    },
    json={
        "template_id": "tpl_00000000000000000000000000000000",
        "data": {"client": "Northgate Studio", "title": "September report"},
    },
    timeout=30,
    allow_redirects=False,
)
if response.status_code not in (200, 202):
    raise RuntimeError("PDF request failed")

job = response.json()
print(job["id"], job["status"])
