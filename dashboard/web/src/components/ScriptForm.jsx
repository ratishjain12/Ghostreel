import { useState } from "react";
import { api } from "../api";

export default function ScriptForm({ initial, lockName, submitLabel, onDone, onCancel }) {
  const [form, setForm] = useState(initial);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  async function submit(e) {
    e.preventDefault();
    setError(null);
    setSaving(true);
    try {
      await api.createScript(form);
      onDone();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="script-form" onSubmit={submit}>
      <label>
        Name (kebab-case)
        <input value={form.name} onChange={set("name")} placeholder="my-topic" required disabled={lockName} />
      </label>
      <label>
        Narration text
        <textarea value={form.text} onChange={set("text")} rows={6} placeholder="Sentence-punctuated narration..." required />
      </label>
      <div className="row">
        <label>
          Caption
          <textarea
            value={form.message}
            onChange={set("message")}
            rows={4}
            placeholder="leave blank to use the script's first sentence — line breaks are preserved"
          />
        </label>
        <label>
          Aspect
          <select value={form.aspect} onChange={set("aspect")}>
            <option value="">default (1080x1920, reels)</option>
            <option value="1080x1080">1080x1080 (square)</option>
            <option value="1920x1080">1920x1080 (landscape)</option>
          </select>
        </label>
      </div>
      {error && <p className="error-text">{error}</p>}
      <div className="form-actions">
        <button type="submit" disabled={saving}>
          {saving ? "Saving…" : submitLabel}
        </button>
        {onCancel && (
          <button type="button" className="ghost" onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
