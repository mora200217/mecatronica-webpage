import { useEffect, useState } from "react";
import SectionTitle from "../components/SectionTitle.jsx";
import { getJSON } from "../api.js";

export default function Historia() {
  const [data, setData] = useState(null);
  useEffect(() => {
    getJSON("/api/history").then(setData);
  }, []);
  if (!data) return <p className="wrap">Cargando…</p>;

  return (
    <div className="wrap">
      <SectionTitle kicker="Memoria">Historia de la carrera</SectionTitle>
      <p>{data.intro}</p>
      <img src="/media/school-eng.jpg" alt="Facultad de Ingeniería UNAL" />
      <div className="timeline">
        {data.timeline.map((item) => (
          <article key={item.year} className="time-item">
            <p className="year">{item.year}</p>
            <h3>{item.title}</h3>
            <p>{item.body}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
