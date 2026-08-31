import { useEffect, useMemo, useRef } from "react";

const MARKER = /^=== (.+) ===$/;

export default function JobLog({ status, lines, total }) {
  const preRef = useRef(null);

  useEffect(() => {
    if (preRef.current) preRef.current.scrollTop = preRef.current.scrollHeight;
  }, [lines]);

  const progress = useMemo(() => {
    if (!total) return null;
    let count = 0;
    let current = null;
    for (const line of lines) {
      const m = MARKER.exec(line);
      if (m) {
        count++;
        current = m[1];
      }
    }
    return count ? { count, current } : null;
  }, [lines, total]);

  return (
    <section className="panel" id="job-panel">
      <div className="panel-head">
        <p className="eyebrow">Job log</p>
        <span className={`job-status-badge ${status}`}>{status}</span>
      </div>
      {progress && (
        <p className="progress-line">
          {progress.count}/{total} — <strong>{progress.current}</strong>
        </p>
      )}
      <pre ref={preRef} id="job-log">
        {lines.length ? lines.join("\n") : <span className="placeholder">Nothing running. Trigger a generate or render to see output here.</span>}
      </pre>
    </section>
  );
}
