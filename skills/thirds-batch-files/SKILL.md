---
name: thirds-batch-files
description: Make a PDF or image for each data row from one saved thirds.ai template with the MCP batch tools.
---

# Make a batch of branded files

Use this skill when one saved thirds.ai design must make a file for each person, product, or event. The [batch guide](https://thirds.ai/docs/batch-renders) explains the CSV and file flow. The [MCP guide](https://thirds.ai/docs/mcp) explains connection and credit approval. If MCP is absent, help the user connect it with a private API key. Keep the key and signed archive link private.

1. Get the saved `template_id`. Use `list_templates` if the user does not know it. Gather one JSON object per file. If the user supplies CSV, parse it in your own work first: `create_batch` accepts JSON rows, not CSV text. Let the user check the mapped fields and row count.
2. Choose `pdf`, `png`, `jpeg`, or `webp`. Pin a `version` when the user needs the same layout across runs. If omitted, thirds.ai pins the latest version when it accepts the batch.
3. Show the row count and expected credit cost before `create_batch`, then get the user's instruction to start. Each successful file costs one credit; failed and cancelled rows cost nothing. The account plan sets the row limit. Read the live tool schema and current [billing guide](https://thirds.ai/docs/billing) for limits.
4. Call `create_batch` with `template_id`, `format`, `rows`, an optional `version`, and a new `idempotency_key`. Keep the same key and exact arguments if the response is lost. A new key can start another billed batch.
5. Poll `get_status` under a time deadline. Stop at `complete`, `partial`, `failed`, or `cancelled`. On a result with files, give the user the private archive link and check its manifest or output before you call the task done. Call `retry_batch` for failed rows only when the user asks. Call `cancel_batch` if they ask to stop pending work; running rows can still finish.

The web app's Batches page can take CSV directly. Use that path when the user wants to paste a spreadsheet without an agent.
