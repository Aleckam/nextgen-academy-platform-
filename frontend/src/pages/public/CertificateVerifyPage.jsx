import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import client from "../../api/client";
import PublicLayout from "../../components/PublicLayout";

/** Certificate verification page — public, reached by scanning the QR code
 * printed on a certificate (§3.7). */
export default function CertificateVerifyPage() {
  const { code } = useParams();
  const [result, setResult] = useState(null);

  useEffect(() => {
    client
      .get(`/certificates/verify/${code}`)
      .then((res) => setResult(res.data))
      .catch(() => setResult({ valid: false }));
  }, [code]);

  return (
    <PublicLayout>
      <div className="card" style={{ maxWidth: 480, margin: "0 auto" }}>
        {!result && <div>Checking…</div>}
        {result && !result.valid && <div style={{ color: "var(--red)" }}>Certificate not found or invalid.</div>}
        {result?.valid && (
          <div>
            <span className="badge on-track">Verified</span>
            <h2>{result.student_name}</h2>
            <p>Completed <strong>{result.module_title}</strong></p>
            <p style={{ color: "var(--text-muted)", fontSize: 13 }}>
              Issued {new Date(result.issued_at).toLocaleDateString()}
            </p>
          </div>
        )}
      </div>
    </PublicLayout>
  );
}
