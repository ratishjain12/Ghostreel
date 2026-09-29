import { useCallback, useEffect, useState } from "react";

export default function CarouselPreview({ carousel, startIndex = 0, onClose }) {
  const slides = carousel.slides;
  const [index, setIndex] = useState(startIndex);

  const prev = useCallback(() => setIndex((i) => (i - 1 + slides.length) % slides.length), [slides.length]);
  const next = useCallback(() => setIndex((i) => (i + 1) % slides.length), [slides.length]);

  useEffect(() => {
    function onKey(e) {
      if (e.key === "ArrowLeft") prev();
      else if (e.key === "ArrowRight") next();
      else if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [prev, next, onClose]);

  if (!slides.length) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="carousel-preview" onClick={(e) => e.stopPropagation()}>
        <div className="carousel-preview-head">
          <span className="carousel-preview-name">{carousel.name}</span>
          <button className="ghost" onClick={onClose}>
            Close
          </button>
        </div>

        <div className="carousel-preview-frame">
          <img src={slides[index]} alt={`${carousel.name} slide ${index + 1}`} />
          {slides.length > 1 && (
            <>
              <button className="carousel-preview-nav prev" onClick={prev} aria-label="Previous slide">
                ‹
              </button>
              <button className="carousel-preview-nav next" onClick={next} aria-label="Next slide">
                ›
              </button>
            </>
          )}
          <span className="carousel-preview-counter">
            {index + 1} / {slides.length}
          </span>
        </div>

        {slides.length > 1 && (
          <div className="carousel-preview-dots">
            {slides.map((_, i) => (
              <button
                key={i}
                className={`carousel-preview-dot ${i === index ? "active" : ""}`}
                onClick={() => setIndex(i)}
                aria-label={`Go to slide ${i + 1}`}
              />
            ))}
          </div>
        )}

        {carousel.meta.message && <p className="carousel-preview-caption">{carousel.meta.message}</p>}
      </div>
    </div>
  );
}
