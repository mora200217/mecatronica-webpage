import { useEffect, useRef, useState } from "react";

const REDUCED = "(prefers-reduced-motion: reduce)";

function useCountUp(target, kind, run) {
  const [value, setValue] = useState(() => (kind === "year" ? target : 0));

  useEffect(() => {
    if (!run) return undefined;
    if (window.matchMedia(REDUCED).matches) {
      setValue(target);
      return undefined;
    }
    // Los años arrancan una década atrás; los conteos, desde cero.
    const from = kind === "year" ? target - 12 : 0;
    const duration = 900;
    const start = performance.now();
    let frame = 0;

    const step = (now) => {
      const t = Math.min((now - start) / duration, 1);
      const eased = 1 - (1 - t) ** 3;
      setValue(Math.round(from + (target - from) * eased));
      if (t < 1) frame = requestAnimationFrame(step);
    };

    frame = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frame);
  }, [target, kind, run]);

  return value;
}

function Stat({ stat, run }) {
  const value = useCountUp(stat.value, stat.kind, run);
  const shown = stat.kind === "year" ? String(value) : value.toLocaleString("es-CO");

  return (
    <article className="stat-card">
      <b>{shown}</b>
      <p className="stat-label">{stat.label}</p>
      <p className="muted stat-detail">{stat.detail}</p>
    </article>
  );
}

export default function StatGrid({ stats }) {
  const ref = useRef(null);
  const [run, setRun] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return undefined;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          setRun(true);
          observer.disconnect();
        }
      },
      { threshold: 0.25 },
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  return (
    <div className="stat-grid" ref={ref}>
      {stats.map((stat) => (
        <Stat key={stat.id} stat={stat} run={run} />
      ))}
    </div>
  );
}
