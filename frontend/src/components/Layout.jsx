import { Link, useLocation } from "react-router-dom";
import BlockNav from "./BlockNav.jsx";

export default function Layout({ children }) {
  const { pathname } = useLocation();
  const home = pathname === "/";

  return (
    <div className="shell">
      <header className="topbar">
        <Link className="brand" to="/">
          <span className="brand-kicker">UNAL · Facultad de Ingeniería</span>
          <strong>Ingeniería Mecatrónica</strong>
        </Link>
        <p className="brand-side">Sede Bogotá · SNIES 16939</p>
      </header>
      {home ? null : <BlockNav />}
      <main>{children}</main>
      <footer className="site-foot">
        <div>
          <p className="foot-kicker">Universidad Nacional de Colombia</p>
          <p>Programa curricular de Ingeniería Mecatrónica · Área de Ingeniería Mecánica y Mecatrónica</p>
        </div>
        <div>
          <p>Av. NQS (Cra. 30) 45-03 · Edificio 411, oficina 205</p>
          <p>El contenido de este MVP se edita en <code>backend/content/*.json</code></p>
        </div>
      </footer>
    </div>
  );
}
