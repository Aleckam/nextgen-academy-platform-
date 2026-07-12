export function roleHome(role) {
  switch (role) {
    case "school_admin":
      return "/school/dashboard";
    case "teacher":
      return "/school/teacher";
    case "student":
      return "/learn/dashboard";
    case "parent":
      return "/learn/parent";
    case "super_admin":
      return "/admin/dashboard";
    default:
      return "/";
  }
}
