# Historical Twilio SMS receipt evidence (2023)

> **Evidence type:** Personal screenshot of a phone's SMS conversation, supplied after the original 2023 source/report/video analysis. The screenshot is intentionally **not published** because it contains a telephone number and potentially sensitive message metadata.

## What the screenshot actually shows
- Multiple received SMS messages bearing the Twilio trial-account preamble.
- Message body: `명지대학교 골목1, 위험수준 [위험]` (Myongji University Alley 1, risk level [Danger]).
- At least ten visible messages in the conversation, including one under the date separator **2023-06-05 (Monday)** at **17:25**; other messages show times around 03:35–03:44, but the screenshot alone does not establish their calendar date.
- The text format is consistent with the message composed in historical `alarm.py`, which uses Twilio's API to send danger-state alerts.

## Revised verification
| Feature | Evidence-based conclusion |
|---|---|
| Twilio SMS delivery | **Received SMS verified from historical phone screenshot** |
| Danger-state wording | **Verified in the received body** |
| Multiple notifications | **Verified in screenshot** |
| Source of danger value (camera measurement vs manual DB insert) | **Not established** |
| Exact sending process (`alarm.py`, browser/Flask, manual test) | **Not established solely by screenshot** |
| End-to-end live crowd hazard detection → SMS | **Not verified** |
| USB speaker WAV playback | **Not verified by this screenshot** |

Repeated messages are consistent with the historical polling behavior when a danger value remains in the database, but their root cause is **not proven** by the screenshot. The archival design should avoid unwanted duplicate notifications when revisited.

For privacy, keep the original screenshot in a private evidence folder and share a redacted copy only after removing the phone number and any other identifiable information.
