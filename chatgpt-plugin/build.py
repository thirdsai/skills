#!/usr/bin/env python3
"""Check the ChatGPT plugin package and build /tmp/thirds-chatgpt-plugin.zip.

The skills come from ../skills at build time, so the package never holds a
second copy. Run from any directory: python3 chatgpt-plugin/build.py
"""

import json
import re
import struct
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parent / "skills"
OUT = Path("/tmp/thirds-chatgpt-plugin.zip")

# Skills that work through an OAuth MCP connection. thirds-ai-image needs the
# AI image tools, which an OAuth connection does not get. thirds-api-workflows
# is for REST calls from the customer's own app.
PLUGIN_SKILLS = [
    "thirds",
    "thirds-brand-kit",
    "thirds-create-template",
    "thirds-reuse-template",
    "thirds-batch-files",
    "thirds-image-packs",
    "thirds-carousels",
]

# The tools the production MCP server gives an OAuth connection.
MCP_TOOLS = {
    "create_brand_kit", "update_brand_kit", "set_brand_asset", "list_brand_kits",
    "create_template", "edit_template", "publish_template", "cancel_template_message",
    "list_templates", "save_template", "render", "create_batch", "retry_batch",
    "cancel_batch", "get_status", "get_brand_kit", "get_brand_asset", "get_template",
    "get_template_version", "save_template_version", "preview_template",
    "adapt_template", "upload_image_asset", "get_image_asset", "create_image_pack",
    "retry_image_pack", "create_carousel", "retry_carousel", "list_gallery_templates",
    "get_gallery_template",
}

# Text that must never ship. The owner's private identity is kept out of this
# public file on purpose, so the check looks for the shapes of a leak instead.
LEAK_PATTERNS = [
    r"/home/", r"/Users/", r"~/", r"@gmail\.", r"[A-Za-z0-9._%+-]+@(?!thirds\.ai)[A-Za-z0-9.-]+\.[a-z]{2,}",
    r"github\.com/(?!thirdsai/)", r"mj\.ms", r"Marketing Suite",
]

errors = []


def check(ok, message):
    if not ok:
        errors.append(message)


def text_limit(value, limit, label):
    check(isinstance(value, str) and value.strip(), f"{label} is missing")
    if isinstance(value, str):
        check(len(value) <= limit, f"{label} has {len(value)} characters, limit {limit}")
        check(not re.search(r"[\x00-\x08\x0b-\x1f\x7f]", value), f"{label} has a control character")


def luminance(hex_colour):
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a, b):
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def image_size(path):
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8X":
            return (int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1)
        if chunk == b"VP8L":
            bits = int.from_bytes(data[21:25], "little")
            return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
        if chunk == b"VP8 ":
            return (int.from_bytes(data[26:28], "little") & 0x3FFF, int.from_bytes(data[28:30], "little") & 0x3FFF)
    raise ValueError(f"{path.name} is not a PNG or WebP file")


def asset(ref, label, square):
    check(isinstance(ref, str) and ref.startswith("./assets/"), f"{label} must start with ./assets/")
    path = HERE / ref
    if not path.is_file():
        errors.append(f"{label} file {ref} is missing")
        return
    check(path.stat().st_size <= 5 * 1024 * 1024, f"{label} is over 5 MiB")
    width, height = image_size(path)
    if square:
        check(width == height, f"{label} is {width}x{height}, not square")
        check(48 <= width <= 4096, f"{label} is {width} px, outside 48 to 4096")


manifest = json.loads((HERE / "plugin.json").read_text())
mcp = json.loads((HERE / "mcp.json").read_text())

name = manifest.get("name", "")
check(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64, "name must be lowercase with hyphens, at most 64")
check(manifest.get("version") == "1.0.0", "version must be 1.0.0")
text_limit(manifest.get("description"), 4000, "description")
text_limit(manifest.get("author", {}).get("name"), 80, "author.name")
check(manifest.get("author", {}).get("name") == "thirds.ai", "author.name must be thirds.ai")

openai = manifest.get("extensions", {}).get("com.openai", {})
check(set(openai) <= {"interface", "review", "publication"}, f"unexpected com.openai keys: {sorted(set(openai) - {'interface', 'review', 'publication'})}")
ui = openai.get("interface", {})
text_limit(ui.get("displayName"), 30, "displayName")
text_limit(ui.get("shortDescription"), 30, "shortDescription")
text_limit(ui.get("longDescription"), 4000, "longDescription")
text_limit(ui.get("developerName"), 80, "developerName")
check(ui.get("developerName") == "thirds.ai", "developerName must be thirds.ai")
text_limit(ui.get("category"), 80, "category")

