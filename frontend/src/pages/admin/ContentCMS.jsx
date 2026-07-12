import Layout from "../../components/Layout";
import PlaceholderPage from "../../components/PlaceholderPage";

/** Content CMS — lessons & quizzes (§3.2). Backend CRUD already exists:
 * POST /api/content/programmes, /modules, /lessons, /lessons/:id/quiz
 * (see backend/app/api/content.py) — this screen just needs forms wired to them. */
export default function ContentCMS() {
  return (
    <Layout>
      <PlaceholderPage
        title="Content CMS"
        note="Backend CRUD is live (POST /api/content/{programmes,modules,lessons,lessons/:id/quiz}). Build the admin forms against it."
      />
    </Layout>
  );
}
