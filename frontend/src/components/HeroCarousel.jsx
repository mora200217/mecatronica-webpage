import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import BlockNav from "./BlockNav.jsx";

const INTERVAL = 6500;
const FIRST_SLIDE_INTERVAL = 11000;

export default function HeroCarousel({ slides }) {
  const [index, setIndex] = useState(0);
  // El botón de pausa es explícito; el hover y el foco solo congelan el avance.
  const [userPaused, setUserPaused] = useState(false);
  const [hovering, setHovering] = useState(false);

  const go = useCallback(
    (next) => setIndex((current) => (next + slides.length) % slides.length),
    [slides.length],
  );

  useEffect(() => {
    if (userPaused || hovering || slides.length < 2) return undefined;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return undefined;
    const wait = index === 0 ? FIRST_SLIDE_INTERVAL : INTERVAL;
    const timer = setTimeout(() => go(index + 1), wait);
    return () => clearTimeout(timer);
  }, [index, userPaused, hovering, go, slides.length]);

  const onKeyDown = (event) => {
    if (event.key === "ArrowRight") {
      event.preventDefault();
      go(index + 1);
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      go(index - 1);
    }
  };

  const slide = slides[index];

  return (
    <section
      className="hero hero-carousel"
      aria-roledescription="carrusel"
      aria-label="Destacados de Ingeniería Mecatrónica"
      onMouseEnter={() => setHovering(true)}
      onMouseLeave={() => setHovering(false)}
      onFocusCapture={() => setHovering(true)}
      onBlurCapture={() => setHovering(false)}
      onKeyDown={onKeyDown}
      tabIndex={-1}
    >
      {slides.map((item, i) => (
        <div
          key={item.image}
          className={i === index ? "hero-slide hero-slide-on" : "hero-slide"}
          style={{ backgroundImage: `url(${item.image})` }}
          aria-hidden={i !== index}
        />
      ))}

      <div className="hero-topright">
        <span className="hero-label">{slide.label}</span>
        <div className="hero-controls">
          <button type="button" onClick={() => go(index - 1)} aria-label="Anterior">
            ←
          </button>
          <div className="hero-dots">
            {slides.map((item, i) => (
              <button
                key={item.image}
                type="button"
                aria-current={i === index ? "true" : undefined}
                aria-label={`Ir a: ${item.kicker}`}
                className={i === index ? "hero-dot hero-dot-on" : "hero-dot"}
                onClick={() => setIndex(i)}
              />
            ))}
          </div>
          <button type="button" onClick={() => go(index + 1)} aria-label="Siguiente">
            →
          </button>
          <button
            type="button"
            className="hero-pause"
            onClick={() => setUserPaused((value) => !value)}
            aria-pressed={userPaused}
          >
            {userPaused ? "▶ Reanudar" : "❚❚ Pausar"}
          </button>
        </div>
      </div>

      <div className="hero-inner" aria-live="polite">
        <span className={slide.accent ? "hero-chip hero-chip-party" : "hero-chip"}>
          {slide.kicker}
        </span>
        <h1>{slide.title}</h1>
        <p>{slide.body}</p>
        {slide.cta ? (
          slide.cta.href ? (
            <a className="btn btn-teal hero-cta" href={slide.cta.href}>
              {slide.cta.label}
            </a>
          ) : (
            <Link className="btn btn-teal hero-cta" to={slide.cta.to}>
              {slide.cta.label}
            </Link>
          )
        ) : null}
      </div>

      <BlockNav variant="hero" />
    </section>
  );
}
