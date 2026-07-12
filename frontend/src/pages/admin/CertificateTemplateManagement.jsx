import Layout from "../../components/Layout";
import PlaceholderPage from "../../components/PlaceholderPage";

/** Certificate template management (§7, Should Have). Certificate PDF
 * rendering already exists in backend/app/utils/pdf.py pattern — add a
 * CertificateTemplate model + a render_certificate_pdf() following the
 * same WeasyPrint approach as the PIN card / term report PDFs. */
export default function CertificateTemplateManagement() {
  return (
    <Layout>
      <PlaceholderPage title="Certificate templates" />
    </Layout>
  );
}
