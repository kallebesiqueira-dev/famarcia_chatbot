# Security Policy / Politica di Sicurezza

## Supported Versions / Versioni Supportate

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | ✅ Yes / Sì        |
| < 1.0   | ❌ No              |

---

## Reporting a Vulnerability / Segnalare una Vulnerabilità

### 🇬🇧 English

If you discover a security vulnerability in this project, please report it responsibly.

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please send an email to: **security@farmacia-ai-example.com**

Include the following information:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)

**Response timeline:**
- **Acknowledgment:** Within 48 hours
- **Initial assessment:** Within 5 business days
- **Fix release:** Within 30 days for critical issues

We appreciate your help in keeping this project secure!

---

### 🇮🇹 Italiano

Se scopri una vulnerabilità di sicurezza in questo progetto, ti preghiamo di segnalarla in modo responsabile.

**NON** aprire una issue pubblica su GitHub per vulnerabilità di sicurezza.

Invia invece un'email a: **security@farmacia-ai-example.com**

Includi le seguenti informazioni:
- Descrizione della vulnerabilità
- Passaggi per riprodurre il problema
- Impatto potenziale
- Correzione suggerita (se presente)

**Tempistiche di risposta:**
- **Conferma ricezione:** Entro 48 ore
- **Valutazione iniziale:** Entro 5 giorni lavorativi
- **Rilascio correzione:** Entro 30 giorni per problemi critici

Apprezziamo il tuo aiuto nel mantenere sicuro questo progetto!

---

## Security Best Practices / Buone Pratiche di Sicurezza

### Environment Variables / Variabili d'Ambiente

> [!CAUTION]
> Never commit sensitive credentials to version control.

- `DJANGO_SECRET_KEY` — Use a strong, unique secret key in production
- `OPENAI_API_KEY` — Keep API keys private and rotate regularly
- `TWILIO_AUTH_TOKEN` — Never expose authentication tokens
- `DATABASE_URL` — Protect database connection strings

### Production Checklist / Checklist Produzione

- [ ] Set `DJANGO_DEBUG=False`
- [ ] Use a strong `DJANGO_SECRET_KEY` (min 50 characters)
- [ ] Configure `DJANGO_ALLOWED_HOSTS` properly
- [ ] Use HTTPS exclusively
- [ ] Enable CSRF protection
- [ ] Configure CORS to allow only trusted origins
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up rate limiting on API endpoints
- [ ] Enable Django security middleware headers
- [ ] Regularly update dependencies (`pip audit`, `npm audit`)
- [ ] Sanitize all user inputs
- [ ] Implement authentication before going live

### API Security / Sicurezza API

```python
# Example: Rate limiting configuration (future implementation)
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute',
    }
}
```

### Data Privacy / Privacy dei Dati

This application stores chat logs for analytics purposes. In production:

- Implement data retention policies (auto-delete logs after N days)
- Comply with GDPR and local privacy regulations
- Provide users with data export/deletion capabilities
- Anonymize stored data where possible
- Display a clear privacy policy

---

## Dependencies / Dipendenze

Regularly audit dependencies for known vulnerabilities:

```bash
# Python
pip audit

# Node.js
npm audit
npm audit fix
```

---

## Contact / Contatti

- **Security Email:** security@farmacia-ai-example.com
- **General Issues:** Use GitHub Issues for non-security bugs
