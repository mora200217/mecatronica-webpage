import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import BirthdayBand from "../components/BirthdayBand.jsx";
import HeroCarousel from "../components/HeroCarousel.jsx";
import SectionTitle from "../components/SectionTitle.jsx";
import { getJSON } from "../api.js";

export default function Home() {
  const [site, setSite] = useState(null);
  const [news, setNews] = useState([]);
  const [events, setEvents] = useState(null);
  const [anniversary, setAnniversary] = useState(null);
  const [filter, setFilter] = useState("academicos");

  useEffect(() => {
    getJSON("/api/site").then(setSite);
    getJSON("/api/news").then(setNews);
    getJSON("/api/events").then(setEvents);
    getJSON("/api/anniversary").then(setAnniversary);
  }, []);

  if (!site || !events) return <p className="wrap">Cargando…</p>;

  const visible = events.items.filter((item) => item.type === filter);

  return (
    <>
      <HeroCarousel slides={site.hero} />

      <div className="wrap">
        <div className="grid-3" style={{ marginBottom: "2rem" }}>
          {[
            { img: "/media/cyt.jpg", title: "Ciencia y Tecnología", to: "/programa" },
            { img: "/media/aulas-ing.jpg", title: "Aulas de Ingeniería", to: "/malla" },
            { img: "/media/ingenierias.jpg", title: "Campus y comunidad", to: "/egresados" },
          ].map((item) => (
            <Link key={item.title} className="card" to={item.to} style={{ textDecoration: "none" }}>
              <img src={item.img} alt={item.title} />
              <div className="card-body">
                <h3>{item.title}</h3>
                <p className="muted">Entrar</p>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {anniversary ? <BirthdayBand data={anniversary} /> : null}

      <div className="wrap">
        <div className="grid-2">
          <section>
            <SectionTitle kicker="Comunidad">Noticias</SectionTitle>
            <Link className="btn" to="/noticias">
              Todas las noticias ↗
            </Link>
            <div className="news-thumbs">
              {news.slice(0, 2).map((post) => (
                <Link key={post.slug} className="card" to={`/noticias/${post.slug}`} style={{ textDecoration: "none" }}>
                  <img src={post.image} alt="" />
                  <div className="card-body">
                    <p className="kicker">{post.kicker}</p>
                    <h3>{post.title}</h3>
                  </div>
                </Link>
              ))}
            </div>
          </section>
          <section>
            <SectionTitle kicker="Calendario">Eventos</SectionTitle>
            <div className="filter-row">
              {events.filters.map((item) => (
                <button
                  key={item.id}
                  aria-pressed={filter === item.id}
                  onClick={() => setFilter(item.id)}
                >
                  {item.label}
                </button>
              ))}
            </div>
            {visible.map((item) => (
              <article key={item.id} className="event-item">
                <div>
                  <p className="kicker">{item.month}</p>
                  <strong>{item.day}</strong>
                </div>
                <div>
                  <h3>{item.title}</h3>
                  <p className="muted">{item.place}</p>
                </div>
              </article>
            ))}
          </section>
        </div>
      </div>
    </>
  );
}
