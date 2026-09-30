"""GET /api/config  -  frontend ko Supabase ka public URL + anon key deta hai.
(Anon key public hoti hai; data Row Level Security se surakshit hai.)"""
import os, json
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        b = json.dumps({
            "supabaseUrl": os.environ.get("SUPABASE_URL", ""),
            "supabaseAnonKey": os.environ.get("SUPABASE_ANON_KEY", ""),
            "model": os.environ.get("GEMINI_MODEL", "gemini-3.5-flash"),
            "aiReady": bool(os.environ.get("GEMINI_API_KEY")),
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