capabilities = ui.get("capabilities", [])
check(1 <= len(capabilities) <= 20, f"capabilities has {len(capabilities)} items, limit 20")
for i, item in enumerate(capabilities):
    text_limit(item, 120, f"capabilities[{i}]")

for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
    url = ui.get(key, "")
    check(url.startswith("https://") and len(url) <= 1024, f"{key} must be an https URL of at most 1024 characters")

prompts = ui.get("defaultPrompt", [])
check(1 <= len(prompts) <= 3, f"defaultPrompt has {len(prompts)} items, limit 3")
for i, prompt in enumerate(prompts):
    text_limit(prompt, 128, f"defaultPrompt[{i}]")

for key, background in (("brandColor", "#FFFFFF"), ("brandColorDark", "#212121")):
    colour = ui.get(key, "")
    if re.fullmatch(r"#[0-9A-Fa-f]{6}", colour):
        ratio = contrast(colour, background)
        check(ratio >= 2, f"{key} {colour} has {ratio:.2f}:1 contrast against {background}, needs 2:1")
    else:
        errors.append(f"{key} must be #RRGGBB")

for key in ("composerIcon", "composerIconDark", "logo", "logoDark"):
    asset(ui.get(key), key, square=True)
for i, ref in enumerate(ui.get("screenshots", [])):
    asset(ref, f"screenshots[{i}]", square=False)

review = openai.get("review", {})
cases = review.get("test_cases", {})
positive, negative = cases.get("positive", []), cases.get("negative", [])
check(len(positive) == 5, f"{len(positive)} positive test cases, need 5")
check(len(negative) == 3, f"{len(negative)} negative test cases, need 3")
for i, case in enumerate(positive):
    for key in ("description", "prompt", "expected_behavior"):
        text_limit(case.get(key), 4000, f"positive[{i}].{key}")
    tools = case.get("tools_triggered", [])
    check(tools and set(tools) <= MCP_TOOLS, f"positive[{i}] names unknown tools: {sorted(set(tools) - MCP_TOOLS)}")
for i, case in enumerate(negative):
    for key in ("description", "prompt"):
        text_limit(case.get(key), 4000, f"negative[{i}].{key}")
check("demo_recording_url" in review, "review.demo_recording_url is missing")
check(review.get("commerce") is False, "review.commerce must be false")
check(not {"test_credentials", "reviewer_instructions"} & set(review), "review must not hold credentials or reviewer instructions")
text_limit(openai.get("publication", {}).get("release_notes"), 4000, "release_notes")

server = mcp.get("mcpServers", {}).get("thirds", {})
check(server == {"type": "streamable-http", "url": "https://thirds.ai/mcp"}, "mcp.json must point thirds at https://thirds.ai/mcp")
check(len(mcp.get("mcpServers", {})) == 1, "mcp.json must hold one server")

# The package source may not hold app references or lifecycle hooks.
for banned in (".app.json", "hooks", ".codex-plugin"):
    check(not (HERE / banned).exists(), f"{banned} must not be in the package")
check('"apps"' not in json.dumps(openai) and '"hooks"' not in json.dumps(openai), "com.openai must not reference apps or hooks")

files = {
    "plugin.json": HERE / "plugin.json",
    "mcp.json": HERE / "mcp.json",
}
for path in sorted((HERE / "assets").iterdir()):
    files[f"assets/{path.name}"] = path
for skill in PLUGIN_SKILLS:
    path = SKILLS / skill / "SKILL.md"
    front = re.match(r"---\nname: (.+)\ndescription: (.+)\n---\n", path.read_text())
    check(front and front.group(1) == skill, f"{skill}/SKILL.md front matter name does not match")
    files[f"skills/{skill}/SKILL.md"] = path

for arcname, path in files.items():
    if path.suffix in {".json", ".md"}:
        body = path.read_text()
        for pattern in LEAK_PATTERNS:
            for hit in re.findall(pattern, body):
                errors.append(f"{arcname} has a possible privacy leak: {hit!r}")

if errors:
    print("Package check failed:", *errors, sep="\n- ")
    sys.exit(1)

OUT.unlink(missing_ok=True)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as archive:
    for arcname, path in files.items():
        archive.write(path, arcname)

print(f"Package check passed. Wrote {OUT} with {len(files)} files:")
for arcname in files:
    print(f"  {arcname}")
