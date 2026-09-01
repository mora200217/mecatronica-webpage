import { useEffect, useState } from "react";
import SectionTitle from "../components/SectionTitle.jsx";
import { getJSON } from "../api.js";

const TABS = [
  { id: "docentes", label: "Docentes" },
  { id: "labs", label: "Laboratorios" },
  { id: "grupos", label: "Grupos de investigación" },
];

export default function Programa() {
  const [data, setData] = useState(null);
  const [tab, setTab] = useState("docentes");
  useEffect(() => {
    getJSON("/api/program").then(setData);
  }, []);
  if (!data) return <p className="wrap">Cargando…</p>;

  return (
    <div className="wrap">
      <SectionTitle kicker="Nuestro programa">Docentes, laboratorios y grupos</SectionTitle>
      <p>{data.about}</p>
      <div className="tabs">
        {TABS.map((item) => (
          <button key={item.id} className={tab === item.id ? "active" : ""} onClick={() => setTab(item.id)}>
            {item.label}
          </button>
        ))}
      </div>

      {tab === "docentes" ? (
        <div className="grid-cards">
          {data.faculty.map((p) => (
            <article key={p.name} className="panel">
              <p className="kicker">{p.real ? "Directorio oficial" : "Ficha ilustrativa"}</p>
              <h3>{p.name}</h3>
              <p>{p.role}</p>
              <p className="muted">{p.area}</p>
              <p>
                <a href={`mailto:${p.email}`}>{p.email}</a>
              </p>
            </article>
          ))}
        </div>
      ) : null}

      {tab === "labs" ? (
        <div className="grid-cards">
          {data.labs.map((lab) => (
            <article key={lab.name} className="panel">
              <p className="kicker">{lab.building}</p>
              <h3>{lab.name}</h3>
              <p>{lab.body}</p>
              <a className="btn btn-navy" href={lab.github} target="_blank" rel="noreferrer">
                GitHub del lab
              </a>
            </article>
          ))}
        </div>
      ) : null}

      {tab === "grupos" ? (
        <div className="grid-cards">
          {data.groups.map((g) => (
            <article key={g.name} className="panel">
              <h3>{g.name}</h3>
              <p>{g.line}</p>
              <a className="btn btn-teal" href={g.hermes} target="_blank" rel="noreferrer">
                Hermes
              </a>
            </article>
          ))}
        </div>
      ) : null}
    </div>
  );
}
