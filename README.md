# thirds.ai skills

These nine skills help an AI agent make branded PDFs and images with [thirds.ai](https://thirds.ai). A skill guides the task. The [MCP server](https://thirds.ai/docs/mcp) or [REST API](https://thirds.ai/docs/api) does the work.

## Install

Install the full library:

```sh
npx skills add https://github.com/thirdsai/skills
```

Or install one complete skill:

```sh
npx skills add https://github.com/thirdsai/skills --skill thirds
```

In Claude Code, add the plugin. It installs every skill and the thirds.ai MCP server:

```sh
/plugin marketplace add thirdsai/skills
/plugin install thirds-ai@thirds-ai
```

Each skill works when installed alone. Pick the task you need:

| Skill | Task | Interface |
| --- | --- | --- |
| [thirds](skills/thirds/SKILL.md) | Make a one-off file or choose a file workflow. | MCP, with REST for missing tools |
| [thirds-brand-kit](skills/thirds-brand-kit/SKILL.md) | Save your logo, colours, fonts, and tone. | MCP |
| [thirds-create-template](skills/thirds-create-template/SKILL.md) | Make or revise an editable design from a gallery design, HTML, words, or an image. | MCP or REST |
| [thirds-reuse-template](skills/thirds-reuse-template/SKILL.md) | Fill a saved design with new details. | MCP |
| [thirds-batch-files](skills/thirds-batch-files/SKILL.md) | Make one file per spreadsheet row. | MCP |
| [thirds-image-packs](skills/thirds-image-packs/SKILL.md) | Adapt one design to several image sizes. | MCP or REST |
| [thirds-carousels](skills/thirds-carousels/SKILL.md) | Export chosen slides in order. | MCP or REST |
| [thirds-ai-image](skills/thirds-ai-image/SKILL.md) | Make a reusable picture asset with AI. | MCP or REST |
| [thirds-api-workflows](skills/thirds-api-workflows/SKILL.md) | Add safe file creation to an app. | REST |

Connect your agent to `https://thirds.ai/mcp` with a private thirds.ai API key before using MCP. Follow the [setup guide](https://thirds.ai/docs/mcp) for your client. Keep the key in its secret store. A skill install does not create an authenticated connection.

## Your data

The skills run in your agent. They send nothing on their own. When your agent uses the thirds.ai MCP server or API, it sends what the task needs to thirds.ai: your template HTML, the data you fill in, brand kit colours, logos, and fonts, and any images you upload. thirds.ai uses them to make your files and keeps them in your account. The [privacy policy](https://thirds.ai/privacy) explains what we keep, for how long, and how to delete it.

The [Python](examples/render_saved_template.py) and [Node](examples/render_saved_template.mjs) examples show one REST request for a saved PDF. Set `THIRDS_API_KEY` in your private environment. Replace the sample template ID, data, and idempotency key.

```sh
python3 -m pip install requests
python3 examples/render_saved_template.py

# Or use Node.js 18 or newer:
node examples/render_saved_template.mjs
```

Each example prints the job ID and status. If it is still running, [check and download the job](https://thirds.ai/docs/retry-and-download). Reuse the same key and data after a lost response. Choose a new key for a new file.

The [public API contract](https://thirds.ai/v1/openapi.json) owns current REST fields. Check your connected MCP server's tool catalog before you start. Each skill gives the REST route for a tool your client cannot use.

## License

MIT. See [LICENSE](LICENSE).
