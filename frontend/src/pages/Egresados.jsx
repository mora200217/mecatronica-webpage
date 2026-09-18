import { useEffect, useMemo, useState } from "react";
import SectionTitle from "../components/SectionTitle.jsx";
import { getJSON } from "../api.js";

export default function Egresados() {
  const [data, setData] = useState(null);
  const [q, setQ] = useState("");
  useEffect(() => {
    getJSON("/api/alumni").then(setData);
  }, []);
  const people = useMemo(() => {
    if (!data) return [];
    const needle = q.toLowerCase();
    return data.people.filter((p) =>
      `${p.name} ${p.company} ${p.focus} ${p.city} ${p.role}`.toLowerCase().includes(needle)
    );
  }, [data, q]);
  if (!data) return <p className="wrap">Cargando…</p>;

  return (
    <div className="wrap">
      <SectionTitle kicker="Red">Egresados</SectionTitle>
      <p className="note">{data.note}</p>
      <div className="malla-toolbar">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Buscar por nombre, ciudad, empresa o foco"
        />
      </div>
      <div className="grid-cards">
        {people.map((p) => (
          <article key={p.linkedin || p.name} className="panel person">
            <p className="kicker">{p.cohort ? `Cohorte ${p.cohort}` : "Egresado/a"}</p>
            <h3>{p.name}</h3>
            <p>
              {p.role}
              {p.company ? ` · ${p.company}` : ""}
            </p>
            <p className="muted">
              {[p.city, p.focus].filter(Boolean).join(" · ")}
            </p>
            <div className="person-actions">
              {p.mentorship ? <span className="tag">Mentoría</span> : null}
              {p.linkedin ? (
                <a className="tag tag-link" href={p.linkedin} target="_blank" rel="noreferrer">
                  LinkedIn ↗
                </a>
              ) : null}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
