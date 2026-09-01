export default function SectionTitle({ kicker, children }) {
  return (
    <header className="section-title">
      {kicker ? <p className="kicker">{kicker}</p> : null}
      <h2>{children}</h2>
      <span className="rule" aria-hidden="true" />
    </header>
  );
}
