export default function ProgressBar({ pct }) {
  return (
    <div className="progress-bar">
      <div style={{ width: `${Math.min(100, Math.max(0, pct || 0))}%` }} />
    </div>
  );
}
