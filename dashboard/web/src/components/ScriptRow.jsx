import { useState } from "react";
import ScriptForm from "./ScriptForm";
import { firstSentence } from "../utils";

const STAGES = [
  { key: "txt", label: "TXT", done: () => true },
  { key: "vox", label: "VOX", done: (s) => s.hasAudio },
  { key: "cap", label: "CAP", done: (s) => s.hasCaptions },
  { key: "prj", label: "PRJ", done: (s) => s.hasProject },
  { key: "pdf", label: "PDF", done: (s) => s.hasPdf },
  { key: "ren", label: "REN", done: (s) => s.renders.length > 0 },
  { key: "upl", label: "UPL", done: (s) => s.hasUploaded },
  { key: "pub", label: "PUB", done: (s) => s.hasPublished },
];

export default function ScriptRow({ script, selected, onToggle, onAuthor, onRender, onDelete, onChanged, onGeneratePdf, onSetTrigger, onPublish }) {
  const [editing, setEditing] = useState(false);
  const [mediaId, setMediaId] = useState(script.trigger?.media_id || "");
  const [keyword, setKeyword] = useState(script.trigger?.keyword || "");

  if (editing) {
    return (
      <div className="channel-strip editing">
        <ScriptForm
          initial={{ name: script.name, text: script.text, message: script.meta.message || "", aspect: script.meta.aspect || "" }}
          lockName
          submitLabel="Save changes"
          onCancel={() => setEditing(false)}
          onDone={() => {
            setEditing(false);
            onChanged();
          }}
        />
      </div>
    );
  }

  const isOverride = Boolean(script.meta.message);
  const message = script.meta.message || firstSentence(script.text);
  const canPublish = script.hasPdf && script.renders.length > 0;

  function handlePublishClick() {
    if (!confirm(`Post this Reel to Instagram now, live and public?\n\nCaption:\n"${message}"`)) return;
    const kw = prompt("Trigger keyword for this post (leave blank to skip trigger registration):", script.trigger?.keyword || "");
    if (kw === null) return; // cancelled
    onPublish(message, kw.trim() || null);
  }

  return (
    <div className="channel-strip">
      <div className="row-top">
        <input type="checkbox" className="channel-toggle" checked={selected} onChange={onToggle} aria-label={`Select ${script.name}`} />
        <span className="script-name">{script.name}</span>
        <div className="stage-chain">
          {STAGES.map((stage, i) => {
            const lit = stage.done(script);
            return (
              <span key={stage.key} className="stage-item">
                {i > 0 && <span className="stage-wire" />}
                <span className={`stage ${lit ? "lit" : ""}`} title={lit ? `${stage.label} ready` : `${stage.label} pending`}>
                  <span className="lozenge" />
                  <label>{stage.label}</label>
                </span>
              </span>
            );
          })}
        </div>
      </div>

      <p className="message-line">
        {isOverride && <span className="override-tag">custom caption</span>}
        <span>“{message}”</span>
      </p>
      <p className="text-preview">{script.text}</p>

      <div className="row-actions">
        <button className="subtle" onClick={() => setEditing(true)}>
          Edit
        </button>
        <button className="subtle danger" onClick={onDelete}>
          Delete
        </button>
        <button
          className="ghost"
          disabled={!script.hasProject}
          title={script.hasProject ? "Spawn an agent to author this project's scenes end-to-end (bypasses tool permissions — see docs)" : "Generate the project first"}
          onClick={onAuthor}
        >
          Author
        </button>
        <button
          className="ghost"
          disabled={!script.hasProject}
          title={script.hasProject ? "Spawn an agent to write a PDF companion guide, then upload it to S3 (bypasses tool permissions — see docs)" : "Generate the project first"}
          onClick={onGeneratePdf}
        >
          PDF
        </button>
        <button className="ghost" disabled={!script.hasProject} title={script.hasProject ? "Render this project's composition to MP4" : "Generate the project first"} onClick={onRender}>
          Render
        </button>
        <button
          className="ghost"
          disabled={!canPublish}
          title={canPublish ? "Post this Reel to Instagram live, then register its comment trigger" : "Generate the PDF guide and render the project first"}
          onClick={handlePublishClick}
        >
          Approve &amp; Publish
        </button>
      </div>

      {script.hasPdf && script.pdfUrl && (
        <details className="pdf-preview">
          <summary>Preview PDF</summary>
          <iframe src={script.pdfUrl} title={`${script.name} guide PDF`} />
        </details>
      )}

      {script.hasUploaded && (
        <div className="trigger-form">
          <input placeholder="IG media ID" value={mediaId} onChange={(e) => setMediaId(e.target.value)} />
          <input placeholder="Trigger keyword" value={keyword} onChange={(e) => setKeyword(e.target.value)} />
          <button
            className="subtle"
            disabled={!mediaId.trim() || !keyword.trim()}
            onClick={() => onSetTrigger(mediaId.trim(), keyword.trim())}
          >
            Save trigger
          </button>
        </div>
      )}
    </div>
  );
}
