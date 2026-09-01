import { useEffect, useState } from "react";
import SectionTitle from "../components/SectionTitle.jsx";
import { getJSON } from "../api.js";

export default function Industria() {
  const [data, setData] = useState(null);
  useEffect(() => {
    getJSON("/api/industry").then(setData);
  }, []);
  if (!data) return <p className="wrap">Cargando…</p>;

  return (
    <div className="wrap">
      <SectionTitle kicker="Campo de acción">Industria</SectionTitle>
      <p>{data.pitch}</p>
      <div className="grid-cards">
        {data.sectors.map((sector) => (
          <article key={sector.name} className="panel">
            <h3>{sector.name}</h3>
            <p>{sector.body}</p>
            <p>
              {sector.examples.map((ex) => (
                <span className="tag" key={ex}>
                  {ex}
                </span>
              ))}
            </p>
          </article>
        ))}
      </div>
      <SectionTitle kicker="Red">Dónde se mueve el egresado</SectionTitle>
      <div className="grid-3">
        {data.partners.map((p) => (
          <article key={p.name} className="panel">
            <h3>{p.name}</h3>
            <p className="muted">{p.role}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
