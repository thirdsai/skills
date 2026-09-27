---
name: thirds-carousels
description: Export selected pages of a thirds.ai design as ordered branded slide images and a checked ZIP archive.
---

# Make carousel slides

Connect [MCP](https://thirds.ai/docs/mcp) and look for `get_template_version` and `create_carousel`. The [carousel guide](https://thirds.ai/docs/carousels), [carousel API](https://thirds.ai/docs/api-reference/carousels), and [OpenAPI contract](https://thirds.ai/v1/openapi.json) own the current rules. If a needed MCP tool is absent, use its authenticated REST route. If neither interface is available, hand off to the editor's Images ZIP export.

1. Read the full saved version. Get its `data-thirds-page` IDs, source, schema, and canvas size. A template list does not include them. Ask which pages and order the user wants; never invent page IDs. Collect shared data and check that the same brand and size work across slides.
2. State one credit per successful slide. Use the user's approval for the set or ask if missing. Call `create_carousel` with `idempotency_key`, `template_id`, optional `version` and `data`, `format` (`png`, `jpeg`, or `webp`), and `pages` in requested order. The API accepts 1 to 100 distinct known page IDs. Retry a lost response with the same key and body.
3. Poll `get_status` for the carousel ID, or `GET /v1/carousels/{id}`, under a wall-clock deadline. Check each slide state and stable error code. Download the private archive, inspect numbered filenames, `manifest.json`, dimensions, actual order, text, and images. On `partial`, report what finished and what failed. `retry_carousel` or `POST /v1/carousels/{id}/retry` retries failed slides only within the approved cost. Read status again for a fresh archive link if needed.

A PDF of selected pages is a separate `render`/`POST /v1/pdf` request with `pages`; it costs one successful-file credit. The carousel skill delivers slide images unless the user asks for a PDF. It does not publish to a social network.

Example request: “Export cover, offer, and action in that order for Northgate Studio.” Expected result: three inspected slide images and a ZIP whose manifest preserves that order.

See the [public source](https://github.com/thirdsai/skills/tree/main/skills/thirds-carousels).
