import { useState } from "react";
import { firstSentence } from "../utils";

function splitDateTime(iso) {
  return { date: iso.slice(0, 10), time: iso.slice(11, 16) };
}

export default function ScheduleForm({ date, item, scripts, onCancel, onSave, onDelete }) {
  const initial = item ? splitDateTime(item.scheduled_at) : { date, time: "09:00" };
  const initialScript = !item ? scripts[0] : null;

  const [name, setName] = useState(item?.name || scripts[0]?.name || "");
  const [dateVal, setDateVal] = useState(initial.date);
  const [timeVal, setTimeVal] = useState(initial.time);
  const [caption, setCaption] = useState(item?.caption ?? initialScript?.meta.message ?? (initialScript ? firstSentence(initialScript.text) : "") ?? "");
  const [keyword, setKeyword] = useState(item?.keyword ?? initialScript?.trigger?.keyword ?? "");
  // A post with no trigger must stay that way — this toggle makes "no trigger" an
  // explicit choice instead of "did I forget to type a keyword", and submit always
  // sends keyword: null when it's off, regardless of whatever text is still typed in.
  const [hasTrigger, setHasTrigger] = useState(item ? Boolean(item.keyword) : Boolean(initialScript?.trigger?.keyword));
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const locked = item && item.status !== "pending" && item.status !== "error";

  function handleScriptChange(e) {
    const newName = e.target.value;
    setName(newName);
    const s = scripts.find((x) => x.name === newName);
    if (!s) return;
    setCaption((prev) => prev || s.meta.message || firstSentence(s.text));
    if (s.trigger?.keyword) {
      setKeyword(s.trigger.keyword);
      setHasTrigger(true);
    } else {
      setKeyword("");
      setHasTrigger(false);
    }
  }

  async function submit(e) {
    e.preventDefault();
    setError(null);
    if (!dateVal || !timeVal) {
      setError("Pick a date and time");
      return;
    }
    if (hasTrigger && !keyword.trim()) {
      setError("Enter a trigger keyword, or turn off the trigger toggle");
      return;
    }
    setSaving(true);
    try {
      const scheduled_at = `${dateVal}T${timeVal}:00`;
      const keywordValue = hasTrigger ? keyword.trim() : null;
      const payload = item
        ? { scheduled_at, caption: caption.trim() || null, keyword: keywordValue }
        : { name, scheduled_at, caption: caption.trim() || null, keyword: keywordValue };
      await onSave(payload, item?.id);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="modal-backdrop" onClick={onCancel}>
      <form className="schedule-form" onClick={(e) => e.stopPropagation()} onSubmit={submit}>
        <h3>{item ? `Edit "${item.name}"` : "Schedule a post"}</h3>

        {!item && (
          <label>
            Script
            <select value={name} onChange={handleScriptChange} required>
              {scripts.map((s) => (
                <option key={s.name} value={s.name}>
                  {s.name}
                </option>
              ))}
            </select>
          </label>
        )}

        <div className="row">
          <label>
            Date
            <input type="date" value={dateVal} onChange={(e) => setDateVal(e.target.value)} disabled={locked} required />
          </label>
          <label>
            Time
            <input type="time" value={timeVal} onChange={(e) => setTimeVal(e.target.value)} disabled={locked} required />
          </label>
        </div>

        <label>
          Caption
          <textarea
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            rows={4}
            placeholder="leave blank to use the script's caption"
            disabled={locked}
          />
        </label>

        <label className="checkbox-label">
          <input type="checkbox" checked={hasTrigger} onChange={(e) => setHasTrigger(e.target.checked)} disabled={locked} />
          Register a comment trigger for this post
        </label>
        {hasTrigger && (
          <label>
            Trigger keyword
            <input value={keyword} onChange={(e) => setKeyword(e.target.value)} placeholder="e.g. guide" disabled={locked} required />
          </label>
        )}

        {item && item.status !== "pending" && (
          <p className={`schedule-status status-${item.status}`}>
            Status: {item.status}
            {item.error ? ` — ${item.error}` : ""}
          </p>
        )}

        {error && <p className="error-text">{error}</p>}

        <div className="form-actions">
          <button type="submit" disabled={saving || locked}>
            {saving ? "Saving…" : item ? "Save changes" : "Schedule"}
          </button>
          {onDelete && (
            <button type="button" className="subtle danger" onClick={onDelete}>
              Cancel post
            </button>
          )}
          <button type="button" className="ghost" onClick={onCancel}>
            Close
          </button>
        </div>
      </form>
    </div>
  );
}
