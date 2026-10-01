PROMPT = """You are reading a purchase invoice (bill) from an Indian pharmacy/wholesale supplier.
Extract every product line item exactly as printed. Rules:
- Do not guess. If a value is not visible or unreadable, use null.
- Numbers must be plain numbers (no currency symbols, no commas).
- expiry: keep as printed (e.g. "08/27" or "Aug-2027").
- bill_date: as printed.
- Do not include totals/tax summary rows as items."""

SALES_PROMPT = """You are reading a SALES bill from an Indian shop (pharmacy, wholesale, clothing, electronics etc.).
It may be a printed retail invoice, a carbon/handwritten counter slip, or a handwritten sales diary page with many entries.
Extract every product line sold. Rules:
- supplier_name: put the CUSTOMER / party name here if written, else null (walk-in sale).
- Do not guess. If a value is not visible or unreadable, use null.
- Numbers must be plain numbers (no currency symbols, no commas).
- expiry and batch only if written; bill_date as written.
- If a diary page has several small sales, list every line as an item.
- Do not include totals, discounts summary, payment or tax summary rows as items."""

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
