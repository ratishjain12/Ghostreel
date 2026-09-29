import { useState } from "react";
import CarouselForm from "./CarouselForm";
import CarouselPreview from "./CarouselPreview";
import { api } from "../api";
import { firstSentence } from "../utils";
import { pillarLabel, hookStyleLabel } from "../growthTags";

const STAGES = [
  { key: "txt", label: "TXT", done: () => true },
  { key: "prj", label: "PRJ", done: (c) => c.hasProject },
  { key: "sld", label: "SLD", done: (c) => c.slides.length > 0 },
  { key: "pub", label: "PUB", done: (c) => Boolean(c.published) },
];

export default function CarouselRow({ carousel, onAuthor, onDelete, onChanged }) {
  const [editing, setEditing] = useState(false);
  const [previewIndex, setPreviewIndex] = useState(null);

  if (editing) {
    return (
      <div className="channel-strip editing">
        <CarouselForm
          initial={{
            name: carousel.name,
            text: carousel.text,
            message: carousel.meta.message || "",
            slide_count: carousel.meta.slide_count || 6,
            pillar: carousel.meta.angle || "",
            hook_style: carousel.meta.hook_style || "",
          }}
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

  const message = carousel.meta.message || firstSentence(carousel.text);
  const pillar = pillarLabel(carousel.meta.angle);
  const hookStyle = hookStyleLabel(carousel.meta.hook_style);

  return (
    <div className="channel-strip">
      <div className="row-top">
        <span className="script-name">{carousel.name}</span>
        <div className="stage-chain">
          {STAGES.map((stage, i) => {
            const lit = stage.done(carousel);
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
        <span>“{message}”</span>
      </p>
      {(pillar || hookStyle) && (
        <p className="tag-line">
          {pillar && <span className="pillar-tag">{pillar}</span>}
          {hookStyle && <span className="hook-tag">{hookStyle}</span>}
        </p>
      )}
      <p className="text-preview">
        {carousel.text} — {carousel.meta.slide_count || 6} slides
      </p>

      <div className="row-actions">
        <button className="subtle" onClick={() => setEditing(true)}>
          Edit
        </button>
        <button className="subtle danger" onClick={onDelete}>
          Delete
        </button>
        <button
          className="ghost"
          disabled={!carousel.hasProject}
          title={carousel.hasProject ? "Spawn an agent to author this carousel's slides end-to-end (bypasses tool permissions — see docs)" : "Generate the project first"}
          onClick={onAuthor}
        >
          Author
        </button>
        {carousel.slides.length > 0 && (
          <button className="ghost" onClick={() => setPreviewIndex(0)}>
            Preview
          </button>
        )}
        {carousel.slides.length > 0 && (
          <button
            className="ghost"
            title="Open the slides folder in Finder so you can AirDrop them to your phone"
            onClick={() => api.revealCarousel(carousel.name).catch((err) => alert(`Couldn't open Finder: ${err.message}`))}
          >
            Reveal in Finder
          </button>
        )}
      </div>

      {carousel.slides.length > 0 && (
        <div className="slide-thumbs">
          {carousel.slides.map((url, i) => (
            <button key={url} className="slide-thumb" onClick={() => setPreviewIndex(i)}>
              <img src={url} alt={`${carousel.name} slide ${i + 1}`} />
            </button>
          ))}
        </div>
      )}

      {carousel.published && (
        <p className="text-preview">
          Posted {new Date(carousel.published.published_at).toLocaleDateString()} — linked via Sync, feeds into Performance/Growth.
        </p>
      )}

      {previewIndex !== null && (
        <CarouselPreview carousel={carousel} startIndex={previewIndex} onClose={() => setPreviewIndex(null)} />
      )}
    </div>
  );
}
