import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Egresados from "./pages/Egresados.jsx";
import Historia from "./pages/Historia.jsx";
import Home from "./pages/Home.jsx";
import Industria from "./pages/Industria.jsx";
import Malla from "./pages/Malla.jsx";
import Noticia from "./pages/Noticia.jsx";
import Noticias from "./pages/Noticias.jsx";
import Ofertas from "./pages/Ofertas.jsx";
import Programa from "./pages/Programa.jsx";
import Puentes from "./pages/Puentes.jsx";
import Trabajos from "./pages/Trabajos.jsx";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/programa" element={<Programa />} />
        <Route path="/malla" element={<Malla />} />
        <Route path="/industria" element={<Industria />} />
        <Route path="/egresados" element={<Egresados />} />
        <Route path="/ofertas" element={<Ofertas />} />
        <Route path="/trabajos" element={<Trabajos />} />
        <Route path="/historia" element={<Historia />} />
        <Route path="/noticias" element={<Noticias />} />
        <Route path="/noticias/:slug" element={<Noticia />} />
        <Route path="/puentes" element={<Puentes />} />
      </Routes>
    </Layout>
  );
}
