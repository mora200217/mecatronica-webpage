import { useEffect, useState } from "react";
import SectionTitle from "../components/SectionTitle.jsx";
import { getJSON } from "../api.js";

export default function Trabajos() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    getJSON("/api/theses").then(setItems);
  }, []);

  return (
    <div className="wrap">
      <SectionTitle kicker="Investigación formativa">Trabajos de grado</SectionTitle>
      <p>Muestra reciente para el MVP. Cada ficha puede enlazar después al repositorio o al PDF en el sistema de bibliotecas.</p>
      <div className="grid-cards">
        {items.map((t) => (
          <article key={t.title} className="panel">
            <p className="kicker">
              {t.year} · {t.modality}
            </p>
            <h3>{t.title}</h3>
            <p>{t.authors}</p>
            <p>
              {t.tags.map((tag) => (
                <span className="tag" key={tag}>
                  {tag}
                </span>
              ))}
            </p>
          </article>
        ))}
      </div>
    </div>
  );
}
