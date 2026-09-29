import { useEffect, useState, useCallback, useMemo } from "react";
import { api } from "../api";
import ScheduleForm from "./ScheduleForm";

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function startOfMonth(date) {
  return new Date(date.getFullYear(), date.getMonth(), 1);
}

function dateKey(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function buildGrid(monthDate) {
  const first = startOfMonth(monthDate);
  const gridStart = new Date(first);
  gridStart.setDate(first.getDate() - first.getDay());
  return Array.from({ length: 42 }, (_, i) => {
    const d = new Date(gridStart);
    d.setDate(gridStart.getDate() + i);
    return d;
  });
}

export default function SchedulePanel({ scripts }) {
  const [month, setMonth] = useState(() => startOfMonth(new Date()));
  const [schedule, setSchedule] = useState([]);
  const [formState, setFormState] = useState(null); // { date, item } | null
  const [configError, setConfigError] = useState(null);

  const load = useCallback(
    () =>
      api
        .listSchedule()
        .then((items) => {
          setSchedule(items);
          setConfigError(null);
        })
        .catch((err) => setConfigError(err.message)),
    []
  );

  useEffect(() => {
    load();
    const id = setInterval(load, 15000);
    return () => clearInterval(id);
  }, [load]);

  const byDay = useMemo(() => {
    const map = new Map();
    for (const item of schedule) {
      const key = item.scheduled_at.slice(0, 10);
      if (!map.has(key)) map.set(key, []);
      map.get(key).push(item);
    }
    for (const list of map.values()) list.sort((a, b) => a.scheduled_at.localeCompare(b.scheduled_at));
    return map;
  }, [schedule]);

  const days = useMemo(() => buildGrid(month), [month]);
  const publishable = useMemo(() => scripts.filter((s) => s.hasPdf && s.renders.length > 0 && s.hasUploaded), [scripts]);
  const todayKey = dateKey(new Date());

  function openNew(day) {
    if (!publishable.length) return;
    setFormState({ date: day, item: null });
  }

  async function handleSave(payload, editingId) {
    if (editingId) {
      await api.updateSchedule(editingId, payload);
    } else {
      await api.createSchedule(payload);
    }
    setFormState(null);
    load();
  }

  async function handleDelete(id) {
    if (!confirm("Cancel this scheduled post?")) return;
    await api.deleteSchedule(id);
    setFormState(null);
    load();
  }

  return (
    <section className="panel" id="schedule-panel">
      <div className="panel-head">
        <p className="eyebrow">Schedule</p>
        <div className="actions calendar-nav">
          <button className="ghost" onClick={() => setMonth((m) => new Date(m.getFullYear(), m.getMonth() - 1, 1))}>
            ←
          </button>
          <span className="month-label">{month.toLocaleDateString(undefined, { month: "long", year: "numeric" })}</span>
          <button className="ghost" onClick={() => setMonth((m) => new Date(m.getFullYear(), m.getMonth() + 1, 1))}>
            →
          </button>
          <button
            disabled={!publishable.length}
            title={publishable.length ? "" : "No project is ready to schedule yet — generate a PDF guide, render it, and upload it first"}
            onClick={() => openNew(todayKey)}
          >
            Schedule a post
          </button>
        </div>
      </div>

      {configError && <p className="error-text">{configError}</p>}

      {!configError && !publishable.length && (
        <p className="empty-state">
          No project is ready to schedule yet — generate a PDF guide, render, and upload it on the Pipeline tab first.
        </p>
      )}

      <div className="calendar-grid">
        {WEEKDAYS.map((d) => (
          <div key={d} className="calendar-weekday">
            {d}
          </div>
        ))}
        {days.map((d) => {
          const key = dateKey(d);
          const items = byDay.get(key) || [];
          return (
            <div key={key} className={`calendar-cell ${d.getMonth() === month.getMonth() ? "" : "outside"} ${key === todayKey ? "today" : ""}`}>
              <div className="cell-head">
                <span className="cell-date">{d.getDate()}</span>
                <button
                  className="cell-add"
                  title="Schedule a post on this day"
                  disabled={!publishable.length}
                  onClick={() => openNew(key)}
                >
                  +
                </button>
              </div>
              <div className="cell-items">
                {items.map((item) => (
                  <button
                    key={item.id}
                    className={`schedule-chip status-${item.status}`}
                    title={item.error || item.name}
                    onClick={() => setFormState({ date: key, item })}
                  >
                    <span className="chip-time">{item.scheduled_at.slice(11, 16)}</span>
                    <span className="chip-name">{item.name}</span>
                  </button>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {formState && (
        <ScheduleForm
          date={formState.date}
          item={formState.item}
          scripts={publishable}
          onCancel={() => setFormState(null)}
          onSave={handleSave}
          onDelete={formState.item ? () => handleDelete(formState.item.id) : null}
        />
      )}
    </section>
  );
}
