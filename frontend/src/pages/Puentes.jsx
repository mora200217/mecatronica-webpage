import { useEffect, useState } from "react";
import SectionTitle from "../components/SectionTitle.jsx";
import { getJSON } from "../api.js";

export default function Puentes() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    getJSON("/api/redirects").then(setItems);
  }, []);
  const groups = [...new Set(items.map((i) => i.group))];

  return (
    <div className="wrap">
      <SectionTitle kicker="Orquestador">Puentes UNAL</SectionTitle>
      <p>
        Un solo lugar para salir a los sistemas que ya existen. Django resuelve <code>/go/atajo/</code> y redirige;
        los atajos se agregan desde el panel de administración.
      </p>
      {groups.map((group) => (
        <section key={group}>
          <h3>{group}</h3>
          <div className="grid-cards">
            {items
              .filter((i) => i.group === group)
              .map((item) => (
                <article key={item.slug} className="panel">
                  <p className="kicker">/go/{item.slug}/</p>
                  <h3>{item.title}</h3>
                  <p>{item.description}</p>
                  <a className="btn btn-navy" href={`/go/${item.slug}/`}>
                    Ir
                  </a>
                </article>
              ))}
          </div>
        </section>
      ))}
    </div>
  );
}
