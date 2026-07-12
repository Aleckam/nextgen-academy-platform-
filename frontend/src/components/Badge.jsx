const LABELS = {
  on_track: "On track",
  needs_attention: "Needs attention",
  falling_behind: "Falling behind",
  inactive: "Inactive",
  completed: "Completed",
  ready: "Ready",
  error: "Error",
};

export default function Badge({ status }) {
  const cls = (status || "").replace(/_/g, "-");
  return <span className={`badge ${cls}`}>{LABELS[status] || status}</span>;
}
