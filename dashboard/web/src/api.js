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
  listCarousels: () => request("/api/carousels"),
  createCarousel: (body) =>
    request("/api/carousels", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  deleteCarousel: (name) => request(`/api/carousels/${name}`, { method: "DELETE" }),
  revealCarousel: (name) => request(`/api/carousels/${name}/reveal`, { method: "POST" }),
  syncCarouselsPublished: () => request("/api/carousels/sync-published", { method: "POST" }),
  generateCarousel: (names) =>
    request("/api/generate-carousel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ names }),
    }),
  authorCarousel: (name) =>
    request("/api/author-carousel", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }),
  listSchedule: () => request("/api/schedule"),
  createSchedule: (body) =>
    request("/api/schedule", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  updateSchedule: (id, body) =>
    request(`/api/schedule/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  deleteSchedule: (id) => request(`/api/schedule/${id}`, { method: "DELETE" }),
  listInsights: () => request("/api/insights"),
  tokenStatus: () => request("/api/tokens/status"),
  growthSnapshot: () => request("/api/growth/snapshot", { method: "POST" }),
  growthAnalyze: (days) =>
    request("/api/growth/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ days: days ?? 7 }),
    }),
  followerHistory: () =>
    fetch(`/growth-data/follower-history.json?t=${Date.now()}`).then((res) => (res.ok ? res.json() : [])),
  latestGrowthAnalysis: () =>
    fetch(`/growth-data/analysis-latest.md?t=${Date.now()}`).then((res) => (res.ok ? res.text() : null)),
};
