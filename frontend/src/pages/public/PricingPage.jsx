import PublicLayout from "../../components/PublicLayout";

const TIERS = [
  { name: "Individual", price: "$4.99/mo", detail: "1 learner · any age group" },
  { name: "Family", price: "$9.99/mo", detail: "Up to 3 learners" },
  { name: "Professional", price: "$7.99/mo", detail: "Adult-focused content track" },
  { name: "School / Institution", price: "Contact us", detail: "Bulk CSV enrolment, PIN login, term reports" },
];

export default function PricingPage() {
  return (
    <PublicLayout>
      <h1>Pricing</h1>
      <div className="stat-grid">
        {TIERS.map((t) => (
          <div key={t.name} className="card">
            <strong>{t.name}</strong>
            <div style={{ fontSize: 22, fontWeight: 700, margin: "8px 0" }}>{t.price}</div>
            <div style={{ color: "var(--text-muted)", fontSize: 13 }}>{t.detail}</div>
          </div>
        ))}
      </div>
    </PublicLayout>
  );
}
