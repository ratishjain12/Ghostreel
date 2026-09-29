import { useState } from "react";
import { api } from "../api";
import CarouselRow from "./CarouselRow";
import NewCarouselForm from "./NewCarouselForm";

export default function CarouselPanel({ carousels, onChanged, onGenerate, onAuthor }) {
  const [syncing, setSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState(null);

  async function remove(name) {
    if (!confirm(`Delete carousel "${name}"? Slides already generated are kept.`)) return;
    await api.deleteCarousel(name);
    onChanged();
  }

  async function sync() {
    setSyncing(true);
    setSyncResult(null);
    try {
      const result = await api.syncCarouselsPublished();
      setSyncResult(result);
      if (result.matched.length) onChanged();
    } catch (err) {
      setSyncResult({ error: err.message });
    } finally {
      setSyncing(false);
    }
  }

  return (
    <section className="panel" id="carousel-panel">
      <div className="panel-head">
        <p className="eyebrow">Carousels ({carousels.length})</p>
        <div className="actions">
          <button
            className="ghost"
            onClick={sync}
            disabled={syncing}
            title="Matches locally-tracked carousels to your recent Instagram posts by caption — no media ID typing needed"
          >
            {syncing ? "Syncing…" : "Sync from Instagram"}
          </button>
          <button onClick={() => onGenerate(null)}>Generate all</button>
        </div>
      </div>

      {syncResult && !syncResult.error && !syncResult.matched.length && !syncResult.unmatched.length && (
        <p className="empty-state">All carousels are already linked to their Instagram posts. Nothing new to sync.</p>
      )}
      {syncResult && !syncResult.error && (syncResult.matched.length > 0 || syncResult.unmatched.length > 0) && (
        <p className="empty-state">
          Linked {syncResult.matched.length} post{syncResult.matched.length === 1 ? "" : "s"}
          {syncResult.matched.length > 0 && `: ${syncResult.matched.join(", ")}`}.
          {syncResult.unmatched.length > 0 && ` No caption match yet for: ${syncResult.unmatched.join(", ")}.`}
        </p>
      )}
      {syncResult?.error && <p className="error-text">{syncResult.error}</p>}

      <div className="scripts-list">
        {!carousels.length && <p className="empty-state">No carousels yet — add one below.</p>}
        {carousels.map((c) => (
          <CarouselRow key={c.name} carousel={c} onAuthor={() => onAuthor(c.name)} onDelete={() => remove(c.name)} onChanged={onChanged} />
        ))}
      </div>

      <NewCarouselForm onCreated={onChanged} />

      <p className="empty-state">
        Once slides are ready, save/AirDrop them from the thumbnails above onto your phone, start a
        new post in the Instagram app, and add music from Instagram's library there — that step
        can't be automated (no API for it), so it stays manual by design. Use the same caption
        shown on the card when you post, then click "Sync from Instagram" above to link it back
        automatically — no need to hunt down or paste a media ID.
      </p>
    </section>
  );
}
