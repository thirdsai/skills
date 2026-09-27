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

The [Python example](examples/render_saved_template.py) and [Node example](examples/render_saved_template.mjs) show how to make one PDF with the REST API. They use the same saved templates and credits as MCP. Save your fields as a JSON object, set `THIRDS_API_KEY` in your private environment, then run one:

```sh
python3 examples/render_saved_template.py \
  tpl_00000000000000000000000000000000 data.json report.pdf \
  --idempotency-key report-2026-09

node examples/render_saved_template.mjs \
  tpl_00000000000000000000000000000000 data.json report.pdf \
  report-2026-09
```

Replace the sample ID and key. Reuse the same key and arguments if a response is lost. Choose a new key for a new file.

Skills do not install MCP or spend credits by themselves. The agent connects with your key, shows the cost before paid work, and keeps each signed file link private.

## License

MIT. See [LICENSE](LICENSE).
