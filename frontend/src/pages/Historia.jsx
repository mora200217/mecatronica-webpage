import { useEffect, useState } from "react";
import Gallery from "../components/Gallery.jsx";
import GrupoGestor from "../components/GrupoGestor.jsx";
import SectionTitle from "../components/SectionTitle.jsx";
import StatGrid from "../components/StatGrid.jsx";
import Timeline from "../components/Timeline.jsx";
import Voices from "../components/Voices.jsx";
import { getJSON } from "../api.js";

export default function Historia() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getJSON("/api/history").then(setData);
  }, []);

  if (!data) return <p className="wrap">Cargando…</p>;

  return (
    <>
    <div className="wrap">
      <SectionTitle kicker="Memoria">Historia de la carrera</SectionTitle>
      <p className="lede">{data.intro}</p>

      <StatGrid stats={data.stats} />
    </div>

    <GrupoGestor />

    <Voices />

    <div className="wrap">
      <SectionTitle kicker="Línea de tiempo">Cómo llegamos hasta aquí</SectionTitle>
      <p className="muted">
        Filtra por época o recorre los hitos con las flechas del teclado.
      </p>
      <Timeline items={data.timeline} eras={data.eras} />

      <SectionTitle kicker="Álbum">Los lugares de la carrera</SectionTitle>
      <Gallery items={data.gallery} />
    </div>
    </>
  );
}
