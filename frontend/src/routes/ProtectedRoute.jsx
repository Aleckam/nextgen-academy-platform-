import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

/** RBAC route guard — redirects to login if unauthenticated, or to "/" if
 * the signed-in role isn't in `roles`. Implemented from day one per the
 * MVP scope's RBAC requirement (§2). */
export default function ProtectedRoute({ roles, children }) {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />;

  return children;
}
