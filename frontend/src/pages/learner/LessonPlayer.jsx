import { useEffect, useRef, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import client from "../../api/client";
import Layout from "../../components/Layout";
import ProgressBar from "../../components/ProgressBar";

function formatDuration(totalSeconds) {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

/** WF04 — Young Investors Lesson Player */
export default function LessonPlayer() {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [watched, setWatched] = useState(0);
  const saveTimer = useRef(null);

  useEffect(() => {
    client
      .get(`/content/lessons/${lessonId}`)
      .then((res) => {
        setData(res.data);
        setWatched(res.data.my_progress.watched_seconds || 0);
      })
      .catch((err) => setError(err.response?.data?.error || "Failed to load lesson"));
  }, [lessonId]);

  useEffect(() => {
    if (!data) return;
    clearTimeout(saveTimer.current);
    saveTimer.current = setTimeout(() => {
      client.put(`/content/lessons/${lessonId}/progress`, { watched_seconds: watched }).catch(() => {});
    }, 800);
    return () => clearTimeout(saveTimer.current);
  }, [watched, data, lessonId]);

  const markComplete = async () => {
    await client.put(`/content/lessons/${lessonId}/progress`, { watched_seconds: watched, completed: true });
    if (data.quiz_id) navigate(`/learn/quiz/${data.quiz_id}`);
  };

  if (error) return <Layout><div className="card">{error}</div></Layout>;
  if (!data) return <Layout><div className="card">Loading…</div></Layout>;

  const { lesson, module, sibling_lessons } = data;
  const pct = lesson.duration_seconds ? Math.round((watched / lesson.duration_seconds) * 100) : 0;
  const moduleCompletionPct = Math.round(
    (sibling_lessons.filter((l) => l.progress.status === "completed").length / sibling_lessons.length) * 100
  );

  return (
    <Layout>
      <div style={{ fontSize: 13, marginBottom: 10, color: "var(--text-muted)" }}>
        <Link to="/learn/modules">{module.title}</Link> · Module {module.order + 1} of 5
      </div>

      <div className="two-col" style={{ alignItems: "start" }}>
        <div>
          <div
            className="card"
            style={{ background: "var(--navy)", color: "#fff", textAlign: "center", padding: 40, marginBottom: 16 }}
          >
            <div style={{ color: "#9fb4d8", fontSize: 12 }}>
              MODULE {module.order + 1} · LESSON {lesson.order + 1}
            </div>
            <h2 style={{ margin: "10px 0" }}>{lesson.title}</h2>
            <div style={{ fontSize: 13, color: "#c8d5ea" }}>{formatDuration(lesson.duration_seconds)}</div>
            <input
              type="range"
              min={0}
              max={lesson.duration_seconds}
              value={watched}
              onChange={(e) => setWatched(Number(e.target.value))}
              style={{ width: "100%", marginTop: 20 }}
            />
            <div style={{ fontSize: 12, color: "#9fb4d8" }}>
              {formatDuration(watched)} / {formatDuration(lesson.duration_seconds)}
            </div>
          </div>

          <div className="card">
            <h3 style={{ marginTop: 0 }}>{lesson.title}</h3>
            <div style={{ fontSize: 12.5, color: "var(--text-muted)", marginBottom: 12 }}>
              {Math.round(lesson.duration_seconds / 60)} min · Workbook included · Quiz after lesson
            </div>

            {lesson.key_terms?.length > 0 && (
              <>
                <strong>Key terms in this lesson</strong>
                <div className="stat-grid" style={{ marginTop: 8, marginBottom: 16 }}>
                  {lesson.key_terms.map((kt) => (
                    <div key={kt.term} className="card" style={{ boxShadow: "none" }}>
                      <div style={{ fontWeight: 600, fontSize: 13.5 }}>{kt.term}</div>
                      <div style={{ fontSize: 12.5, color: "var(--text-muted)" }}>{kt.definition}</div>
                    </div>
                  ))}
                </div>
              </>
            )}

            <div className="card" style={{ background: "var(--green-bg)", boxShadow: "none", fontSize: 13, marginBottom: 14 }}>
              Finish watching to unlock the quiz — answer 4 out of 5 correctly to progress to the next lesson.
            </div>

            <div style={{ display: "flex", justifyContent: "flex-end", gap: 10 }}>
              {lesson.workbook_url && (
                <a className="btn" href={lesson.workbook_url}>Workbook</a>
              )}
              <button className="btn primary" onClick={markComplete} disabled={pct < 90}>
                Next lesson
              </button>
            </div>
          </div>
        </div>

        <div>
          <div className="card" style={{ marginBottom: 16 }}>
            <strong>{module.title}</strong>
            <div style={{ fontSize: 12.5, color: "var(--text-muted)", marginBottom: 10 }}>
              {sibling_lessons.filter((l) => l.progress.status === "completed").length} of {sibling_lessons.length} lessons complete
            </div>
            <ProgressBar pct={moduleCompletionPct} />
            <div style={{ marginTop: 12 }}>
              {sibling_lessons.map((l) => (
                <Link
                  key={l.id}
                  to={`/learn/lesson/${l.id}`}
                  style={{
                    display: "block",
                    padding: "8px 0",
                    borderBottom: "1px solid var(--border)",
                    color: l.id === lesson.id ? "var(--blue)" : "var(--text)",
                    fontWeight: l.id === lesson.id ? 600 : 400,
                  }}
                >
                  {l.title}
                  <div style={{ fontSize: 11.5, color: "var(--text-muted)" }}>
                    {Math.round(l.duration_seconds / 60)} min · {l.progress.status.replace("_", " ")}
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
