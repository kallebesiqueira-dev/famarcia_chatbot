<![CDATA[# 💊 Farmacia AI Assistant

> Assistente farmaceutico virtuale bilingue (IT/EN) con intelligenza artificiale.

![Farmacia AI Assistant — Welcome](docs/screenshot.png)

![Farmacia AI Assistant — Active Conversation](docs/screenshot_chat.png)

---

## ✨ Funzionalità

- 🤖 **AI-powered** — Integrazione OpenAI (GPT-4/4o) per risposte intelligenti
- 🇮🇹🇬🇧 **Bilingue** — Italiano e Inglese con rilevamento automatico della lingua
- 💊 **Knowledge Base farmaceutica** — Consigli su farmaci da banco, sintomi comuni
- 📱 **WhatsApp** — Invia conversazioni direttamente su WhatsApp
- 🕐 **Info farmacia** — Orari, contatti, servizi disponibili
- 🎨 **UI moderna** — Interfaccia premium con animazioni e design glassmorphism
- 📊 **Analytics** — Logging completo delle conversazioni per statistiche
- 🔄 **Fallback offline** — Funziona anche senza backend con risposte rule-based

---

## 🛠️ Tech Stack

| Layer | Tecnologia |
|-------|-----------|
| **Frontend** | React 19 + Vite 8 |
| **Backend** | Django 4.2 + Django REST Framework |
| **AI** | OpenAI API (GPT-4 / GPT-4o / GPT-4o-mini) |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Styling** | Vanilla CSS con glassmorphism + gradients |

---

## 🚀 Quick Start

### Prerequisiti

- Python 3.10+
- Node.js 18+
- (Opzionale) API Key OpenAI

### 1. Clone

```bash
git clone https://github.com/your-username/farmacia-chatbot.git
cd farmacia-chatbot
```

### 2. Backend

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Apri nel browser

```
http://localhost:5173/
```

---

## ⚙️ Configurazione AI

Edita il file `backend/.env`:

```env
# Modalità mock (senza API key, risposte rule-based)
AI_PROVIDER=mock

# Modalità OpenAI (risposte AI reali)
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-la-tua-chiave-qui
AI_MODEL=gpt-4o-mini    # o gpt-4, gpt-4o, gpt-3.5-turbo
AI_MAX_TOKENS=500
```

| Modello | Costo | Velocità | Consigliato |
|---------|-------|----------|-------------|
| `gpt-4` | Alto | Lento | ❌ |
| `gpt-4o` | Medio | Veloce | ✅ Produzione |
| `gpt-4o-mini` | Basso | Molto veloce | ✅ Sviluppo |
| `gpt-3.5-turbo` | Molto basso | Veloce | ⚠️ Legacy |

---

## 📁 Struttura Progetto

```
farmacia-chatbot/
├── backend/
│   ├── chatbot/          # App chat (views, AI engine, models)
│   │   ├── ai_engine.py  # Motore AI bilingue con knowledge base
│   │   ├── views.py      # API endpoints REST
│   │   ├── models.py     # ChatLog model
│   │   └── ...
│   ├── pharmacy/         # App farmacia (prodotti, info)
│   ├── config/           # Settings Django
│   ├── .env              # Variabili d'ambiente
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components (Header, ChatBox, etc.)
│   │   ├── services/     # API client
│   │   └── App.jsx       # Root component
│   └── package.json
├── docs/
│   └── screenshot.png
├── SECURITY.md
└── README.md
```

---

## 🔒 Sicurezza

Consulta [SECURITY.md](SECURITY.md) per:
- Gestione API keys e variabili d'ambiente
- Checklist produzione
- Policy segnalazione vulnerabilità

---

## 📄 Licenza

Questo progetto è distribuito sotto licenza [MIT](LICENSE).

---

<p align="center">
  Made with ❤️ for Italian pharmacies
</p>
]]>
