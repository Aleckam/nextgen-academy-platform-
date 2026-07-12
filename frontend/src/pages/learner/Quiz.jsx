import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import client from "../../api/client";
import Layout from "../../components/Layout";

/** Post-lesson quiz — 5 questions minimum, required before progression (§3.3). */
export default function Quiz() {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  useEffect(() => {
    client.get(`/content/quizzes/${quizId}`).then((res) => setQuiz(res.data));
  }, [quizId]);

  const submit = async () => {
    const res = await client.post(`/content/quizzes/${quizId}/attempt`, { answers });
    setResult(res.data);
  };

  if (!quiz) return <Layout><div className="card">Loading…</div></Layout>;

  if (result) {
    return (
      <Layout>
        <div className="card" style={{ textAlign: "center", padding: 40 }}>
          <span className={`badge ${result.passed ? "on-track" : "error"}`}>
            {result.passed ? "Passed" : "Try again"}
          </span>
          <h2>{result.score_pct}%</h2>
          {result.passed && <p>You earned {result.coin_reward} NextGen Coins.</p>}
          {result.certificate_issued && <p>Module certificate issued — check your Certificates page.</p>}
          <button className="btn primary" onClick={() => navigate("/learn/modules")}>Back to modules</button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="page-header"><h1>Quiz</h1></div>
      {quiz.questions.map((q, i) => (
        <div key={q.id} className="card" style={{ marginBottom: 12 }}>
          <strong>{i + 1}. {q.question_text}</strong>
          <div style={{ marginTop: 8 }}>
            {q.choices.map((c) => (
              <label key={c.id} style={{ display: "block", padding: "6px 0" }}>
                <input
                  type="radio"
                  name={`q${q.id}`}
                  checked={answers[q.id] === c.id}
                  onChange={() => setAnswers({ ...answers, [q.id]: c.id })}
                />{" "}
                {c.text}
              </label>
            ))}
          </div>
        </div>
      ))}
      <button className="btn primary" onClick={submit} disabled={Object.keys(answers).length < quiz.questions.length}>
        Submit quiz
      </button>
    </Layout>
  );
}
