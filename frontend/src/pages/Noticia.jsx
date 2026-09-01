import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getJSON } from "../api.js";

export default function Noticia() {
  const { slug } = useParams();
  const [post, setPost] = useState(null);
  useEffect(() => {
    getJSON(`/api/news?slug=${slug}`).then(setPost);
  }, [slug]);
  if (!post) return <p className="wrap">Cargando…</p>;

  return (
    <div className="wrap" style={{ maxWidth: 760 }}>
      <p className="kicker">
        {post.date} · {post.kicker}
      </p>
      <h1>{post.title}</h1>
      <img src={post.image} alt="" />
      {post.body.split("\n\n").map((p) => (
        <p key={p.slice(0, 24)}>{p}</p>
      ))}
      <Link className="btn btn-ghost" to="/noticias">
        Volver
      </Link>
    </div>
  );
}
