import { useEffect, useMemo, useState } from "react";
import SectionTitle from "../components/SectionTitle.jsx";
import { getJSON } from "../api.js";

const KEY = "malla-done-v1";

export default function Malla() {
  const [data, setData] = useState(null);
  const [selected, setSelected] = useState(null);
  const [area, setArea] = useState("todas");
  const [component, setComponent] = useState("todas");
  const [query, setQuery] = useState("");
  const [done, setDone] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem(KEY) || "[]");
    } catch {
      return [];
    }
  });

  useEffect(() => {
    getJSON("/api/curriculum").then((payload) => {
      setData(payload);
      setSelected(payload.courses[0]);
    });
  }, []);

  useEffect(() => {
    localStorage.setItem(KEY, JSON.stringify(done));
  }, [done]);

  const byId = useMemo(() => {
    const map = {};
    data?.courses.forEach((c) => {
      map[c.id] = c;
    });
    return map;
  }, [data]);

  const unlocks = useMemo(() => {
    if (!selected || !data) return [];
    return data.courses.filter((c) => c.prereqs.includes(selected.id)).map((c) => c.id);
  }, [selected, data]);

  const filtered = useMemo(() => {
    if (!data) return [];
    return data.courses.filter((c) => {
      if (area !== "todas" && c.area !== area) return false;
      if (component !== "todas" && c.component !== component) return false;
      if (query && !`${c.name} ${c.id}`.toLowerCase().includes(query.toLowerCase())) return false;
      return true;
    });
  }, [data, area, component, query]);

  const doneCredits = data
    ? data.courses.filter((c) => done.includes(c.id)).reduce((sum, c) => sum + c.credits, 0)
    : 0;

  if (!data) return <p className="wrap">Cargando…</p>;

  const semesters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

  function toggleDone(id) {
    setDone((curr) => (curr.includes(id) ? curr.filter((x) => x !== id) : [...curr, id]));
  }

  return (
    <div className="wrap" style={{ width: "min(1400px, calc(100% - 1.2rem))" }}>
      <SectionTitle kicker="Explorador">Malla curricular</SectionTitle>
      <p className="note">{data.disclaimer}</p>
      <p>
        <a className="btn btn-navy" href="/go/malla-oficial/">
          PDF oficial · Acuerdo 6 de 2022
        </a>
      </p>

      <div className="stats">
        {data.components.map((c) => (
          <div className="stat" key={c.id}>
            <span className="kicker">{c.label}</span>
            <b>{c.credits}</b>
            <span className="muted">{c.pct}</span>
          </div>
        ))}
        <div className="stat">
          <span className="kicker">Tu avance</span>
          <b>
            {doneCredits}/{data.totals.credits}
          </b>
          <span className="muted">{done.length} asignaturas</span>
        </div>
      </div>

      <div className="malla-toolbar">
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Buscar asignatura" />
        <select value={component} onChange={(e) => setComponent(e.target.value)}>
          <option value="todas">Todos los componentes</option>
          {data.components.map((c) => (
            <option key={c.id} value={c.id}>
              {c.label}
            </option>
          ))}
        </select>
        <select value={area} onChange={(e) => setArea(e.target.value)}>
          <option value="todas">Todas las áreas</option>
          {data.areas.map((a) => (
            <option key={a.id} value={a.id}>
              {a.label}
            </option>
          ))}
        </select>
        <button className="btn btn-ghost" type="button" onClick={() => setDone([])}>
          Limpiar avance
        </button>
      </div>
      <p className="legend">
        <span>
          <i className="swatch" style={{ background: "var(--navy)" }} /> Fundamentación
        </span>
        <span>
          <i className="swatch" style={{ background: "var(--teal)" }} /> Disciplinar
        </span>
        <span>
          <i className="swatch" style={{ background: "var(--char)" }} /> Libre elección
        </span>
        <span>Amarillo = prerrequisito · Celeste = desbloquea</span>
      </p>

      <div className="malla-board">
        {semesters.map((sem) => (
          <div className="sem-col" key={sem}>
            <h4>Sem {sem}</h4>
            {filtered
              .filter((c) => c.semester === sem)
              .map((c) => {
                const classes = [
                  "course",
                  c.component,
                  selected?.id === c.id ? "active" : "",
                  selected && c.prereqs.includes(selected.id) === false && selected.prereqs.includes(c.id)
                    ? "prereq"
                    : "",
                  unlocks.includes(c.id) ? "unlocks" : "",
                  done.includes(c.id) ? "done" : "",
                ];
                return (
                  <button key={c.id} className={classes.join(" ")} onClick={() => setSelected(c)} type="button">
                    {c.name}
                    <small>
                      {c.credits} cr · {c.id}
                    </small>
                  </button>
                );
              })}
          </div>
        ))}
      </div>

      {selected ? (
        <aside className="detail">
          <div>
            <p className="kicker">
              Semestre {selected.semester} · {selected.component}
            </p>
            <h2>{selected.name}</h2>
            <p>{selected.summary}</p>
            {selected.note ? <p className="note">{selected.note}</p> : null}
            <p>
              Prerrequisitos:{" "}
              {selected.prereqs.length
                ? selected.prereqs.map((id) => byId[id]?.name || id).join(", ")
                : "ninguno"}
            </p>
            <p>
              Abre la puerta a:{" "}
              {unlocks.length ? unlocks.map((id) => byId[id]?.name || id).join(", ") : "cierre o electivas"}
            </p>
          </div>
          <div>
            <p>
              <b>{selected.credits}</b> créditos
            </p>
            <button className="btn btn-teal" type="button" onClick={() => toggleDone(selected.id)}>
              {done.includes(selected.id) ? "Quitar de mi avance" : "Marcar como vista"}
            </button>
          </div>
        </aside>
      ) : null}
    </div>
  );
}
