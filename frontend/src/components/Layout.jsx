import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import BlockNav from "./BlockNav.jsx";
import { getJSON } from "../api.js";

export default function Layout({ children }) {
  const { pathname } = useLocation();
  const home = pathname === "/";
  const [site, setSite] = useState(null);

  useEffect(() => {
    getJSON("/api/site").then(setSite);
  }, []);

  const contact = site?.contact ?? {};

  return (
    <div className="shell">
      <header className="topbar">
        <Link className="brand" to="/">
          <span className="brand-kicker">UNAL · {site?.faculty}</span>
          <strong>{site?.program}</strong>
        </Link>
        <p className="brand-side">
          {site ? `${site.campus} · SNIES ${site.snies}` : null}
        </p>
      </header>
      {home ? null : <BlockNav />}
      <main>{children}</main>
      <footer className="site-foot">
        <div>
          <p className="foot-kicker">{site?.university}</p>
          <p>{site ? `Programa curricular de ${site.program} · ${site.faculty}` : null}</p>
        </div>
        <div>
          <p>{contact.building ? `${contact.building} · ${contact.address}` : null}</p>
          <p>
            {site?.disclaimer} El contenido se edita en el{" "}
            <a href="/admin/">panel de administración</a>.
          </p>
        </div>
      </footer>
    </div>
  );
}
