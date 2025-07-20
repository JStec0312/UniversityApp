"use client";
import { useUser } from "@/app/UserContext";

export default function AdminDashboardPage() {
  const { user } = useUser();
  return (
    <div>
      <h1>Admin Dashboard</h1>
      <p>Welcome to the admin dashboard!</p>
    </div>
  );
}