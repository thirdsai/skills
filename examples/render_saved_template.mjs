// Start a PDF from a saved thirds.ai template.
const response = await fetch("https://thirds.ai/v1/pdf", {
  method: "POST",
  redirect: "manual",
  headers: {
    Authorization: `Bearer ${process.env.THIRDS_API_KEY}`,
    "Content-Type": "application/json",
    "Idempotency-Key": "report-2026-09",
  },
  body: JSON.stringify({
    template_id: "tpl_00000000000000000000000000000000",
    data: { client: "Northgate Studio", title: "September report" },
  }),
});
if (![200, 202].includes(response.status)) {
  throw new Error("PDF request failed");
}

const job = await response.json();
console.log(job.id, job.status);
