# Safe Watch — Crowd Density Monitoring (2023 Capstone)

> **Archive of a 2023 university capstone prototype.** This repository documents the implementation and test evidence from that time. **It is not a currently running or end-to-end reproducible application.** The original Raspberry Pi is not available. The TFLite model, label file, and WAV alarm were recovered in a separate private backup, but are intentionally excluded from this public repository; the Flask API server source remains missing.

## Overview

Safe Watch attempted to monitor a camera scene, count detected people with a TensorFlow Lite model, calculate a density indicator, record results in MariaDB, and display live camera video and monitoring information through Nginx/PHP/AJAX. The 4-person team also developed risk-level alerts and tested the prototype indoors and outdoors.

The project was performed in **March–June 2023** as a **4-person university capstone**.

## Historical architecture

```text
Raspberry Pi 4 + Camera Module 3
    ├─ stream.py : Picamera2 → MJPEG HTTP stream (port 8000)
    │      ├─ Browser iframe: live camera view
    │      └─ main.py: capture a frame → before.jpg
    └─ main.py → count_objects.py (TensorFlow Lite detection)
                       └─ detected people count → configured area ratio → risk level
                                └─ MariaDB: receive_data / cameras / density VIEW
                                        ├─ Nginx + PHP + AJAX → dashboard and graphs
                                        └─ alarm.py → WAV audio / Twilio SMS (code path)
```

**Important:** Image analysis was periodic rather than true 1-second inference. The supplied `configs.ini` has `delay=15`; the personal report shows a historical `delay=10`. Processing time is additional to the sleep in the submitted code.

## Technologies

- Hardware/OS: Raspberry Pi 4, Camera Module 3, Raspberry Pi OS/Raspbian, VNC, SSH
- Application: Python, Picamera2, OpenCV, TensorFlow Lite, Nginx, PHP, HTML/CSS/JavaScript, AJAX, Chart.js
- Data: MariaDB, `mysql.connector`, PHP MySQLi, SQL tables and VIEW
- Alert: USB speaker using `aplay`, Twilio SMS integration code; **historical SMS receipt independently evidenced by a phone screenshot**

## Work division (from contemporaneous final report)

| Workstream | Assigned role |
|---|---|
| Web server and database research/build, dynamic PHP/AJAX pages | Repository owner's documented responsibility |
| Camera MJPEG streaming integration, alert/SMS implementation | Repository owner's documented responsibility |
| Model training, datasets and model deployment | Other team member |
| Density calculation rule research | Other team member |
| Raspberry Pi hardware procurement and initial connections | Other team member |

The submitted code is an archive of **team output**; file authorship cannot be independently established for every line. The original report documents the owner's responsibilities, not exclusive authorship of all uploaded code.

## Evidence and verified scope

- Historical photos and video show local-network access to the monitoring page, camera view, recognition output, and risk display.
- A recorded database test shows **manually inserted measurements** reflected in the web status and graphs.
- A recorded test shows the **risk modal dialog** for a danger measurement.
- A later-supplied 2023 phone screenshot confirms **receipt of multiple Twilio trial-account danger-alert SMS messages** matching the format in `alarm.py`. [Evidence and limitations](docs/sms-receipt-evidence-2023.md).
- Outdoor and indoor tests identified practical recognition limits; the report notes unreliable recognition at longer distances and false positives for mannequins.
- **Not verified:** end-to-end **camera-detected real crowd danger → SMS** (as opposed to manually induced/test danger states), the exact sending process responsible for the screenshot, end-to-end reproducibility today, quantitative model accuracy, automatic daemon/service restart.

Historical videos/reports containing people, phone numbers and account information are intentionally **not published**.

## Repository structure

- [`src/python/`](src/python/) — historical Raspberry Pi scripts, with credentials externalized
- [`src/web/`](src/web/) — historical Nginx/PHP web pages, with DB passwords externalized
- [`database/schema_legacy_percent.sql`](database/schema_legacy_percent.sql) — supplied SQL variant; see important differences in `docs/implementation-notes.md`
- [`docs/`](docs/) — architecture, known limitations, troubleshooting, publication notes
- [`.env.example`](.env.example) — variable names only; not a verified deployment procedure

## Configuration and limitations

For safety, hardcoded database credentials, Twilio credentials, recipient numbers, and a historical camera LAN URL have been removed/replaced. **These are publication edits, not changes verified on original hardware.** Environment variables must be injected into relevant processes before attempting use. The sample `.env.example` is not loaded automatically by the scripts.

The original model (`models/people_detect.tflite`), label file, and WAV audio were recovered in private backups but are **not published** here. The Flask `app.py` server source has not been recovered. `src/web/index.html` has an `RPI_IP_ADDRESS` placeholder; browser-triggered SMS is disabled in the public copy. SQL setup and camera record initialization also require environment-specific steps. Re-running this version **has not been tested**.

## Sources, attribution and rights

Code in the object-detection and Picamera2 streaming paths includes references/structures drawn from external examples. We preserve original comments and provide references in [`docs/attribution.md`](docs/attribution.md). No universal project-wide open-source license is granted here; third-party and teammate contributions may have independent rights. If you intend to reuse code, verify relevant source licenses and contact rights holders.

## Project reflection

The primary value of this repository is documenting systems integration: camera streaming, DB-backed monitoring, PHP data exchange, Linux environment setup, and device output troubleshooting, rather than presenting a production crowd-safety solution.

## 2026 reconstruction from the 2023 project Q&A

The [reconstructed code package](reconstructed/README.md) organizes the Raspberry Pi scripts, Nginx/PHP frontend, MariaDB schema, configuration samples, and local tests by deployment location. It is **a new, documented reconstruction**, not an exact copy of the 2023 running system.

- [Reconstructed Raspberry Pi implementation](reconstructed/01_raspberry_pi_project/)
- [Reconstructed web server implementation](reconstructed/02_nginx_webroot/)
- [Database and migration](reconstructed/03_database/)
- [Setup notes and example service files](reconstructed/04_configuration/)
- [Comparison and provenance](reconstructed/05_documentation/COMPARISON_AND_PROVENANCE.md)
- [Tests and static verification limits](reconstructed/05_documentation/TEST_REPORT.md)

The earlier `src/` and `database/schema_legacy_percent.sql` are preserved as archival source. Actual 2023 backup ZIP internals, proprietary model and warning-audio assets, and original Flask API source were not fully recovered; end-to-end operation on Raspberry Pi hardware has not been established.
