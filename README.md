# thirds.ai skills

These skills help an AI agent make branded PDFs and images with [thirds.ai](https://thirds.ai). A skill guides the work. The [thirds.ai MCP server](https://thirds.ai/docs/mcp) provides the tools that do it.

## Install

Install the full library:

```sh
npx skills add https://github.com/thirdsai/skills
```

Or install one skill:

```sh
npx skills add https://github.com/thirdsai/skills --skill thirds-brand-kit
```

| Skill | Use it when you want to |
| --- | --- |
| [thirds-brand-kit](skills/thirds-brand-kit/SKILL.md) | Set up your logo, colours, fonts, and tone. |
| [thirds-create-template](skills/thirds-create-template/SKILL.md) | Make an editable design from a gallery template, HTML, words, or an image. |
| [thirds-reuse-template](skills/thirds-reuse-template/SKILL.md) | Fill a saved design with new details and get a PDF or image. |
| [thirds-batch-files](skills/thirds-batch-files/SKILL.md) | Make one file per row from a saved design. |

Connect your agent to `https://thirds.ai/mcp` with a private thirds.ai API key before you use an MCP skill. Follow the [MCP setup guide](https://thirds.ai/docs/mcp) for your client. Keep the key in your client's secret store.

The [Python](examples/render_saved_template.py) and [Node](examples/render_saved_template.mjs) examples show the REST API call for one PDF. They use the same saved templates and credits as MCP. Set `THIRDS_API_KEY` in your private environment. Replace the template ID, data, and idempotency key in the example you choose.

```sh
python3 -m pip install requests
python3 examples/render_saved_template.py

# Or use Node.js 18 or newer:
node examples/render_saved_template.mjs
```

Each example prints the render job ID and status. If the file is still running, [check and download the job](https://thirds.ai/docs/retry-and-download). Reuse the same idempotency key and data if a response is lost. Choose a new key for a new file.

Skills do not install MCP or spend credits by themselves. The agent connects with your key, shows the cost before paid work, and keeps each signed file link private.

## License

MIT. See [LICENSE](LICENSE).
