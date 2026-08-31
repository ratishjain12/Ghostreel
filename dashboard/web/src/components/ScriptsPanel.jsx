import { useState, useMemo } from "react";
import ScriptRow from "./ScriptRow";
import NewScriptForm from "./NewScriptForm";
import { api } from "../api";

export default function ScriptsPanel({ scripts, onChanged, onGenerate, onAuthor, onRender, onGeneratePdf, onSetTrigger, onPublish }) {
  const [selected, setSelected] = useState(new Set());
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return scripts;
    return scripts.filter((s) => s.name.toLowerCase().includes(q) || s.text.toLowerCase().includes(q) || (s.meta.message || "").toLowerCase().includes(q));
  }, [scripts, query]);

  const allFilteredSelected = filtered.length > 0 && filtered.every((s) => selected.has(s.name));

  function toggle(name) {
    setSelected((prev) => {
      const next = new Set(prev);
      next.has(name) ? next.delete(name) : next.add(name);
      return next;
    });
  }

  function toggleAll() {
    setSelected((prev) => {
      const next = new Set(prev);
      filtered.forEach((s) => (allFilteredSelected ? next.delete(s.name) : next.add(s.name)));
      return next;
    });
  }

  async function remove(name) {
    if (!confirm(`Delete script "${name}"? Audio and video files already generated are kept.`)) return;
    await api.deleteScript(name);
    setSelected((prev) => {
      const next = new Set(prev);
      next.delete(name);
      return next;
    });
    onChanged();
  }

  return (
    <section className="panel" id="scripts-panel">
      <div className="panel-head">
        <p className="eyebrow">Scripts ({scripts.length})</p>
        <div className="actions">
          <button
            className="ghost"
            onClick={() => {
              if (!selected.size) return alert("Select at least one script first.");
              onGenerate([...selected]);
            }}
          >
            Generate selected{selected.size ? ` (${selected.size})` : ""}
          </button>
          <button onClick={() => onGenerate(null)}>Generate all</button>
        </div>
      </div>

      {scripts.length > 0 && (
        <div className="list-controls">
          <input className="search" type="search" placeholder="Filter by name, text, or message…" value={query} onChange={(e) => setQuery(e.target.value)} />
          <label className="select-all">
            <input type="checkbox" className="channel-toggle" checked={allFilteredSelected} onChange={toggleAll} disabled={!filtered.length} />
            Select all
          </label>
        </div>
      )}

      <div className="scripts-list">
        {!scripts.length && <p className="empty-state">No scripts loaded yet — add one below.</p>}
        {scripts.length > 0 && !filtered.length && <p className="empty-state">No scripts match “{query}”.</p>}
        {filtered.map((s) => (
          <ScriptRow
            key={s.name}
            script={s}
            selected={selected.has(s.name)}
            onToggle={() => toggle(s.name)}
            onAuthor={() => onAuthor(s.name)}
            onRender={() => onRender(s.name)}
            onDelete={() => remove(s.name)}
            onChanged={onChanged}
            onGeneratePdf={() => onGeneratePdf(s.name)}
            onSetTrigger={(mediaId, keyword) => onSetTrigger(s.name, mediaId, keyword)}
            onPublish={(caption, keyword) => onPublish(s.name, caption, keyword)}
          />
        ))}
      </div>

      <NewScriptForm onCreated={onChanged} />
    </section>
  );
}
