import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";

const origin = "https://thirds.ai";
const [templateId, dataPath, outputPath, retryKey] = process.argv.slice(2);
const apiKey = process.env.THIRDS_API_KEY;

if (!templateId || !dataPath || !outputPath || !retryKey || !apiKey) {
  console.error("Usage: node render_saved_template.mjs TEMPLATE_ID data.json output.pdf RETRY_KEY");
  process.exit(2);
}

async function api(path, options = {}) {
  const response = await fetch(`${origin}${path}`, {
    ...options,
    redirect: "manual",
    signal: AbortSignal.timeout(30_000),
    headers: { Authorization: `Bearer ${apiKey}`, ...options.headers },
  });
  if (!response.ok) throw new Error("API request failed");
  return response.json();
}

async function main() {
  const data = JSON.parse(await readFile(dataPath, "utf8"));
  const body = JSON.stringify({ template_id: templateId, data });
  let job = await api("/v1/pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json", "Idempotency-Key": retryKey },
    body,
  });

  const deadline = performance.now() + 120_000;
  while (job.status === "queued" || job.status === "running") {
    if (performance.now() >= deadline) throw new Error("Render timed out");
    await new Promise((resolve) => setTimeout(resolve, 2_000));
    job = await api(`/v1/pdf/${job.id}`);
  }
  if (job.status !== "succeeded") throw new Error("Render failed");

  const url = new URL(job.download.url, origin);
  if (url.origin !== origin) throw new Error("Unexpected download host");
  const response = await fetch(url, { redirect: "manual", signal: AbortSignal.timeout(30_000) });
  if (!response.ok) throw new Error("Download failed");
  const pdf = Buffer.from(await response.arrayBuffer());
  const hash = createHash("sha256").update(pdf).digest("hex");
  if (pdf.length !== job.artifact.byte_size || hash !== job.artifact.sha256) {
    throw new Error("Downloaded file did not match the render");
  }

  await writeFile(outputPath, pdf);
  console.log(`Saved ${outputPath}`);
}

main().catch(() => {
  // A signed download URL or API response may hold private data.
  console.error("Could not save the PDF. Check the key, template, data, and job.");
  process.exitCode = 1;
});
