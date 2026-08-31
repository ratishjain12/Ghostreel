export default function VideosPanel({ projects, onRefresh }) {
  return (
    <section className="panel" id="videos-panel">
      <div className="panel-head">
        <p className="eyebrow">Videos</p>
        <button className="subtle" onClick={onRefresh}>
          Refresh
        </button>
      </div>
      <div className="videos-grid">
        {!projects.length && <p className="empty-state">Nothing rendered yet — render a project to see it appear here.</p>}
        {projects.map((p) => (
          <div className="monitor" key={p.name}>
            <div className="screen">
              <video controls src={p.renders[0].url} />
            </div>
            <p className="name">{p.name}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
