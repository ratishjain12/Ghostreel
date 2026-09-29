import { useState } from "react";
import { api } from "../api";
import { PILLARS, HOOK_STYLES } from "../growthTags";

export default function CarouselForm({ initial, lockName, submitLabel, onDone, onCancel }) {
  const [form, setForm] = useState(initial);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  async function submit(e) {
    e.preventDefault();
    setError(null);
    setSaving(true);
    try {
      await api.createCarousel({ ...form, slide_count: Number(form.slide_count) });
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
        Outline
        <textarea value={form.text} onChange={set("text")} rows={6} placeholder="One idea per line/slide..." required />
      </label>
      <div className="row">
        <label>
          Caption
          <textarea
            value={form.message}
            onChange={set("message")}
            rows={4}
            placeholder="leave blank to use the outline's first sentence"
          />
        </label>
        <label>
          Slide count
          <input type="number" min={2} max={10} value={form.slide_count} onChange={set("slide_count")} required />
        </label>
      </div>
      <div className="row">
        <label>
          Pillar
          <select value={form.pillar || ""} onChange={set("pillar")}>
            <option value="">untagged</option>
            {PILLARS.map((p) => (
              <option key={p.value} value={p.value}>
                {p.label}
              </option>
            ))}
          </select>
        </label>
        <label>
          Hook style
          <select value={form.hook_style || ""} onChange={set("hook_style")}>
            <option value="">untagged</option>
            {HOOK_STYLES.map((h) => (
              <option key={h.value} value={h.value}>
                {h.label}
              </option>
            ))}
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
