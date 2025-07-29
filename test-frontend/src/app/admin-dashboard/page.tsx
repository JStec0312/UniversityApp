"use client";
import { useUser } from "@/app/UserContext";
import { usePathname } from "next/navigation";
import Link from "next/link";
import { useAdmin } from "../AdminContext";
import Admin from "@/types/Admin";
export default function AdminDashboardPage() {
  const {admin } = useAdmin();
  const pathname = usePathname(); // np. "/dashboard"
  const base = pathname.endsWith("/") ? pathname.slice(0, -1) : pathname;
  const go = (sub) => `${base}${sub}`;
  return (
    <div>
      <h1>Admin Dashboard</h1>
      <p>Welcome to the admin dashboard!</p>
      <p>Loged as: </p>
      <div className="flex flex-row items-center justify-center gap-8 mt-8">
        <Link href={go("/add-event")} className="px-4 py-2 border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">
          Create Event
        </Link>
      </div>
    </div>
  );
}