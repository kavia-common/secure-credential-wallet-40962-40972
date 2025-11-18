# Security Notes

- This codebase uses a placeholder stream XOR + HMAC for encryption in src/security/crypto.py.
- For production, replace with a vetted cipher (e.g., AES-256-GCM via `cryptography` package) and manage keys via a KMS.
- JWTs are signed with HS256 using SECRET_KEY. Rotate keys periodically and consider asymmetric keys for multi-service environments.
- Environment variables are required; see `.env.example`.
