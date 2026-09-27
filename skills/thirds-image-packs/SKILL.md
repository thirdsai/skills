---
name: thirds-image-packs
description: Adapt one thirds.ai design to several sizes and deliver an inspected PNG, JPEG, or WebP image pack.
---

# Make an image pack

Connect [MCP](https://thirds.ai/docs/mcp) and check the live tool catalog for `get_template_version`, `adapt_template`, and `create_image_pack`. Keep credentials and signed links private. When a tool is absent, use the matching authenticated REST route in the [image pack API](https://thirds.ai/docs/api-reference/image-packs) and [OpenAPI contract](https://thirds.ai/v1/openapi.json). If the client cannot call either interface, hand off to the editor's size export.

1. Get the saved template ID and full version. A list does not show source or sizes. Collect the user's data and target sizes. `sizes` accepts 1 to 20 distinct values: `original`, a saved size ID, a preset slug, or `WxH` custom size. A custom size adapts the editable source; merely changing image export pixels does not check the layout.
2. For new custom sizes, use `adapt_template` with `source` and `sizes` objects of `width` and `height` to check each adaptation for free. Inspect text bounds, crops, logos, and safe space at each size. Fix the design or choose a saved size when adaptation fails.
3. State one credit per successful size. Use the user's approval for this pack or ask if missing. Call `create_image_pack` with `idempotency_key`, `template_id`, optional `version` and `data`, `format`, and ordered `sizes`. Retry a lost response with the same key and body.
4. Poll `get_status` for the pack ID, or `GET /v1/image-packs/{id}`, under a wall-clock deadline. Read every member state and code. Download the private `archive_url` and inspect `manifest.json`, file dimensions, order, and layout. On `partial`, report the successful sizes and failed sizes separately. `retry_image_pack` or `POST /v1/image-packs/{id}/retry` retries only failed members when the approved cost covers it. Read status again for a fresh archive link if needed.

Example request: “Make my offer in square, story, and wide sizes.” Expected result: three checked images or an exact partial result with a ZIP manifest.

See the [size guide](https://thirds.ai/docs/pdf-and-image-options) and [public source](https://github.com/thirdsai/skills/tree/main/skills/thirds-image-packs).
