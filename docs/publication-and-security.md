# Public archive and security notes

- Hardcoded MariaDB passwords, Twilio account SID/auth token/from number, SMS recipient, and historical LAN-specific stream endpoint were removed or replaced in the public code copy.
- Avoid uploading the original ZIP, training notebook or final report/PPT: they may contain credentials, personal contact details, images of identifiable people, and third-party material.
- If the originally exposed Twilio/API credentials are still valid, rotate/revoke them. Removing a secret from a new public repository does not revoke the original credential.
- `.env.example` documents configuration names, not actual secrets. Scripts do not automatically load `.env` files.
- No claimed vulnerability fix, smoke test on Raspberry Pi, security hardening, or operational readiness accompanies these publishing edits.
- Browser-triggered SMS calls were disabled in the public copy; `alarm.py` still contains a Twilio path that requires external configuration and real account credentials.
- Image, model and private media artifacts are deliberately excluded.
