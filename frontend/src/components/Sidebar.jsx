import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const NAV_BY_ROLE = {
  school_admin: {
    heading: "School Portal",
    items: [
      { to: "/school/dashboard", label: "Dashboard" },
      { to: "/school/students", label: "Students" },
      { to: "/school/upload", label: "Upload students (CSV)" },
      { to: "/school/classes/1", label: "Classes" },
      { to: "/school/subscription", label: "Subscription" },
    ],
  },
  teacher: {
    heading: "School Portal",
    items: [
      { to: "/school/teacher", label: "My class" },
      { to: "/school/classes/1", label: "Class view" },
    ],
  },
  student: {
    heading: "Learner App",
    items: [
      { to: "/learn/dashboard", label: "Dashboard" },
      { to: "/learn/modules", label: "Modules" },
      { to: "/learn/certificates", label: "Certificates" },
      { to: "/learn/profile", label: "Profile & settings" },
    ],
  },
  parent: {
    heading: "Learner App",
    items: [
      { to: "/learn/parent", label: "Parent dashboard" },
      { to: "/learn/subscription", label: "Subscription" },
    ],
  },
  super_admin: {
    heading: "Admin Panel",
    items: [
      { to: "/admin/dashboard", label: "Overview" },
      { to: "/admin/content", label: "Content CMS" },
      { to: "/admin/blog", label: "Blog CMS" },
      { to: "/admin/users", label: "User management" },
      { to: "/admin/schools", label: "School management" },
      { to: "/admin/subscriptions", label: "Subscriptions & billing" },
      { to: "/admin/analytics", label: "Analytics" },
    ],
  },
};

export default function Sidebar() {
  const { user, logout } = useAuth();
  if (!user) return null;
  const nav = NAV_BY_ROLE[user.role];

  return (
    <aside className="sidebar">
      <div className="brand">
        NextGen
        <small>{nav?.heading || "Academy"}</small>
      </div>
      <nav>
        {nav?.items.map((item) => (
          <NavLink key={item.to} to={item.to} className={({ isActive }) => (isActive ? "active" : "")}>
            <span className="label">{item.label}</span>
          </NavLink>
        ))}
        <div className="nav-heading">Account</div>
        <a onClick={logout} style={{ cursor: "pointer" }}>
          <span className="label">Log out ({user.name})</span>
        </a>
      </nav>
    </aside>
  );
}
