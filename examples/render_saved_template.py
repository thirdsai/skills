"""Make one PDF from a saved thirds.ai template and JSON data."""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

ORIGIN = "https://thirds.ai"
TEMPLATE_ID = re.compile(r"tpl_[0-9a-f]{32}\Z")


class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise RuntimeError("A request tried to redirect.")


OPENER = build_opener(RejectRedirects)


def read_json(response):
    return json.load(response)


def api_call(path, key, *, body=None, request_key=None):
    headers = {"Authorization": f"Bearer {key}", "Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
        headers["Idempotency-Key"] = request_key
    request = Request(
        ORIGIN + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers=headers,
        method="POST" if body is not None else "GET",
    )
    with OPENER.open(request, timeout=30) as response:
        return read_json(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template_id")
    parser.add_argument("data_file", type=Path)
    parser.add_argument("output_file", type=Path)
    parser.add_argument("--version", type=int)
    parser.add_argument("--idempotency-key", required=True,
                        help="Use the same key and arguments if you retry a lost response.")
    args = parser.parse_args()
    key = os.environ.get("THIRDS_API_KEY")
    if not key:
        parser.error("Set THIRDS_API_KEY in your private environment.")
    if not TEMPLATE_ID.fullmatch(args.template_id):
        parser.error("Use a saved template ID that starts with tpl_.")
    data = json.loads(args.data_file.read_text())
    if not isinstance(data, dict):
        parser.error("The data file must hold one JSON object.")

    body = {"template_id": args.template_id, "data": data, "wait": False}
    if args.version is not None:
        body["version"] = args.version
    job = api_call("/v1/pdf", key, body=body, request_key=args.idempotency_key)
    job_id = job["id"]
    deadline = time.monotonic() + 120
    while job.get("status") in {"queued", "running"}:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RuntimeError(f"Render {job_id} is still running. Check the same job later.")
        time.sleep(min(2, remaining))
        job = api_call(f"/v1/pdf/{job_id}", key)
    if job.get("status") != "succeeded":
        raise RuntimeError(f"Render {job_id} ended with status {job.get('status')}.")

    signed_url = urljoin(ORIGIN, job["download"]["url"])
    parsed_url = urlparse(signed_url)
    if parsed_url.scheme != "https" or parsed_url.netloc != urlparse(ORIGIN).netloc:
        raise RuntimeError("The download host did not match thirds.ai.")
    with OPENER.open(signed_url, timeout=30) as response:
        output = response.read()
    artifact = job["artifact"]
    if (not output.startswith(b"%PDF-")
            or len(output) != artifact["byte_size"]
            or hashlib.sha256(output).hexdigest() != artifact["sha256"]):
        raise RuntimeError("The PDF did not match the finished job.")
    args.output_file.write_bytes(output)
    print(f"Saved {args.output_file} from render {job_id}.")


if __name__ == "__main__":
    try:
        main()
    except (HTTPError, URLError, KeyError, ValueError, RuntimeError) as error:
        # The API error body may hold private request details. Do not print it.
        print(f"Render failed: {type(error).__name__}.", file=sys.stderr)
        raise SystemExit(1) from None
