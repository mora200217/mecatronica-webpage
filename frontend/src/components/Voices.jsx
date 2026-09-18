import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { voices } from "../data/voices.js";

export default function Voices({ variant = "full" }) {
  const items = variant === "home" ? voices.items.filter((item) => item.home) : voices.items;
  const [active, setActive] = useState(items[0]);
  const videoRef = useRef(null);

  useEffect(() => {
    const node = videoRef.current;
    if (!node) return undefined;
    node.pause();
    node.load();
    return undefined;
  }, [active.id]);

  useEffect(() => {
    if (window.location.hash === "#voces") {
      document.getElementById("voces")?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, []);

  return (
    <section className={variant === "home" ? "voices voices-home" : "voices"} id="voces">
      <div className="voices-inner">
        <header className="voices-head">
          <p className="voices-kicker">{voices.kicker}</p>
          <h2>{voices.title}</h2>
          <p>{voices.lead}</p>
        </header>

        <div className={`voices-stage ${active.orientation === "portrait" ? "voices-stage-portrait" : ""}`}>
          <figure className="voices-player">
            <video
              ref={videoRef}
              key={active.id}
              poster={active.poster}
              controls
              playsInline
              preload="metadata"
            >
              <source src={active.src} type="video/mp4" />
            </video>
            <figcaption>
              <span className="voices-speaker">{active.speaker}</span>
              <span>{active.place}</span>
              <span className="voices-time">{active.duration}</span>
            </figcaption>
          </figure>

          <ul className="voices-rail">
            {items.map((item) => (
              <li key={item.id}>
                <button
                  type="button"
                  className={item.id === active.id ? "voices-thumb voices-thumb-on" : "voices-thumb"}
                  onClick={() => setActive(item)}
                >
                  <img src={item.poster} alt="" />
                  <span className="voices-thumb-play" aria-hidden="true">
                    ▶
                  </span>
                  <span>
                    <strong>{item.speaker}</strong>
                    <em>{item.place}</em>
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </div>

        {variant === "home" ? (
          <p className="voices-more">
            <Link className="btn btn-lime" to="/historia#voces">
              Ver todas las voces →
            </Link>
          </p>
        ) : (
          <p className="voices-credit">{voices.credit}</p>
        )}
      </div>
    </section>
  );
}
