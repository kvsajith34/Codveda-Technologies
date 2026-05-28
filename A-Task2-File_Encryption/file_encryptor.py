"""
file_encryptor.py
=================
A command-line tool for encrypting and decrypting text files.

Supports two modes:
  1. Fernet (AES-128-CBC + HMAC) via the `cryptography` library  [RECOMMENDED]
  2. Caesar Cipher + XOR fallback (pure Python, no extra dependencies)

Author  : Senior Python Engineer
Version : 1.0.0
Python  : 3.8+
"""

from __future__ import annotations

import os
import sys
import hashlib
import hmac
import struct
import base64
from pathlib import Path

# ---------------------------------------------------------------------------
# Optional import: cryptography (Fernet)
# ---------------------------------------------------------------------------
try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    FERNET_AVAILABLE = True
except ImportError:
    FERNET_AVAILABLE = False


# ===========================================================================
# CONSTANTS
# ===========================================================================

ENCRYPTED_SUFFIX  = ".encrypted"
DECRYPTED_SUFFIX  = "_decrypted.txt"
SALT_SIZE         = 16          # bytes – stored at the start of every encrypted file
PBKDF2_ITERATIONS = 480_000     # OWASP 2023 recommendation for PBKDF2-HMAC-SHA256
CAESAR_SHIFT      = 13          # Fixed Caesar shift used alongside XOR
HMAC_SIZE         = 32          # bytes – SHA-256 HMAC appended in fallback mode


# ===========================================================================
# SECTION 1 – KEY DERIVATION (Fernet mode)
# ===========================================================================

def derive_fernet_key(password: str, salt: bytes) -> bytes:
    """
    Derive a 32-byte Fernet-compatible key from a user password using
    PBKDF2-HMAC-SHA256.

    Args:
        password: Plain-text password supplied by the user.
        salt:     16-byte random salt (generated on encrypt, read on decrypt).

    Returns:
        URL-safe base64-encoded 32-byte key ready for Fernet.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    raw_key = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(raw_key)


# ===========================================================================
# SECTION 2 – FERNET ENCRYPT / DECRYPT
# ===========================================================================

def encrypt_fernet(plaintext: bytes, password: str) -> bytes:
    """
    Encrypt *plaintext* bytes with Fernet (AES-128-CBC + HMAC-SHA256).

    File format written to disk:
        [16 bytes salt] [Fernet ciphertext …]

    Args:
        plaintext: Raw file content as bytes.
        password:  User-supplied password string.

    Returns:
        Bytes to be written to the .encrypted file.
    """
    salt = os.urandom(SALT_SIZE)
    key  = derive_fernet_key(password, salt)
    f    = Fernet(key)
    ciphertext = f.encrypt(plaintext)
    return salt + ciphertext          # prepend salt so decrypt can re-derive key


def decrypt_fernet(ciphertext_blob: bytes, password: str) -> bytes:
    """
    Decrypt a blob produced by *encrypt_fernet*.

    Args:
        ciphertext_blob: Full content of the .encrypted file.
        password:        Same password used during encryption.

    Returns:
        Original plaintext bytes.

    Raises:
        ValueError: If the password is wrong or the file is corrupted.
    """
    if len(ciphertext_blob) <= SALT_SIZE:
        raise ValueError("File is too small to be a valid encrypted file.")

    salt       = ciphertext_blob[:SALT_SIZE]
    ciphertext = ciphertext_blob[SALT_SIZE:]

    key = derive_fernet_key(password, salt)
    f   = Fernet(key)

    try:
        return f.decrypt(ciphertext)
    except InvalidToken as exc:
        raise ValueError(
            "Decryption failed — wrong password or corrupted file."
        ) from exc


# ===========================================================================
# SECTION 3 – CAESAR + XOR FALLBACK ENCRYPT / DECRYPT (pure Python)
# ===========================================================================

def _xor_bytes(data: bytes, key_bytes: bytes) -> bytes:
    """XOR every byte of *data* against the repeating *key_bytes*."""
    key_len = len(key_bytes)
    return bytes(b ^ key_bytes[i % key_len] for i, b in enumerate(data))


def _caesar_shift_bytes(data: bytes, shift: int) -> bytes:
    """Apply a byte-level Caesar shift (mod 256)."""
    return bytes((b + shift) % 256 for b in data)


def _caesar_unshift_bytes(data: bytes, shift: int) -> bytes:
    """Reverse a byte-level Caesar shift."""
    return bytes((b - shift) % 256 for b in data)


def _password_to_key_bytes(password: str) -> bytes:
    """
    Derive a 32-byte key from *password* using SHA-256 (pure Python fallback).
    """
    return hashlib.sha256(password.encode("utf-8")).digest()


def encrypt_fallback(plaintext: bytes, password: str) -> bytes:
    """
    Encrypt using Caesar shift followed by XOR (pure Python — no extra libs).

    ⚠️  This is weaker than Fernet.  Use only when the `cryptography`
        package cannot be installed.

    File format:
        [4 bytes magic "CXFE"] [plaintext length uint32 big-endian]
        [XOR( Caesar(plaintext) ) …] [32 bytes HMAC-SHA256 of previous bytes]

    The HMAC allows wrong-password detection on decryption.

    Args:
        plaintext: Raw file content as bytes.
        password:  User-supplied password string.

    Returns:
        Bytes to write to the .encrypted file.
    """
    key_bytes  = _password_to_key_bytes(password)
    shifted    = _caesar_shift_bytes(plaintext, CAESAR_SHIFT)
    xored      = _xor_bytes(shifted, key_bytes)

    magic      = b"CXFE"
    length_hdr = struct.pack(">I", len(plaintext))   # 4-byte big-endian length
    body       = magic + length_hdr + xored

    # Append HMAC so we can detect wrong passwords / corruption on decrypt
    mac = hmac.new(key_bytes, body, hashlib.sha256).digest()
    return body + mac


def decrypt_fallback(ciphertext_blob: bytes, password: str) -> bytes:
    """
    Decrypt a blob produced by *encrypt_fallback*.

    Args:
        ciphertext_blob: Full content of the .encrypted file.
        password:        Same password used during encryption.

    Returns:
        Original plaintext bytes.

    Raises:
        ValueError: If the magic header is missing, HMAC fails, or password
                    is wrong / file is corrupted.
    """
    MIN_SIZE = 8 + HMAC_SIZE    # 4 magic + 4 length + 32 HMAC

    if len(ciphertext_blob) < MIN_SIZE:
        raise ValueError("File is too small to be a valid encrypted file.")

    magic = ciphertext_blob[:4]
    if magic != b"CXFE":
        raise ValueError(
            "Unrecognised file format.  "
            "Was this file encrypted with the Fernet mode instead?"
        )

    # Split body and MAC
    body       = ciphertext_blob[:-HMAC_SIZE]
    stored_mac = ciphertext_blob[-HMAC_SIZE:]

    key_bytes  = _password_to_key_bytes(password)

    # Verify HMAC before doing any decryption work (timing-safe compare)
    expected_mac = hmac.new(key_bytes, body, hashlib.sha256).digest()
    if not hmac.compare_digest(stored_mac, expected_mac):
        raise ValueError(
            "Decryption failed — wrong password or corrupted file."
        )

    expected_len = struct.unpack(">I", body[4:8])[0]
    ciphertext   = body[8:]

    unxored   = _xor_bytes(ciphertext, key_bytes)
    plaintext = _caesar_unshift_bytes(unxored, CAESAR_SHIFT)

    if len(plaintext) != expected_len:
        raise ValueError(
            "Decryption length mismatch — file may be corrupted."
        )

    return plaintext


# ===========================================================================
# SECTION 4 – FILE I/O HELPERS
# ===========================================================================

def read_file(path: Path) -> bytes:
    """
    Read and return the raw bytes of a file.

    Raises:
        FileNotFoundError: If the path does not exist.
        PermissionError:   If the process lacks read permission.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Path is not a regular file: {path}")
    return path.read_bytes()


