# 🧾 Bill Scanner

**Bill ki photo se automatic purchase entry.** AI (Google Gemini) supplier ke bill ko padhta hai: product, batch, expiry, qty, free, MRP, rate, GST aur amount nikal ke ek editable table mein dikhata hai. User check karke save karta hai.

Made for Indian pharmacies, wholesalers and retail shops.

## Features
- 📸 Photo / PDF upload (phone camera se bhi)
- 🤖 AI se line items nikalna (Gemini)
- ✏️ Review screen: galat row peeli dikhti hai, bill total match check
- 🔐 Har user ka alag account (Supabase Auth), sirf apna data dikhta hai (Row Level Security)
- 📋 History + ⬇️ Excel (CSV) export

## Tech
| Part | Tool |
|---|---|
| Frontend | Plain HTML/JS (`index.html`) |
| Backend | Python serverless function on Vercel (`api/scan.py`) |
| AI | Google Gemini API |
| Database + Login | Supabase |

## Setup
1. **Supabase:** naya project banaiye → SQL Editor mein `supabase.sql` chalaiye.
2. **Gemini:** [aistudio.google.com](https://aistudio.google.com) se API key.
3. **Vercel:** is repo ko import kariye aur ye Environment Variables daaliye (dekhiye `.env.example`):
   - `GEMINI_API_KEY`
   - `GEMINI_MODEL` (default `gemini-3.5-flash`)
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
4. Deploy. 🎉

> ⚠️ API keys kabhi code mein mat daaliye. `.env` git mein nahi jaata (`.gitignore`).

## Security notes
- Gemini key sirf server (`api/scan.py`) pe rehti hai, browser tak nahi jaati.
- `/api/scan` sirf logged-in user ke liye chalta hai (Supabase token check).
- Supabase anon key public hoti hai; data RLS policies se surakshit hai.

---
Built by **Tabish Ali Khan** ([@Hamza313-cyber](https://github.com/Hamza313-cyber))
