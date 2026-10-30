# Implementation and verification notes

## Historical data flow

1. Picamera2 streams a camera image over an MJPEG HTTP endpoint at port 8000.
2. `main.py` resolves the device's `wlan0` IP, captures a JPEG frame, and invokes `count_objects.detect()`.
3. `count_objects.py` loads an external TensorFlow Lite model/labels and writes an annotated frame into the Nginx static path.
4. `main.py` divides the detected number of people by the configured `total_area` and writes the computed value plus the risk label to `receive_data`.
5. PHP accesses MariaDB and responds in JSON to browser polling requests; graphs use Chart.js.
6. `alarm.py` polls the latest danger status and attempts WAV playback/SMS when the label is `위험`.

## Key differences among archival sources

| Subject | Submitted code/SQL | Personal report and presentation | Evidence-based interpretation |
|---|---|---|---|
| Processing pause | `delay = 15` | `delay = 10` in report | Different archived revisions; no measured sustained 1-second inference claim |
| Density threshold | `<=2` safe, `2<x<4` warning, `>=4` danger | Presentation describes a different 1–5 scale | Use code values only when describing this specific source version |
| Density computation | `people_num / total_area` | Planned adjustment for obstacles | Obstacle adjustment not present in submitted execution path |
| Change metric | SQL upload uses percentage relative to prior value | Report final SQL uses absolute difference | Uploaded SQL is a historic variant, not proven deployed schema |
| Alert delivery | Twilio and WAV call paths present | Field test never reached danger; later screenshot shows received Twilio trial SMS with danger wording | **SMS receipt verified**; camera-triggered end-to-end delivery and exact sending process remain unverified |

## Known technical gaps

- `main.py` runs 100 iterations and sleeps the full configured delay *after* processing, rather than subtracting execution time from the interval.
- `database/schema_legacy_percent.sql` joins `current.id = previous.id + 1` even though camera IDs may interleave, so the immediately preceding row may not belong to the same camera.
- The percentage expression does not explicitly handle a previous density of zero.
- PHP query endpoints fetch latest records without selecting a specific camera, so multi-camera displays could be mixed.
- The `cameras` table must contain camera 1 before inserts using the default FK value can succeed; the supplied SQL does not create that row or a database/schema namespace.
- The original browser-side AJAX SMS function used `127.0.0.1:5000` and depended on Flask `app.py`, which is not present. The historical call is disabled in this public copy and **not a working SMS integration**.
- Local paths such as `/home/pi/project/image/` and `/var/www/html/tensorflow/` are environment-specific.
- Original Nginx service configuration and TFLite model files are not in the archive.

## Verification level

**Code implemented:** Python/PHP source, DB/VIEW, MJPEG serving, audio/SMS call paths.

**Documented and witnessed in historic materials:** Nginx/MariaDB setup screens; desktop and VNC screens; periodic recognition display; status/graph updates on manually injected DB values; risk modal output; **multiple received danger-alert SMS via Twilio trial account**, confirmed by a later-supplied phone screenshot ([details](sms-receipt-evidence-2023.md)).

**Not independently verified:** currently runnable build, live field camera danger-to-SMS/warning chain (the SMS receipt screenshot does not establish what triggered it), USB speaker output in that event, real-world camera density accuracy, actual model identity from source alone, original contributor-level authorship for each file.
