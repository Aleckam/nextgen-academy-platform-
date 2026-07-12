/** Used for screens on the Phase 1 list (§7) not yet wired to the backend
 * in this scaffold — keeps routing/navigation complete while flagging
 * what still needs full implementation. */
export default function PlaceholderPage({ title, note }) {
  return (
    <div>
      <div className="page-header">
        <h1>{title}</h1>
      </div>
      <div className="card placeholder-page">
        {note || "Screen scaffolded — full implementation pending."}
      </div>
    </div>
  );
}
