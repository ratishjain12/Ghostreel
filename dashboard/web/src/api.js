async function request(path, opts) {
  const res = await fetch(path, opts);
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `${res.status} ${res.statusText}`);
  }
  return res.status === 204 ? null : res.json();
}

export const api = {
  listScripts: () => request("/api/scripts"),
  createScript: (body) =>
    request("/api/scripts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  deleteScript: (name) => request(`/api/scripts/${name}`, { method: "DELETE" }),
  generate: (names) =>
    request("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ names }),
    }),
  render: (name) =>
    request("/api/render", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }),
  author: (name) =>
    request("/api/author", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }),
  generatePdf: (name) =>
    request("/api/generate-pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }),
  upload: (name) =>
    request("/api/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }),
  setTrigger: (name, mediaId, keyword) =>
    request("/api/set-trigger", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, media_id: mediaId, keyword }),
    }),
  publish: (name, caption, keyword) =>
    request("/api/publish", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, caption, keyword }),
    }),
  jobStatus: (jobId, since) => request(`/api/jobs/${jobId}?since=${since}`),
  listVideos: () => request("/api/videos"),
};
