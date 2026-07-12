import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import ProtectedRoute from "./routes/ProtectedRoute";
import "./styles/theme.css";

import HomePage from "./pages/public/HomePage";
import ProgrammePage from "./pages/public/ProgrammePage";
import PricingPage from "./pages/public/PricingPage";
import SignUpPage from "./pages/public/SignUpPage";
import LoginPage from "./pages/public/LoginPage";
import BlogListPage from "./pages/public/BlogListPage";
import BlogArticlePage from "./pages/public/BlogArticlePage";
import CertificateVerifyPage from "./pages/public/CertificateVerifyPage";

import KidsDashboard from "./pages/learner/KidsDashboard";
import TeenDashboard from "./pages/learner/TeenDashboard";
import ProfessionalDashboard from "./pages/learner/ProfessionalDashboard";
import ParentDashboard from "./pages/learner/ParentDashboard";
import LessonPlayer from "./pages/learner/LessonPlayer";
import Quiz from "./pages/learner/Quiz";
import ModuleListing from "./pages/learner/ModuleListing";
import CertificatePage from "./pages/learner/CertificatePage";
import ProfileSettings from "./pages/learner/ProfileSettings";
import PaymentSubscription from "./pages/learner/PaymentSubscription";

import SchoolDashboard from "./pages/school/SchoolDashboard";
import CsvUploadPinCard from "./pages/school/CsvUploadPinCard";
import ClassView from "./pages/school/ClassView";
import StudentRoster from "./pages/school/StudentRoster";
import TeacherDashboard from "./pages/school/TeacherDashboard";
import SchoolSubscription from "./pages/school/SchoolSubscription";

import AdminDashboard from "./pages/admin/AdminDashboard";
import ContentCMS from "./pages/admin/ContentCMS";
import BlogCMS from "./pages/admin/BlogCMS";
import UserManagement from "./pages/admin/UserManagement";
import SchoolManagement from "./pages/admin/SchoolManagement";
import SubscriptionAdmin from "./pages/admin/SubscriptionAdmin";
import AnalyticsDashboard from "./pages/admin/AnalyticsDashboard";
import CertificateTemplateManagement from "./pages/admin/CertificateTemplateManagement";

const SCHOOL_STAFF = ["school_admin", "super_admin"];
const TEACHER = ["teacher", "school_admin", "super_admin"];
const LEARNER = ["student", "parent"];
const ADMIN = ["super_admin"];

// Routes a logged-in "student" role to the right age-tier dashboard.
// Professionals are also role=student (see backend/app/api/auth.py) but
// distinguished by account_type/age_group.
function LearnerHome() {
  const { user } = useAuth();
  if (user?.age_group === "professional") return <ProfessionalDashboard />;
  if (user?.age_group === "7-12") return <KidsDashboard />;
  return <TeenDashboard />;
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public */}
          <Route path="/" element={<HomePage />} />
          <Route path="/programmes/:ageGroup" element={<ProgrammePage />} />
          <Route path="/pricing" element={<PricingPage />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/blog" element={<BlogListPage />} />
          <Route path="/blog/:slug" element={<BlogArticlePage />} />
          <Route path="/verify/:code" element={<CertificateVerifyPage />} />

          {/* Learner App */}
          <Route path="/learn/dashboard" element={<ProtectedRoute roles={LEARNER}><LearnerHome /></ProtectedRoute>} />
          <Route path="/learn/parent" element={<ProtectedRoute roles={["parent"]}><ParentDashboard /></ProtectedRoute>} />
          <Route path="/learn/modules" element={<ProtectedRoute roles={LEARNER}><ModuleListing /></ProtectedRoute>} />
          <Route path="/learn/lesson/:lessonId" element={<ProtectedRoute roles={LEARNER}><LessonPlayer /></ProtectedRoute>} />
          <Route path="/learn/quiz/:quizId" element={<ProtectedRoute roles={LEARNER}><Quiz /></ProtectedRoute>} />
          <Route path="/learn/certificates" element={<ProtectedRoute roles={LEARNER}><CertificatePage /></ProtectedRoute>} />
          <Route path="/learn/profile" element={<ProtectedRoute roles={LEARNER}><ProfileSettings /></ProtectedRoute>} />
          <Route path="/learn/subscription" element={<ProtectedRoute roles={LEARNER}><PaymentSubscription /></ProtectedRoute>} />

          {/* School Portal */}
          <Route path="/school/dashboard" element={<ProtectedRoute roles={SCHOOL_STAFF}><SchoolDashboard /></ProtectedRoute>} />
          <Route path="/school/upload" element={<ProtectedRoute roles={SCHOOL_STAFF}><CsvUploadPinCard /></ProtectedRoute>} />
          <Route path="/school/classes/:classId" element={<ProtectedRoute roles={TEACHER}><ClassView /></ProtectedRoute>} />
          <Route path="/school/students" element={<ProtectedRoute roles={SCHOOL_STAFF}><StudentRoster /></ProtectedRoute>} />
          <Route path="/school/teacher" element={<ProtectedRoute roles={TEACHER}><TeacherDashboard /></ProtectedRoute>} />
          <Route path="/school/subscription" element={<ProtectedRoute roles={SCHOOL_STAFF}><SchoolSubscription /></ProtectedRoute>} />

          {/* Admin Panel */}
          <Route path="/admin/dashboard" element={<ProtectedRoute roles={ADMIN}><AdminDashboard /></ProtectedRoute>} />
          <Route path="/admin/content" element={<ProtectedRoute roles={ADMIN}><ContentCMS /></ProtectedRoute>} />
          <Route path="/admin/blog" element={<ProtectedRoute roles={ADMIN}><BlogCMS /></ProtectedRoute>} />
          <Route path="/admin/users" element={<ProtectedRoute roles={ADMIN}><UserManagement /></ProtectedRoute>} />
          <Route path="/admin/schools" element={<ProtectedRoute roles={ADMIN}><SchoolManagement /></ProtectedRoute>} />
          <Route path="/admin/subscriptions" element={<ProtectedRoute roles={ADMIN}><SubscriptionAdmin /></ProtectedRoute>} />
          <Route path="/admin/analytics" element={<ProtectedRoute roles={ADMIN}><AnalyticsDashboard /></ProtectedRoute>} />
          <Route path="/admin/certificate-templates" element={<ProtectedRoute roles={ADMIN}><CertificateTemplateManagement /></ProtectedRoute>} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
