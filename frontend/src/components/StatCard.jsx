export default function StatCard({ value, label, tone }) {
  return (
    <div className={`stat-card ${tone || ""}`}>
      <div className="value">{value}</div>
      <div className="label">{label}</div>
    </div>
  );
}
