---
name: thirds
description: Use thirds.ai to make a one-off PDF or image with MCP, or find the right skill for a brand kit, reusable template, or batch.
---

# Make a file with thirds.ai

Use thirds.ai to make branded PDFs and still images. Start with the [MCP setup guide](https://thirds.ai/docs/mcp) if the server is not connected. Keep the API key in the client's secret store. A skill alone does not connect MCP.

Choose the task:

- Set up a logo, colours, fonts, or tone: use [thirds-brand-kit](https://github.com/thirdsai/skills/tree/main/skills/thirds-brand-kit).
- Make an editable design from words, HTML, an image, or the gallery: use [thirds-create-template](https://github.com/thirdsai/skills/tree/main/skills/thirds-create-template).
- Fill a saved design with new details: use [thirds-reuse-template](https://github.com/thirdsai/skills/tree/main/skills/thirds-reuse-template).
- Make one file for each data row: use [thirds-batch-files](https://github.com/thirdsai/skills/tree/main/skills/thirds-batch-files).

For a one-off file from the user's own HTML, call `render` with `request.html` and `output` set to `pdf`, `png`, `jpeg`, or `webp`. Set `request.image.width` and `request.image.height` for an image. Show the one-credit cost and get the user's instruction before the paid call. Use a new `idempotency_key` for a new file. If a response is lost, retry the same call with the same key and arguments.

Poll `get_status` under a time deadline until the render succeeds, fails, or is cancelled. A failed render costs no credit. Give the user the finished file or its private download link. Check the file before you say the work is done. The [MCP guide](https://thirds.ai/docs/mcp#create-and-collect-an-output) shows the render request and status flow.