def write_file(path: Path, data: bytes) -> None:
    """
    Write *data* bytes to *path*, creating parent directories as needed.

    Raises:
        PermissionError: If the process lacks write permission.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def build_encrypted_path(source: Path) -> Path:
    """Return the .encrypted output path for a given source file."""
    return source.parent / (source.name + ENCRYPTED_SUFFIX)


def build_decrypted_path(source: Path) -> Path:
    """
    Return the _decrypted.txt output path for a given .encrypted file.

    Example:
        notes.txt.encrypted  →  notes.txt_decrypted.txt
    """
    # Strip the .encrypted suffix, then append _decrypted.txt
    stem = source.name[: -len(ENCRYPTED_SUFFIX)]   # e.g. "notes.txt"
    return source.parent / (stem + DECRYPTED_SUFFIX)


# ===========================================================================
# SECTION 5 – HIGH-LEVEL ENCRYPT / DECRYPT ACTIONS
# ===========================================================================

def action_encrypt(use_fernet: bool) -> None:
    """
    Interactive encryption workflow:
      1. Ask for source file path.
      2. Ask for password.
      3. Encrypt and save.
    """
    # ── Input: file path ────────────────────────────────────────────────────
    raw_path = input("\n  Enter path to the .txt file to encrypt: ").strip()
    if not raw_path:
        print("  ✗  No path provided. Returning to menu.")
        return

    source = Path(raw_path)

    # ── Input: password ─────────────────────────────────────────────────────
    password = input("  Enter encryption password/key: ").strip()
    if not password:
        print("  ✗  Password cannot be empty. Returning to menu.")
        return

    confirm = input("  Confirm password: ").strip()
    if password != confirm:
        print("  ✗  Passwords do not match. Returning to menu.")
        return

    # ── Read source ─────────────────────────────────────────────────────────
    try:
        plaintext = read_file(source)
    except (FileNotFoundError, ValueError, PermissionError) as exc:
        print(f"\n  ✗  Error reading file: {exc}")
        return

    # ── Encrypt ─────────────────────────────────────────────────────────────
    try:
        if use_fernet:
            encrypted_data = encrypt_fernet(plaintext, password)
            mode_label = "Fernet (AES)"
        else:
            encrypted_data = encrypt_fallback(plaintext, password)
            mode_label = "Caesar+XOR"
    except Exception as exc:         # pragma: no cover
        print(f"\n  ✗  Encryption error: {exc}")
        return

    # ── Write output ─────────────────────────────────────────────────────────
    out_path = build_encrypted_path(source)
    try:
        write_file(out_path, encrypted_data)
    except PermissionError as exc:
        print(f"\n  ✗  Cannot write output file: {exc}")
        return

    print(f"\n  ✓  Encrypted successfully using {mode_label}!")
    print(f"     Output saved to: {out_path.resolve()}")
    print(f"     Original size  : {len(plaintext):,} bytes")
    print(f"     Encrypted size : {len(encrypted_data):,} bytes")


def action_decrypt(use_fernet: bool) -> None:
    """
    Interactive decryption workflow:
      1. Ask for .encrypted file path.
      2. Ask for password.
      3. Decrypt and save.
    """
    # ── Input: file path ────────────────────────────────────────────────────
    raw_path = input(
        "\n  Enter path to the .encrypted file to decrypt: "
    ).strip()
    if not raw_path:
        print("  ✗  No path provided. Returning to menu.")
        return

    source = Path(raw_path)

    if source.suffix != ENCRYPTED_SUFFIX and not source.name.endswith(ENCRYPTED_SUFFIX):
        print(
            f"  ⚠  Warning: file does not end with '{ENCRYPTED_SUFFIX}'. "
            "Continuing anyway…"
        )

    # ── Input: password ─────────────────────────────────────────────────────
    password = input("  Enter decryption password/key: ").strip()
    if not password:
        print("  ✗  Password cannot be empty. Returning to menu.")
        return

    # ── Read encrypted file ─────────────────────────────────────────────────
    try:
        ciphertext_blob = read_file(source)
    except (FileNotFoundError, ValueError, PermissionError) as exc:
        print(f"\n  ✗  Error reading file: {exc}")
        return

    # ── Decrypt ──────────────────────────────────────────────────────────────
    try:
        if use_fernet:
            plaintext = decrypt_fernet(ciphertext_blob, password)
            mode_label = "Fernet (AES)"
        else:
            plaintext = decrypt_fallback(ciphertext_blob, password)
            mode_label = "Caesar+XOR"
    except ValueError as exc:
        print(f"\n  ✗  Decryption failed: {exc}")
        return
    except Exception as exc:         # pragma: no cover
        print(f"\n  ✗  Unexpected error during decryption: {exc}")
        return

    # ── Write output ─────────────────────────────────────────────────────────
    out_path = build_decrypted_path(source)
    try:
        write_file(out_path, plaintext)
    except PermissionError as exc:
        print(f"\n  ✗  Cannot write output file: {exc}")
        return

    print(f"\n  ✓  Decrypted successfully using {mode_label}!")
    print(f"     Output saved to: {out_path.resolve()}")
    print(f"     Recovered size : {len(plaintext):,} bytes")


# ===========================================================================
# SECTION 6 – MAIN MENU & ENTRY POINT
# ===========================================================================

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║          FILE ENCRYPTION / DECRYPTION TOOL           ║
║                  Level 3 — Advanced                  ║
╚══════════════════════════════════════════════════════╝
"""

