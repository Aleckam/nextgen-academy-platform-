import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import client from "../../api/client";
import PublicLayout from "../../components/PublicLayout";

/** One of 4 age-group programme pages (§7). */
export default function ProgrammePage() {
  const { ageGroup } = useParams();
  const [programmes, setProgrammes] = useState([]);

  useEffect(() => {
    client.get("/content/programmes", { params: { age_group: ageGroup } }).then((res) => setProgrammes(res.data));
  }, [ageGroup]);

  return (
    <PublicLayout>
      <h1>Programme — Ages {ageGroup}</h1>
      {programmes.length === 0 && <div className="card placeholder-page">No programmes published for this age group yet.</div>}
      {programmes.map((p) => (
        <div key={p.id} className="card" style={{ marginBottom: 12 }}>
          <strong>{p.title}</strong>
          <p style={{ color: "var(--text-muted)", fontSize: 13.5 }}>{p.description}</p>
        </div>
      ))}
    </PublicLayout>
  );
}
