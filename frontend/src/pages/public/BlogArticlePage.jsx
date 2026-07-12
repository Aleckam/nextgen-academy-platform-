import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import client from "../../api/client";
import PublicLayout from "../../components/PublicLayout";

export default function BlogArticlePage() {
  const { slug } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    client.get(`/blog/${slug}`).then((res) => setData(res.data));
  }, [slug]);

  if (!data) return <PublicLayout><div className="card">Loading…</div></PublicLayout>;

  return (
    <PublicLayout>
      <span className="badge on-track">{data.post.category}</span>
      <h1>{data.post.title}</h1>
      <div className="card" style={{ marginBottom: 20 }}>{data.body}</div>

      <div className="card" style={{ marginBottom: 20 }}>
        <strong>Subscribe for weekly financial literacy tips</strong>
        <form
          style={{ display: "flex", gap: 8, marginTop: 10 }}
          onSubmit={(e) => {
            e.preventDefault();
            const email = e.target.elements.email.value;
            client.post("/blog/newsletter-signup", { email });
            e.target.reset();
          }}
        >
          <input name="email" type="email" placeholder="you@example.com" style={{ flex: 1, padding: 8, borderRadius: 6, border: "1px solid var(--border)" }} />
          <button className="btn primary">Subscribe</button>
        </form>
      </div>

      {data.related.length > 0 && (
        <div>
          <strong>Related articles</strong>
          {data.related.map((r) => (
            <Link key={r.id} to={`/blog/${r.slug}`} style={{ display: "block", marginTop: 8 }}>{r.title}</Link>
          ))}
        </div>
      )}
    </PublicLayout>
  );
}
