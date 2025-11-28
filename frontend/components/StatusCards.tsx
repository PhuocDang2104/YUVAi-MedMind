const cards = [
  { title: "Adherence today", value: "82%", tone: "var(--primary)" },
  { title: "Missed doses this week", value: "2", tone: "var(--warning)" },
  { title: "Critical alerts", value: "0", tone: "var(--success)" },
  { title: "New symptoms", value: "Headache, dizziness", tone: "var(--accent)" }
];

export default function StatusCards() {
  return (
    <section className="grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))" }}>
      {cards.map((card) => (
        <article key={card.title} className="card">
          <div className="pill" style={{ background: `${card.tone}1f` }}>
            {card.title}
          </div>
          <h2 style={{ margin: "8px 0 4px" }}>{card.value}</h2>
        </article>
      ))}
    </section>
  );
}