MENU = """
  ┌─────────────────────────────┐
  │  1.  Encrypt a text file    │
  │  2.  Decrypt a file         │
  │  3.  Exit                   │
  └─────────────────────────────┘
"""


def select_encryption_mode() -> bool:
    """
    Ask the user whether to use Fernet or the pure-Python fallback.

    Returns:
        True  → use Fernet
        False → use Caesar+XOR fallback
    """
    if not FERNET_AVAILABLE:
        print(
            "\n  ⚠  `cryptography` library not found.\n"
            "     Falling back to Caesar+XOR mode (weaker).\n"
            "     Install with:  pip install cryptography"
        )
        return False

    print("\n  Encryption mode:")
    print("    [1] Fernet / AES-128  (recommended — requires `cryptography`)")
    print("    [2] Caesar+XOR        (pure Python fallback — weaker)")
    choice = input("  Select mode [1/2, default=1]: ").strip()
    return choice != "2"            # default to Fernet


def main() -> None:
    """Entry point — display the menu and dispatch user choices."""
    print(BANNER)

    # Determine the encryption mode once per session.
    use_fernet = select_encryption_mode()
    mode_name  = "Fernet/AES" if use_fernet else "Caesar+XOR"
    print(f"\n  Active mode: {mode_name}")

    while True:
        print(MENU)
        choice = input("  Enter your choice [1-3]: ").strip()

        if choice == "1":
            action_encrypt(use_fernet)

        elif choice == "2":
            action_decrypt(use_fernet)

        elif choice == "3":
            print("\n  Goodbye! Stay secure. 🔐\n")
            sys.exit(0)

        else:
            print("  ✗  Invalid choice. Please enter 1, 2, or 3.")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
