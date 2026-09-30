PROMPT = """You are reading a purchase invoice (bill) from an Indian pharmacy/wholesale supplier.
Extract every product line item exactly as printed. Rules:
- Do not guess. If a value is not visible or unreadable, use null.
- Numbers must be plain numbers (no currency symbols, no commas).
- expiry: keep as printed (e.g. "08/27" or "Aug-2027").
- bill_date: as printed.
- Do not include totals/tax summary rows as items."""

N = {"type": "NUMBER", "nullable": True}
S = {"type": "STRING", "nullable": True}

SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "supplier_name": S,
        "bill_number": S,
        "bill_date": S,
        "bill_total": N,
        "items": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "product_name": {"type": "STRING"},
                    "batch": S, "expiry": S, "qty": N, "free_qty": N,
                    "mrp": N, "rate": N, "gst_percent": N, "amount": N,
                },
                "required": ["product_name"],
            },
        },
    },
    "required": ["items"],
}

ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
