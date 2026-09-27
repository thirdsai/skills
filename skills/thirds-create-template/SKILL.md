---
name: thirds-create-template
description: Make an editable thirds.ai PDF or image template from a gallery design, HTML, words, or a source image, then review it before saving.
---

# Make a thirds.ai template

Use this skill to make one design that the user can fill again. A template can make a PDF or a still image. Read [how to make a template](https://thirds.ai/docs/design-a-template) and [connect MCP](https://thirds.ai/docs/mcp) before you use the tools. If MCP is absent, help the user connect it with a private API key. Do not put that key in chat or source code.

Choose the start that fits the user's input:

- A [gallery design](https://thirds.ai/gallery) is ready to copy and edit in the web app. Use it when one already fits. The MCP tools do not copy gallery designs into an account.
- For the user's own HTML, call `save_template` with `source`. It saves a reusable template without an AI call. Add `name`, `schema`, and `tags` only when useful.
- For an AI draft from words, HTML, or an image, choose a brand kit first. Call `create_template` with `brand_kit_id`, a new `idempotency_key`, and `input`. Use `input.type` `prompt`, `html`, or `image`. An image must be a still PNG, JPEG, or WebP that the user has the right to use. The rebuild is editable and may differ from the source picture. It must use the user's brand, not the source brand.
- For the user's own marked template source, call `create_template` with `input.type: source`, `source`, and `sample_data` for every non-brand variable. This compile path uses no AI credits. It still needs a brand kit and an idempotency key.

Before an AI call, show the credit cost from the live tool schema and get the user's instruction to spend it. A new AI build reserves 50 credits. A later words or HTML edit reserves 25. Saving HTML without AI does not spend AI credits. Rendering a finished file costs one credit when it works. Keep the same idempotency key and exact arguments after a lost response; use a new key for new work.

For a build, keep the returned build ID. Poll `get_status` under a time deadline while the message runs. Read `message.state`, `failure_code`, and `repair_code`. Wait until `message.state` is `succeeded` and `current_draft` is true. Ask the user to review the result in the thirds.ai editor. Use `edit_template` only for a change they request, and show its cost first when it uses AI. Call `publish_template` only after the user clearly confirms that this draft can enter their reusable template library. A draft does not publish itself.

Return the saved template ID and version. For a finished PDF or image, use the [reuse-template skill](https://github.com/thirdsai/skills/tree/main/skills/thirds-reuse-template).
