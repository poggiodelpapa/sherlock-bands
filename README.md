# 🔔 Monitor Pagina Sapienza

Script che monitora automaticamente la pagina:
👉 https://www.uniroma1.it/it/node/40540

Se rileva un cambiamento, ti manda un'email.

---

## ⚙️ Setup (5 minuti)

### 1. Crea un repository GitHub

- Vai su [github.com](https://github.com) → **New repository**
- Chiamalo ad es. `monitor-sapienza`
- Spunta **"Add a README file"** → Create repository

### 2. Carica i file

Carica in questo ordine:
- `monitor.py` → nella root del repo
- `.github/workflows/monitor.yml` → crea le cartelle manualmente o usa git

Struttura finale del repo:
```
monitor-sapienza/
├── monitor.py
├── last_hash.txt          ← creato automaticamente alla prima esecuzione
└── .github/
    └── workflows/
        └── monitor.yml
```

### 3. Configura Gmail App Password

1. Vai su [myaccount.google.com](https://myaccount.google.com)
2. **Sicurezza** → **Verifica in due passaggi** (deve essere attiva)
3. Cerca **"Password per le app"** → crea una nuova password per "Mail"
4. Copia la password di 16 caratteri (es. `abcd efgh ijkl mnop`)

### 4. Aggiungi i Secrets su GitHub

Nel tuo repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Aggiungi questi 3 secrets:

| Nome | Valore |
|------|--------|
| `EMAIL_MITTENTE` | la tua email Gmail (es. `mario@gmail.com`) |
| `EMAIL_DESTINATARIO` | dove ricevere le notifiche (può essere uguale) |
| `GMAIL_APP_PASSWORD` | la password di 16 caratteri del punto 3 |

### 5. Abilita i permessi di scrittura per Actions

Nel repo → **Settings** → **Actions** → **General** → **Workflow permissions**
→ seleziona **"Read and write permissions"** → Save

### 6. Prima esecuzione manuale

- Vai su **Actions** → seleziona il workflow **"Monitora Pagina Sapienza"**
- Clicca **"Run workflow"**
- La prima volta salva solo l'hash iniziale (nessuna email)
- Dalla seconda in poi ti avvisa se cambia qualcosa

---

## 🕐 Frequenza di controllo

Nel file `monitor.yml`, la riga:
```yaml
- cron: "0 * * * *"   # ogni ora
```

Puoi cambiarla con:
- `"0 */6 * * *"` → ogni 6 ore
- `"0 9,18 * * *"` → alle 9 e alle 18 ogni giorno
- `"0 9 * * 1-5"` → ogni giorno feriale alle 9

---

## 📝 Note

- GitHub Actions è **gratuito** per repo pubblici e ha 2000 minuti/mese gratis per repo privati (più che sufficienti).
- L'hash viene salvato nel file `last_hash.txt` nel repo.
