---
name: thirds-reuse-template
description: Fill a saved thirds.ai template with new data and make a branded PDF, PNG, JPEG, or WebP through MCP.
---

# Make a new file from a saved template

Use this skill when the user already has a design and wants another file from it. Connect the [thirds.ai MCP server](https://thirds.ai/docs/mcp) first. If it is absent, use that guide to connect it with a private API key. Keep the key and signed download links out of shared chats and source code.

1. Get the saved template ID. If it is missing, call `list_templates` with `q` or `tag`, then let the user choose if several designs match. The list gives IDs, names, and versions. It does not give the template's source or data fields.
2. Gather the values the design needs. Ask for a missing client name, date, price, or other field. Do not guess a real person's details. Use `version` when the user needs an exact saved design. If you omit it, thirds.ai pins the latest version when it accepts the render.
3. Show the output format and cost before the paid call. One successful file costs one credit. Call `render` with `output` set to `pdf`, `png`, `jpeg`, or `webp`; a new `idempotency_key`; and `request.template_id` plus `request.data`. For an image, set `request.image.width` and `request.image.height` as the live tool schema requires. `viewport` is for PDF only.
4. Keep the returned render ID. Poll `get_status` under a time deadline while the job is queued or running. Stop when it succeeds, fails, or is cancelled. Read `isError` and stable error codes. If the first response is lost, retry the same call with the same key and exact arguments.
5. On success, give the user the file or private download link. Download before `download.expires_at`. If it expires, call `get_status` for a fresh link. Check the finished file before you call the task done.

For many rows from one design, use the [batch-files skill](https://github.com/thirdsai/skills/tree/main/skills/thirds-batch-files). The [MCP guide](https://thirds.ai/docs/mcp#create-and-collect-an-output) has a full render request and status example.
