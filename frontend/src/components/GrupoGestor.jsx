import { gestor } from "../data/gestor.js";

export default function GrupoGestor() {
  return (
    <section className="gestor" id="grupo-gestor" aria-labelledby="gestor-title">
      <div className="gestor-inner">
        <header className="gestor-head">
          <p className="gestor-kicker">{gestor.kicker}</p>
          <h2 id="gestor-title">{gestor.title}</h2>
          <p>{gestor.lead}</p>
        </header>

        <ul className="gestor-grid">
          {gestor.people.map((person) => (
            <li key={person.id}>
              <figure className="gestor-card">
                <div className="gestor-photo">
                  <img
                    src={person.photo}
                    alt={person.name}
                    style={{ objectPosition: person.position }}
                  />
                </div>
                <figcaption>
                  <strong>{person.name}</strong>
                  <span>{person.role}</span>
                </figcaption>
              </figure>
            </li>
          ))}
        </ul>
        <p className="gestor-note">{gestor.note}</p>
      </div>
    </section>
  );
}
