# 🔐 File Encryption / Decryption Tool

>
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Cryptography](https://img.shields.io/badge/cryptography-Fernet%2FAES-green?logo=letsencrypt&logoColor=white)](https://cryptography.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Internship](https://img.shields.io/badge/Codveda-Internship%20Project-orange)](https://codveda.com)

---

## 📌 Project Overview

A command-line Python tool that **encrypts and decrypts text files** using two modes:

| Mode | Algorithm | Requirement |
|---|---|---|
| ✅ **Fernet (Recommended)** | AES-128-CBC + HMAC-SHA256 | `pip install cryptography` |
| 🔁 **Fallback** | Caesar Cipher + XOR + HMAC-SHA256 | Pure Python — no extra packages |

The tool auto-detects whether the `cryptography` library is installed and lets the user choose their preferred mode at startup.

---

## 📁 Project Structure

```
task2-file-encryptor/
│
├── file_encryptor.py      # Main script — all logic lives here
├── README.md              # This file
└── test_file.txt          # (Optional) Sample file for testing
```

---

## ⚙️ How It Works

### Fernet Mode (Recommended)
```
plaintext → PBKDF2-HMAC-SHA256(password + random salt) → Fernet key
         → AES-128-CBC encrypt → HMAC-SHA256 authenticate
         → [16B salt] + [Fernet ciphertext]  →  saved as .encrypted
```

### Caesar + XOR Fallback Mode
```
plaintext → Caesar-shift (mod 256) → XOR with SHA-256(password)
          → [4B magic] + [4B length] + [ciphertext] + [32B HMAC]
          →  saved as .encrypted
```

Both modes include **HMAC integrity checking** — wrong passwords and corrupted files are detected immediately.

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/codveda-internship.git
cd codveda-internship/level3-task2
```

### 2. (Recommended) Install the cryptography library
```bash
pip install cryptography
```
> Skip this step if you want to use the pure-Python Caesar+XOR fallback.

### 3. Run the tool
```bash
python file_encryptor.py
```

---

## 🖥️ Usage

On launch you will see:

```
╔══════════════════════════════════════════════════════╗
║          FILE ENCRYPTION / DECRYPTION TOOL           ║
║                  Level 3 — Advanced                  ║
╚══════════════════════════════════════════════════════╝

  Encryption mode:
    [1] Fernet / AES-128  (recommended)
    [2] Caesar+XOR        (pure Python fallback)
  Select mode [1/2, default=1]:
```

Then the main menu:

```
  ┌─────────────────────────────┐
  │  1.  Encrypt a text file    │
  │  2.  Decrypt a file         │
  │  3.  Exit                   │
  └─────────────────────────────┘
```

### Encrypting a file
```
Choice: 1
  Enter path to the .txt file to encrypt: secret_notes.txt
  Enter encryption password/key: ••••••••
  Confirm password: ••••••••

  ✓  Encrypted successfully using Fernet (AES)!
     Output saved to: /home/user/secret_notes.txt.encrypted
     Original size  : 48 bytes
     Encrypted size : 172 bytes
```

### Decrypting a file
```
Choice: 2
  Enter path to the .encrypted file: secret_notes.txt.encrypted
  Enter decryption password/key: ••••••••

  ✓  Decrypted successfully using Fernet (AES)!
     Output saved to: /home/user/secret_notes.txt_decrypted.txt
     Recovered size : 48 bytes
```

### File naming convention

| Input file | Encrypted output | Decrypted output |
|---|---|---|
| `notes.txt` | `notes.txt.encrypted` | `notes.txt_decrypted.txt` |
| `report.txt` | `report.txt.encrypted` | `report.txt_decrypted.txt` |

---

## ✅ Testing

```bash
# Step 1 — Create a test file
echo "This is my secret document." > test_file.txt

# Step 2 — Encrypt
python file_encryptor.py
# → Choose mode 1 → option 1 → path: test_file.txt → password: Test1234!

# Step 3 — Verify the encrypted file looks like binary noise
cat test_file.txt.encrypted

# Step 4 — Decrypt
python file_encryptor.py
# → Choose mode 1 → option 2 → path: test_file.txt.encrypted → password: Test1234!

# Step 5 — Confirm original content is restored
diff test_file.txt test_file.txt_decrypted.txt
# (no output = files are identical ✓)

# Step 6 — Test wrong password (should show a clean error, not crash)
python file_encryptor.py
# → Choose mode 1 → option 2 → path: test_file.txt.encrypted → password: WrongPass
```

---

## 🔒 Security Notes

| Topic | Detail |
|---|---|
| **Fernet strength** | AES-128-CBC + HMAC-SHA256 — industry-standard symmetric encryption |
| **Key derivation** | PBKDF2-HMAC-SHA256 with 480 000 iterations (OWASP 2023 standard) |
| **Random salt** | A fresh 16-byte salt is generated per encryption — same password never produces the same ciphertext |
| **Integrity checking** | Both modes append an HMAC — tampering or wrong passwords are detected immediately |
| **Caesar+XOR warning** | The fallback mode is for educational purposes only — not suitable for sensitive data |
| **No key storage** | Passwords are never saved anywhere — losing your password means losing your data |
| **RAM exposure** | The password lives as a plain Python `str` in memory during the session |

---

## 🧠 Concepts Demonstrated

- Symmetric encryption (Fernet / AES-128-CBC)
- Password-based key derivation (PBKDF2-HMAC-SHA256)
- HMAC integrity verification (`hmac.compare_digest` — timing-safe)
- Classical ciphers (Caesar cipher + XOR)
- File I/O with `pathlib`
- Modular, PEP 8-compliant Python code
- Graceful error handling (`FileNotFoundError`, `PermissionError`, `InvalidToken`)
- Clean CLI design with user-friendly messages

---

## 🔮 Future Enhancements (Level 4 Ideas)

- [ ] Password masking with `getpass.getpass()`
- [ ] Encrypt entire directories recursively
- [ ] CLI flags via `argparse` (`--encrypt`, `--decrypt`, `--mode`)
- [ ] Key-file mode (random key file instead of password)
- [ ] Streaming encryption for large files (chunked I/O)
- [ ] GUI with `tkinter` (file picker + password field)
- [ ] Audit log of all encrypt/decrypt events

---

## 👤 Author

**KVS Ajith**

---

*Level 3 · Task 2 — Basic File Encryption/Decryption Tool*
