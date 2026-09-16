import { useEffect, useMemo, useState } from "react";
import SectionTitle from "../components/SectionTitle.jsx";
import { getJSON } from "../api.js";

export default function Ofertas() {
  const [jobs, setJobs] = useState([]);
  const [type, setType] = useState("Todas");
  useEffect(() => {
    getJSON("/api/jobs").then(setJobs);
  }, []);
  const types = ["Todas", ...new Set(jobs.map((j) => j.type))];
  const visible = useMemo(
    () => jobs.filter((j) => type === "Todas" || j.type === type),
    [jobs, type]
  );

  return (
    <div className="wrap">
      <SectionTitle kicker="Empleo y práctica">Ofertas laborales</SectionTitle>
      <p className="note">Prácticas, trabajos de grado y vacantes que llegan al programa. Se publican desde el panel de administración.</p>
      <div className="filter-row">
        {types.map((t) => (
          <button key={t} aria-pressed={type === t} onClick={() => setType(t)}>
            {t}
          </button>
        ))}
      </div>
      {visible.map((job) => (
        <article key={job.id} className="panel" style={{ marginBottom: "0.7rem" }}>
          <p className="kicker">
            {job.type} · cierra {job.deadline}
          </p>
          <h3>{job.title}</h3>
          <p>
            {job.company} · {job.area}
          </p>
          <p>{job.body}</p>
        </article>
      ))}
    </div>
  );
}
