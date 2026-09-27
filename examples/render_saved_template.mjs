// Make one PDF from a saved thirds.ai template and JSON data.
import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";

const origin = "https://thirds.ai";
const [templateId, dataFile, outputFile, requestKey] = process.argv.slice(2);
const apiKey = process.env.THIRDS_API_KEY;

if (!/^tpl_[0-9a-f]{32}$/.test(templateId ?? "") || !dataFile || !outputFile || !requestKey || !apiKey) {
  console.error("Usage: THIRDS_API_KEY=... node render_saved_template.mjs <template-id> <data.json> <output.pdf> <idempotency-key>");
  process.exit(2);
}

async function request(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    redirect: "manual",
    signal: AbortSignal.timeout(30000),
  });
  if (!response.ok) throw new Error("Request failed.");
  return response;
}

async function api(path, options = {}) {
  const response = await request(new URL(path, origin), {
    ...options,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      Accept: "application/json",
      ...(options.body ? { "Content-Type": "application/json", "Idempotency-Key": requestKey } : {}),
    },
  });
  return response.json();
}

try {
  const data = JSON.parse(await readFile(dataFile, "utf8"));
  if (data === null || typeof data !== "object" || Array.isArray(data)) {
    throw new Error("The data file must hold one JSON object.");
  }

  let job = await api("/v1/pdf", {
    method: "POST",
    body: JSON.stringify({ template_id: templateId, data, wait: false }),
  });
  const deadline = performance.now() + 120000;
  while (job.status === "queued" || job.status === "running") {
    const remaining = deadline - performance.now();
    if (remaining <= 0) throw new Error("The render is still running. Check the same job later.");
    await new Promise((resolve) => setTimeout(resolve, Math.min(2000, remaining)));
    job = await api(`/v1/pdf/${job.id}`);
  }
  if (job.status !== "succeeded") throw new Error("The render did not succeed.");

  const downloadUrl = new URL(job.download.url, origin);
  if (downloadUrl.protocol !== "https:" || downloadUrl.host !== new URL(origin).host) {
    throw new Error("The download host did not match thirds.ai.");
  }
  const pdf = Buffer.from(await (await request(downloadUrl)).arrayBuffer());
  if (
    !pdf.subarray(0, 5).equals(Buffer.from("%PDF-")) ||
    pdf.length !== job.artifact.byte_size ||
    createHash("sha256").update(pdf).digest("hex") !== job.artifact.sha256
  ) {
    throw new Error("The PDF did not match the finished job.");
  }
  await writeFile(outputFile, pdf);
  console.log(`Saved ${outputFile} from render ${job.id}.`);
} catch {
  // The API may return private data. Do not print a response or signed URL.
  console.error("Render failed. Check the input, key, and job state.");
  process.exitCode = 1;
}
