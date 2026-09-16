import { useCallback, useEffect, useState } from "react";

export default function Gallery({ items }) {
  const [open, setOpen] = useState(null);

  const move = useCallback(
    (delta) => {
      setOpen((current) => {
        if (current === null) return current;
        return (current + delta + items.length) % items.length;
      });
    },
    [items.length],
  );

  useEffect(() => {
    if (open === null) return undefined;
    const onKey = (event) => {
      if (event.key === "Escape") setOpen(null);
      if (event.key === "ArrowRight") move(1);
      if (event.key === "ArrowLeft") move(-1);
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, move]);

  const shown = open === null ? null : items[open];

  return (
    <>
      <div className="gallery">
        {items.map((item, index) => (
          <button
            key={item.src}
            type="button"
            className="gallery-item"
            onClick={() => setOpen(index)}
            aria-label={`Ampliar: ${item.title}`}
          >
            <img src={item.src} alt={item.title} loading="lazy" />
            <span className="gallery-cap">
              <strong>{item.title}</strong>
              <em>{item.caption}</em>
            </span>
          </button>
        ))}
      </div>

      {shown ? (
        <div
          className="lightbox"
          role="dialog"
          aria-modal="true"
          aria-label={shown.title}
          onClick={() => setOpen(null)}
        >
          <figure className="lightbox-figure" onClick={(event) => event.stopPropagation()}>
            <img src={shown.src} alt={shown.title} />
            <figcaption>
              <div>
                <strong>{shown.title}</strong>
                <p className="muted">{shown.caption}</p>
                <p className="meta">Foto: {shown.credit}</p>
              </div>
              <div className="lightbox-nav">
                <button type="button" className="btn btn-ghost" onClick={() => move(-1)}>
                  ←
                </button>
                <span className="muted">
                  {open + 1} / {items.length}
                </span>
                <button type="button" className="btn btn-ghost" onClick={() => move(1)}>
                  →
                </button>
              </div>
            </figcaption>
          </figure>
          <button
            type="button"
            className="lightbox-close"
            onClick={() => setOpen(null)}
            aria-label="Cerrar"
          >
            ×
          </button>
        </div>
      ) : null}
    </>
  );
}
