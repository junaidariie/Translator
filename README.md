# 🌍 Polyglot — Multilingual AI Translator

Polyglot is a modern, fast and visually polished **AI translation app** that supports **100+ languages** using Facebook’s `m2m100_418M` model.  
It features a sleek Streamlit interface, animated loaders, light/dark theme toggle, safe clipboard copy and deployment-ready backend.

---

## ✅ Features

✅ Translate text between **100+ languages**  
✅ Built with **Facebook M2M100 (418M)** multilingual model  
✅ **FastAPI backend** already implemented (production-ready)  
✅ Streamlit frontend with:
- ✨ Light + Dark UI mode  
- 🎯 One-time model loading  
- ⏳ Beautiful 3-dot loading animation  
- 📋 One-click “Copy Translation”  
✅ Supports Hindi, English, Chinese, Arabic, Tamil, French + 90+ more  
✅ Fully offline — works locally without an API key

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Model     | Facebook M2M100 (418M) |
| Backend   | FastAPI (deploy-ready) |
| Frontend  | Streamlit UI with CSS animations |
| Language Mapping | Custom dictionary (100+ codes) |

---

## 📁 Project Structure

```
Translator/
│
├── translator.py            # Model loading & translation functions
├── main.py                  # Streamlit UI
└── README.md
```

---

## 🚀 Running Locally

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

Minimum requirements:
```
streamlit
transformers
torch
```

### 2️⃣ Run the app
```bash
streamlit run main.py
```

### ✅ Now the app opens at:
```
http://localhost:8501
```

---

## ✅ How It Works

- The model loads only once (cached)
- UI shows animated dots while:
  - Loading model
  - Translating text
- After completing translation, the loader **disappears**
- Output appears in a separate soft-highlighted box

---

## 🧠 Model Info

| Property | Value |
|----------|-------|
| Name | facebook/m2m100_418M |
| Size | 418M parameters |
| Type | Multilingual Sequence-to-Sequence |
| Supports | 100+ languages, both directions |

---

## ✅ Deployment-Ready FastAPI Backend

This project includes a **complete FastAPI backend** for production deployment.  
It exposes a `/translate` endpoint that accepts text + source + target + returns JSON translation.

If cloud access was available, the Streamlit UI could consume the API instead of running locally.

You can deploy backend on:
- Render
- Railway
- Vercel serverless
- AWS / Azure / GCP
- DigitalOcean Apps

📌 API is ready — just needs cloud credit to upload.

---

## 📸 Screenshots (optional)

_Add screenshots here if needed._

---

## ✅ Example Translation

| Input Language | Output Language | Result |
|----------------|----------------|--------|
| English | Hindi | ✅ हेलो मेरा नाम है जुली |
| Hindi | English | ✅ My name is Julie |

---

## 🤝 Contributions

Pull requests welcome.  
Add new languages, UI themes or speech-to-text support.

---

## 📜 License

MIT License — free to use & modify.

---

## 💬 Credits

Built by **Junaid**  
• Practical ML apps  
• Deep learning, Streamlit, NLP & FastAPI
