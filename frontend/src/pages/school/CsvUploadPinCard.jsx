import { useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";
import { useAuth } from "../../context/AuthContext";

/** WF03 — CSV Student Upload + PIN Card flow */
export default function CsvUploadPinCard() {
  const { user } = useAuth();
  const schoolId = user?.school_id || 1;

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [confirmResult, setConfirmResult] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  const handleUpload = async (selectedFile) => {
    setFile(selectedFile);
    setError(null);
    setConfirmResult(null);
    const form = new FormData();
    form.append("file", selectedFile);
    setBusy(true);
    try {
      const res = await client.post(`/schools/${schoolId}/students/upload`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setPreview(res.data);
    } catch (err) {
      setError(err.response?.data?.error || "Upload failed");
    } finally {
      setBusy(false);
    }
  };

  const handleConfirm = async () => {
    setBusy(true);
    try {
      const res = await client.post(`/schools/${schoolId}/students/confirm`, {
        valid_rows: preview.valid_rows,
      });
      setConfirmResult(res.data);
    } catch (err) {
      setError(err.response?.data?.error || "Could not create accounts");
    } finally {
      setBusy(false);
    }
  };

  const downloadPinCards = async (className, students) => {
    const classId = confirmResult.class_ids_by_name[className];
    const res = await client.post(
      `/schools/${schoolId}/classes/${classId}/pin-cards.pdf`,
      { students },
      { responseType: "blob" }
    );
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const a = document.createElement("a");
    a.href = url;
    a.download = `pin-cards-${className.replace(/\s+/g, "-")}.pdf`;
    a.click();
  };

  return (
    <Layout>
      <div className="page-header">
        <h1>Upload students</h1>
      </div>

      {error && <div className="card" style={{ marginBottom: 16, color: "var(--red)" }}>{error}</div>}

      <div className="two-col" style={{ marginBottom: 20 }}>
        <div className="card">
          <strong>Upload student list</strong>
          <p style={{ color: "var(--text-muted)", fontSize: 13 }}>Add students in bulk via CSV file</p>
          <div className="dropzone">
            <div style={{ marginBottom: 10 }}>Drag and drop your CSV file here</div>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => e.target.files[0] && handleUpload(e.target.files[0])}
            />
          </div>
          <div style={{ marginTop: 14, fontSize: 12.5, color: "var(--text-muted)" }}>
            Required columns: <strong>First name, Last name, Class name</strong>. Optional: Student ID, Age group.
          </div>
        </div>

        <div className="card">
          <strong>How it works</strong>
          <ol style={{ fontSize: 13.5, paddingLeft: 18, color: "var(--text)" }}>
            <li>Download the CSV template and fill in student names.</li>
            <li>Upload the file — NextGen reads it and shows a preview before saving.</li>
            <li>Download PIN cards — a 4-digit PIN is generated per student.</li>
          </ol>
          <div className="card" style={{ background: "var(--amber-bg)", boxShadow: "none", fontSize: 12.5 }}>
            No email addresses needed. Students log in with their name and PIN only — works on any device,
            including shared school computers.
          </div>
        </div>
      </div>

      {preview && !confirmResult && (
        <div className="card" style={{ marginBottom: 20 }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <strong>
              {preview.total} students read from your file — please review before confirming
            </strong>
            <button className="btn primary" disabled={busy || preview.valid_rows.length === 0} onClick={handleConfirm}>
              Confirm &amp; create accounts
            </button>
          </div>
          <div style={{ fontSize: 12.5, color: "var(--text-muted)", margin: "6px 0 12px" }}>
            {preview.valid_rows.length} valid · {preview.error_rows.length} need attention
          </div>
          <table className="data-table">
            <thead>
              <tr><th>Name</th><th>Class</th><th>Status</th></tr>
            </thead>
            <tbody>
              {preview.valid_rows.map((r, i) => (
                <tr key={`v${i}`}>
                  <td>{r.first_name} {r.last_name}</td>
                  <td>{r.class_name}</td>
                  <td><span className="badge ready">Ready</span></td>
                </tr>
              ))}
              {preview.error_rows.map((r, i) => (
                <tr key={`e${i}`}>
                  <td>{r.first_name} {r.last_name}</td>
                  <td>{r.class_name}</td>
                  <td><span className="badge error">{r.errors.join(", ")}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {confirmResult && (
        <div className="card">
          <strong>{confirmResult.created_count} student accounts created</strong>
          <p style={{ fontSize: 13, color: "var(--text-muted)" }}>
            Download the PIN card sheet for each class and hand it out — students can log in immediately.
          </p>
          {Object.entries(confirmResult.pin_cards_by_class).map(([className, students]) => (
            <div key={className} className="card" style={{ boxShadow: "none", marginBottom: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <strong>{className}</strong>
                <button className="btn gold" onClick={() => downloadPinCards(className, students)}>
                  Download PIN cards (PDF)
                </button>
              </div>
              <table className="data-table">
                <thead><tr><th>Name</th><th>Username</th><th>PIN</th></tr></thead>
                <tbody>
                  {students.map((s) => (
                    <tr key={s.username}>
                      <td>{s.name}</td>
                      <td>{s.username}</td>
                      <td>{s.pin}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}
