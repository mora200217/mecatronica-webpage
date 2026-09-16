import { useEffect, useMemo, useRef, useState } from "react";

export default function Timeline({ items, eras }) {
  const [era, setEra] = useState("todas");
  const [active, setActive] = useState(0);
  const railRef = useRef(null);
  const buttonRefs = useRef([]);

  const visible = useMemo(
    () => (era === "todas" ? items : items.filter((item) => item.era === era)),
    [items, era],
  );

  useEffect(() => {
    setActive(0);
  }, [era]);

  const current = visible[Math.min(active, visible.length - 1)];

  const focusIndex = (index) => {
    const next = Math.max(0, Math.min(index, visible.length - 1));
    setActive(next);
    const node = buttonRefs.current[next];
    if (node) {
      node.focus();
      node.scrollIntoView({ block: "nearest", inline: "center", behavior: "smooth" });
    }
  };

  const onKeyDown = (event) => {
    if (event.key === "ArrowRight") {
      event.preventDefault();
      focusIndex(active + 1);
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      focusIndex(active - 1);
    } else if (event.key === "Home") {
      event.preventDefault();
      focusIndex(0);
    } else if (event.key === "End") {
      event.preventDefault();
      focusIndex(visible.length - 1);
    }
  };

  if (!current) return null;

  const progress = visible.length > 1 ? (active / (visible.length - 1)) * 100 : 100;

  return (
    <section className="tl">
      <div className="tl-filters" role="group" aria-label="Filtrar la línea de tiempo por época">
        <button
          type="button"
          className={era === "todas" ? "chip chip-on" : "chip"}
          aria-pressed={era === "todas"}
          onClick={() => setEra("todas")}
        >
          Todo <span className="chip-note">1997 – 2026</span>
        </button>
        {eras.map((item) => (
          <button
            key={item.id}
            type="button"
            className={era === item.id ? "chip chip-on" : "chip"}
            aria-pressed={era === item.id}
            onClick={() => setEra(item.id)}
          >
            {item.label} <span className="chip-note">{item.range}</span>
          </button>
        ))}
      </div>

      <div className="tl-rail-wrap">
        <div className="tl-track" aria-hidden="true">
          <span className="tl-track-fill" style={{ width: `${progress}%` }} />
        </div>
        <div
          className="tl-rail"
          role="tablist"
          aria-label="Hitos de la carrera"
          ref={railRef}
          onKeyDown={onKeyDown}
        >
          {visible.map((item, index) => (
            <button
              key={item.year}
              type="button"
              role="tab"
              id={`tl-tab-${index}`}
              aria-selected={index === active}
              aria-controls="tl-panel"
              tabIndex={index === active ? 0 : -1}
              ref={(node) => {
                buttonRefs.current[index] = node;
              }}
              className={index === active ? "tl-dot tl-dot-on" : "tl-dot"}
              onClick={() => setActive(index)}
            >
              <span className="tl-bullet" aria-hidden="true" />
              <span className="tl-year">{item.year}</span>
            </button>
          ))}
        </div>
      </div>

      <article
        className="tl-panel"
        id="tl-panel"
        role="tabpanel"
        aria-labelledby={`tl-tab-${active}`}
        key={current.year}
      >
        <div className="tl-panel-body">
          <p className="kicker">
            {current.year} · {eras.find((item) => item.id === current.era)?.label}
          </p>
          <h3>{current.title}</h3>
          <p>{current.body}</p>
          <div className="tl-tags">
            {current.tags.map((tag) => (
              <span key={tag} className="tag">
                {tag}
              </span>
            ))}
          </div>
          <div className="tl-nav">
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => focusIndex(active - 1)}
              disabled={active === 0}
            >
              ← Anterior
            </button>
            <span className="muted tl-counter">
              {active + 1} / {visible.length}
            </span>
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => focusIndex(active + 1)}
              disabled={active === visible.length - 1}
            >
              Siguiente →
            </button>
          </div>
        </div>
        <aside className="tl-panel-side">
          <img src={current.image} alt="" />
          <div className="tl-figure">
            <b>{current.figure.value}</b>
            <span>{current.figure.label}</span>
          </div>
        </aside>
      </article>
    </section>
  );
}
