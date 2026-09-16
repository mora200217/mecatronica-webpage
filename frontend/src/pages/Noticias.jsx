import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import SectionTitle from "../components/SectionTitle.jsx";
import { getJSON } from "../api.js";

export default function Noticias() {
  const [posts, setPosts] = useState([]);
  useEffect(() => {
    getJSON("/api/news").then(setPosts);
  }, []);

  return (
    <div className="wrap">
      <SectionTitle kicker="CMS / blog">Noticias</SectionTitle>
      <p>Lo que va pasando en el programa. Cada entrada se publica desde el panel de administración.</p>
      <div className="grid-cards">
        {posts.map((post) => (
          <Link key={post.slug} className="card" to={`/noticias/${post.slug}`} style={{ textDecoration: "none" }}>
            <img src={post.image} alt="" />
            <div className="card-body">
              <p className="kicker">{post.date} · {post.kicker}</p>
              <h3>{post.title}</h3>
              <p className="muted">{post.excerpt}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
