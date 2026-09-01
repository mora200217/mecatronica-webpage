import { NavLink } from "react-router-dom";

export const PRIMARY = [
  { to: "/programa", label: "Programa" },
  { to: "/malla", label: "Malla" },
  { to: "/egresados", label: "Egresados" },
  { to: "/industria", label: "Industria" },
];

export const SECONDARY = [
  { to: "/", label: "Inicio" },
  { to: "/ofertas", label: "Ofertas" },
  { to: "/trabajos", label: "Tesis" },
  { to: "/historia", label: "Historia" },
  { to: "/noticias", label: "Noticias" },
  { to: "/puentes", label: "Puentes" },
];

export default function BlockNav({ variant = "bar" }) {
  return (
    <div className={variant === "hero" ? "nav-stack nav-stack-hero" : "nav-stack"}>
      <nav className="block-nav" aria-label="Secciones principales">
        {PRIMARY.map((item) => (
          <NavLink key={item.to} to={item.to}>
            {item.label}
          </NavLink>
        ))}
      </nav>
      <nav className="sub-nav" aria-label="Más secciones">
        {SECONDARY.map((item) => (
          <NavLink key={item.to} to={item.to} end={item.to === "/"}>
            {item.label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
