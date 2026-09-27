---
name: thirds-brand-kit
description: Set up or change a thirds.ai brand kit with a customer's own logo, colours, fonts, and tone through the thirds.ai MCP server.
---

# Set up a thirds.ai brand kit

Use this skill when the user wants one brand across their PDFs and images. The brand kit holds their logo, colours, fonts, and tone. Read the [brand kit guide](https://thirds.ai/docs/design-a-template#set-up-your-brand-kit) for the product steps.

The work uses the [thirds.ai MCP server](https://thirds.ai/docs/mcp). If it is absent, help the user connect it with their API key in their client's secret store. Never ask them to paste the key in chat or a file you publish. A skill cannot connect the server by itself.

1. Ask for the brand name and the brand details the user wants to use. Use only assets they provide or own. Do not make up a logo, colour, or font.
2. Call `list_brand_kits` if the user may already have a kit. Its result shows IDs and dates, not the kit's content. Do not claim that you read a logo or colour from that result.
3. Call `create_brand_kit` with `name` and any supplied `colours` or `tone_guidance`. For changes, call `update_brand_kit` with `brand_kit_id` and the fields to change. Read the live tool schema for each field's shape.
4. For each supplied logo or font, call `set_brand_asset` with `brand_kit_id`, `media_type`, and base64 file bytes. It accepts still PNG, JPEG, or WebP images and WOFF2 fonts. It does not accept SVG. Keep the bytes and asset IDs private. Use `asset_id` only when the user wants to replace that asset.
5. Report the kit ID and the details you sent. Explain that the user can select this kit when they make a template. Do not claim that changing a kit changes an already saved template version.

For a first design, open a [gallery template](https://thirds.ai/gallery) in the editor. If the user wants an AI draft, use the [create-template skill](https://github.com/thirdsai/skills/tree/main/skills/thirds-create-template) after the kit exists.
