---
name: thirds-reuse-template
description: Fill a saved thirds.ai template with new values and deliver an inspected PDF or image through MCP.
---

# Make a file from a saved design

Connect [MCP](https://thirds.ai/docs/mcp) and check `list_templates`. Keep credentials and signed links private. The [template guide](https://thirds.ai/docs/templates-with-data) explains data fields; the [OpenAPI contract](https://thirds.ai/v1/openapi.json) owns request details.

1. Find the saved `template_id` with `list_templates` using `q` or `tag`. Let the user choose if several match. The list has names and versions, not source or schema. Read the full version with `get_template_version` when available, or `GET /v1/templates/{template_id}/versions/{version}` with authorized HTTP. If neither read is available, ask for the required fields instead of guessing.
2. Collect the real client name, date, amount, photos, and other required values. Choose `pdf`, `png`, `jpeg`, or `webp`. Ask for the intended image size when it matters. Image dimensions are optional and default to 1280 × 720 pixels. Set `request.image.width` and `request.image.height` to the design's intended canvas size unless that default is correct. Use `version` when the user needs one exact design. An omitted version resolves the latest saved version when the job starts.
3. State the one-credit successful-file cost. Use the user's existing approval for this file, or ask if missing. Call `render` with `output`, a new `idempotency_key`, and `request.template_id`, `request.data`, optional `request.version`, and image or PDF options as needed. If the response is lost, retry the identical request with the same key.
4. Poll `get_status` under a wall-clock deadline. Read state and stable error codes. On success, download before `download.expires_at`. If the link expires, read status again for a fresh link while the artifact remains. Inspect actual text, page count or pixels, clipping, and image loading. Report a failure with its code; correct input before a new paid attempt.

Example request: “Use my monthly report design for Northgate Studio's September figures.” Expected result: one PDF with the supplied figures and no clipped text.

See the [download guide](https://thirds.ai/docs/retry-and-download), [public source](https://github.com/thirdsai/skills/tree/main/skills/thirds-reuse-template), and [skill listing](https://skills.sh/thirdsai/skills/thirds-reuse-template).
