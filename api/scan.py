"""POST /api/scan  -  bill photo -> Gemini -> JSON
Header: Authorization: Bearer <supabase access token>
Body:   {"mime": "image/jpeg", "data": "<base64>"}
"""
import os, sys, json, time
from http.server import BaseHTTPRequestHandler

import requests

sys.path.append(os.path.dirname(__file__))
from _prompt import PROMPT, SCHEMA, ALLOWED_MIME  # noqa: E402

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
SB_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SB_ANON = os.environ.get("SUPABASE_ANON_KEY", "")


def user_from_token(token: str):
    """Supabase se poochho: ye token asli user ka hai?"""
    if not token:
        return None
    r = requests.get(f"{SB_URL}/auth/v1/user",
                     headers={"apikey": SB_ANON, "Authorization": f"Bearer {token}"}, timeout=10)
    return r.json() if r.status_code == 200 else None


def gemini_read(data_b64: str, mime: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    body = {
        "contents": [{"parts": [{"text": PROMPT},
                                {"inline_data": {"mime_type": mime, "data": data_b64}}]}],
        "generationConfig": {"responseMimeType": "application/json",
                             "responseSchema": SCHEMA, "temperature": 0},
    }
    r = requests.post(url, headers={"x-goog-api-key": GEMINI_KEY}, json=body, timeout=55)
    if r.status_code != 200:
        raise RuntimeError(f"AI error {r.status_code}: {r.text[:200]}")
    res = r.json()
    text = res["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text), res.get("usageMetadata", {}).get("totalTokenCount", 0)


class handler(BaseHTTPRequestHandler):
    def _send(self, obj, code=200):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        try:
            if not (GEMINI_KEY and SB_URL and SB_ANON):
                return self._send({"error": "Server setup adhoora hai (environment variables)."}, 500)
            token = self.headers.get("Authorization", "").replace("Bearer ", "").strip()
            if not user_from_token(token):
                return self._send({"error": "Login zaroori hai."}, 401)
            n = int(self.headers.get("Content-Length", 0))
            if n > 4_300_000:
                return self._send({"error": "Photo bahut badi hai."}, 413)
            data = json.loads(self.rfile.read(n) or b"{}")
            mime = data.get("mime", "image/jpeg")
            if mime not in ALLOWED_MIME or not data.get("data"):
                return self._send({"error": "Sirf JPG, PNG, WEBP ya PDF chalega."}, 400)
            t0 = time.time()
            bill, tokens = gemini_read(data["data"], mime)
            self._send({"bill": bill, "tokens": tokens, "seconds": round(time.time() - t0, 1)})
        except Exception as e:
            self._send({"error": str(e)[:300]}, 500)
