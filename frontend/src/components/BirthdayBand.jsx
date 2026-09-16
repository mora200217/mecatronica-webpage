import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

function useCountdown(target) {
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(timer);
  }, []);

  return useMemo(() => {
    const diff = target - now;
    if (diff <= 0) return null;
    const total = Math.floor(diff / 1000);
    return {
      dias: Math.floor(total / 86400),
      horas: Math.floor((total % 86400) / 3600),
      min: Math.floor((total % 3600) / 60),
      seg: total % 60,
    };
  }, [target, now]);
}

export default function BirthdayBand({ data }) {
  const [day, setDay] = useState(data.days[0].id);

  const start = useMemo(() => new Date(data.startsAt).getTime(), [data.startsAt]);
  const end = useMemo(() => new Date(data.endsAt).getTime(), [data.endsAt]);
  const left = useCountdown(start);
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 30000);
    return () => clearInterval(timer);
  }, []);

  const live = now >= start && now <= end;
  const past = now > end;
  const agenda = data.days.find((item) => item.id === day);

  return (
    <section className="party" id="aniversario">
      <div className="party-inner">
        <div className="party-head">
          <img className="party-logo" src={data.logo} alt={`${data.years} años de Ingeniería Mecatrónica`} />
          <div>
            <p className="party-kicker">{data.kicker}</p>
            <h2>{data.headline}</h2>
            <p className="party-lead">{data.lead}</p>
            <p className="party-when">
              <strong>{data.dateLabel}</strong>
              <span>{data.venue}</span>
            </p>
            {data.cta?.to ? (
              <Link className="btn btn-lime" to={data.cta.to}>
                {data.cta.label} →
              </Link>
            ) : null}
          </div>
        </div>

        <div className="party-count">
          {live ? (
            <p className="party-live">
              <span className="party-pulse" aria-hidden="true" /> Sucediendo ahora en el Auditorio CyT
            </p>
          ) : past ? (
            <p className="party-live">Gracias por estos {data.years} años.</p>
          ) : left ? (
            <>
              <p className="party-count-label">Faltan</p>
              <div className="party-clock">
                {[
                  ["dias", "días"],
                  ["horas", "horas"],
                  ["min", "min"],
                  ["seg", "seg"],
                ].map(([key, label]) => (
                  <div key={key} className="party-unit">
                    <b>{String(left[key]).padStart(2, "0")}</b>
                    <span>{label}</span>
                  </div>
                ))}
              </div>
            </>
          ) : null}
        </div>

        <div className="party-highlights">
          {data.highlights.map((item) => (
            <article key={item.id}>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
            </article>
          ))}
        </div>

        <div className="party-agenda">
          <div className="party-tabs" role="tablist" aria-label="Agenda del aniversario">
            {data.days.map((item) => (
              <button
                key={item.id}
                type="button"
                role="tab"
                aria-selected={day === item.id}
                className={day === item.id ? "party-tab party-tab-on" : "party-tab"}
                onClick={() => setDay(item.id)}
              >
                <strong>{item.label}</strong>
                <span>{item.theme}</span>
              </button>
            ))}
          </div>
          <ol className="party-list">
            {agenda.agenda.map((slot) => (
              <li key={`${slot.time}-${slot.title}`} className={`party-slot slot-${slot.track}`}>
                <span className="party-time">
                  {slot.time}
                  <em>{slot.end}</em>
                </span>
                <span>
                  <strong>{slot.title}</strong>
                  {slot.note ? <em className="party-note">{slot.note}</em> : null}
                </span>
              </li>
            ))}
          </ol>
        </div>

        <p className="party-credit">{data.credit}</p>
      </div>
    </section>
  );
}
