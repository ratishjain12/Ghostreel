import { useEffect, useState, useCallback, useMemo } from "react";
import { api } from "../api";
import { useJobRunner } from "../hooks/useJobRunner";
import { pillarLabel, hookStyleLabel } from "../growthTags";

const COLUMNS = [
  { key: "reach", label: "Reach" },
  { key: "views", label: "Views" },
  { key: "likes", label: "Likes" },
  { key: "comments", label: "Comments" },
  { key: "saved", label: "Saved" },
  { key: "shares", label: "Shares" },
  { key: "engagement", label: "Eng. rate" },
  { key: "saveRate", label: "Save rate" },
  { key: "delivered", label: "Guide sent" },
];

function formatDate(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

function engagementRate(post) {
  const reach = post.metrics?.reach || 0;
  const interactions = post.metrics?.total_interactions || 0;
  if (!reach) return 0;
  return (interactions / reach) * 100;
}

// The real proxy for follow-intent: Instagram's API has no metric for "new followers
// from this post" (the `follows` field that exists is the account's cumulative total,
// not per-post attribution). profile_visits looked like the closest real proxy, but the
// live Graph API rejects it for this account's Reels ("does not support the
// profile_visits metric for this media product type") — confirmed by actually calling
// it, not just reading docs. saved/reach is the real, available signal instead: saves
// are Instagram's own stated strongest ranking signal, and it's genuine per-post data.
function saveRate(post) {
  const reach = post.metrics?.reach || 0;
  const saved = post.metrics?.saved;
  if (!reach || saved == null) return null;
  return (saved / reach) * 100;
}

function sortValue(post, key) {
  if (key === "engagement") return engagementRate(post);
  if (key === "saveRate") return saveRate(post) ?? -1;
  if (key === "delivered") return post.trigger?.delivered || 0;
  return post.metrics?.[key] || 0;
}

function FollowerHistory() {
  const [history, setHistory] = useState([]);
  const [logging, setLogging] = useState(false);
  const [error, setError] = useState(null);

  const load = useCallback(() => api.followerHistory().then(setHistory), []);

  useEffect(() => {
    load();
  }, [load]);

  async function logToday() {
    setLogging(true);
    setError(null);
    try {
      await api.growthSnapshot();
      await load();
    } catch (err) {
      setError(err.message);
    } finally {
      setLogging(false);
    }
  }

  const rows = [...history].reverse();

  return (
    <section className="panel" id="follower-history-panel">
      <div className="panel-head">
        <p className="eyebrow">Follower history</p>
        <button className="ghost" onClick={logToday} disabled={logging}>
          {logging ? "Logging…" : "Log today's follower count"}
        </button>
      </div>
      {error && <p className="error-text">{error}</p>}
      {!rows.length && <p className="empty-state">No snapshots logged yet — click the button above periodically to build a trend.</p>}
      {rows.length > 0 && (
        <div className="follower-history-list">
          {rows.map((row, i) => {
            const prev = rows[i + 1];
            const delta = prev ? row.followers_count - prev.followers_count : null;
            return (
              <div key={row.date} className="follower-history-row">
                <span className="fh-date">{row.date}</span>
                <span className="fh-count">{row.followers_count.toLocaleString()}</span>
                {delta !== null && (
                  <span className={`fh-delta ${delta > 0 ? "up" : delta < 0 ? "down" : ""}`}>
                    {delta > 0 ? "+" : ""}
                    {delta}
                  </span>
                )}
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}

const TOKEN_WARN_DAYS = 14;

function TokenRow({ label, token, action }) {
  if (!token) return null;
  const days = token.days_left;
  const warn = !token.ok || (days != null && days < TOKEN_WARN_DAYS);
  const status = !token.ok ? token.error || "invalid" : days == null ? "never expires" : `${Math.floor(days)} days left`;
  return (
    <div className="follower-history-row">
      <span className="fh-date">{label}</span>
      <span className={`fh-delta ${warn ? "down" : "up"}`}>{status}</span>
      {action}
    </div>
  );
}

function TokenHealth() {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.tokenStatus().then(setStatus).catch((err) => setError(err.message));
  }, []);

  const reconnect = () => {
    window.location.href = `/api/fb/connect?return_to=${encodeURIComponent(window.location.href)}`;
  };

  return (
    <section className="panel" id="token-health-panel">
      <div className="panel-head">
        <p className="eyebrow">Meta tokens</p>
      </div>
      {error && <p className="error-text">{error}</p>}
      {status && (
        <div className="follower-history-list">
          <TokenRow label="Instagram (posting, auto-refreshed weekly)" token={status.instagram} />
          <TokenRow
            label="Competitor research (re-login every ~90 days)"
            token={status.competitor}
            action={
              status.reconnect_configured ? (
                <button className="ghost" onClick={reconnect}>Reconnect Facebook</button>
              ) : (
                <span className="empty-state">set FB_LOGIN_CONFIG_ID in .env to enable reconnect</span>
              )
            }
          />
        </div>
      )}
    </section>
  );
}

function GrowthAnalysis() {
  const job = useJobRunner();
  const [report, setReport] = useState(null);

  const loadReport = useCallback(() => api.latestGrowthAnalysis().then(setReport), []);

  useEffect(() => {
    loadReport();
  }, [loadReport]);

  async function run() {
    const result = await job.run(() => api.growthAnalyze(7));
    if (result?.status === "done") loadReport();
  }

  return (
    <section className="panel" id="growth-analysis-panel">
      <div className="panel-head">
        <p className="eyebrow">Growth analysis</p>
        <button className="ghost" onClick={run} disabled={job.status === "running"}>
          {job.status === "running" ? `Running… (${job.lines.length} lines)` : "Run growth analysis (last 7 days)"}
        </button>
      </div>
      <p className="empty-state">
        Reads recent posts' pillar/hook tags + metrics + follower trend, writes growth/analysis-latest.md, which future Author
        runs read as context for new content.
      </p>
      {job.status === "error" && <p className="error-text">Analysis failed — check the last log lines below.</p>}
      {job.status === "running" && job.lines.length > 0 && <pre className="growth-job-log">{job.lines.slice(-6).join("\n")}</pre>}
      {report ? (
        <pre className="growth-report">{report}</pre>
      ) : (
        <p className="empty-state">No analysis yet — run one above once you have a few tagged, published posts.</p>
      )}
    </section>
  );
}

export default function PerformancePanel() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortKey, setSortKey] = useState("reach");

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    return api
      .listInsights()
      .then(setPosts)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const sorted = useMemo(() => [...posts].sort((a, b) => sortValue(b, sortKey) - sortValue(a, sortKey)), [posts, sortKey]);

  const totals = useMemo(() => {
    return posts.reduce(
      (acc, p) => ({
        reach: acc.reach + (p.metrics?.reach || 0),
        matched: acc.matched + (p.trigger?.matched || 0),
        delivered: acc.delivered + (p.trigger?.delivered || 0),
      }),
      { reach: 0, matched: 0, delivered: 0 }
    );
  }, [posts]);

  return (
    <div className="performance-stack">
      <TokenHealth />
      <section className="panel" id="performance-panel">
        <div className="panel-head">
          <p className="eyebrow">Performance ({posts.length})</p>
          <div className="actions">
            <button className="ghost" onClick={load} disabled={loading}>
              {loading ? "Refreshing…" : "Refresh"}
            </button>
          </div>
        </div>

        {error && <p className="error-text">{error}</p>}

        {!error && !loading && posts.length === 0 && (
          <p className="empty-state">No published posts yet — insights show up here once something's live on Instagram.</p>
        )}

        {posts.length > 0 && (
          <>
            <div className="perf-summary">
              <div className="perf-stat">
                <span className="perf-stat-value">{totals.reach.toLocaleString()}</span>
                <span className="perf-stat-label">total reach</span>
              </div>
              <div className="perf-stat">
                <span className="perf-stat-value">{totals.matched}</span>
                <span className="perf-stat-label">triggers matched</span>
              </div>
              <div className="perf-stat">
                <span className="perf-stat-value">
                  {totals.delivered}
                  {totals.matched > 0 && <span className="perf-stat-pct"> ({Math.round((totals.delivered / totals.matched) * 100)}%)</span>}
                </span>
                <span className="perf-stat-label">guides delivered</span>
              </div>
            </div>

            <div className="perf-table-wrap">
              <table className="perf-table">
                <thead>
                  <tr>
                    <th className="perf-col-post">Post</th>
                    <th>Pillar</th>
                    <th>Hook</th>
                    {COLUMNS.map((col) => (
                      <th key={col.key} className={sortKey === col.key ? "sorted" : ""} onClick={() => setSortKey(col.key)}>
                        {col.label}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {sorted.map((post) => {
                    const matched = post.trigger?.matched || 0;
                    const delivered = post.trigger?.delivered || 0;
                    const sr = saveRate(post);
                    return (
                      <tr key={post.media_id}>
                        <td className="perf-col-post">
                          <a href={post.permalink || undefined} target="_blank" rel="noreferrer" className="perf-post-name" title={post.caption || post.name}>
                            {post.name}
                          </a>
                          <span className="perf-post-date">{formatDate(post.published_at)}</span>
                          {post.error && <span className="perf-post-error" title={post.error}>⚠ insights unavailable</span>}
                        </td>
                        <td>{pillarLabel(post.pillar) || "—"}</td>
                        <td>{hookStyleLabel(post.hook_style) || "—"}</td>
                        <td>{(post.metrics?.reach ?? "—").toLocaleString?.() ?? "—"}</td>
                        <td>{(post.metrics?.views ?? "—").toLocaleString?.() ?? "—"}</td>
                        <td>{post.metrics?.likes ?? "—"}</td>
                        <td>{post.metrics?.comments ?? "—"}</td>
                        <td>{post.metrics?.saved ?? "—"}</td>
                        <td>{post.metrics?.shares ?? "—"}</td>
                        <td>{post.metrics ? `${engagementRate(post).toFixed(1)}%` : "—"}</td>
                        <td>{sr == null ? "—" : `${sr.toFixed(1)}%`}</td>
                        <td>
                          {delivered}
                          {matched > 0 && <span className="perf-conv-pct">/{matched}</span>}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </>
        )}
      </section>

      <FollowerHistory />
      <GrowthAnalysis />
    </div>
  );
}
