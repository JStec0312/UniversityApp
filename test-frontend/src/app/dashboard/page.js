"use client";

import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { logout } from "@/api/authApi";
import { useUser } from "@/context/UserContext";

export default function DashboardPage() {
  const { user } = useUser();
  const router = useRouter();
  const pathname = usePathname(); // np. "/dashboard"
  const base = pathname.endsWith("/") ? pathname.slice(0, -1) : pathname;

  const handleLogout = async () => {
    try {
      await logout();
      user.setUser(null); 
      router.push("/");
    } catch (error) {
      console.error("Logout error:", error);
      alert("An error occurred while logging out. Please try again.");
    }
  };

  const go = (sub) => `${base}${sub}`;
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <p className="text-gray-600">This is the dashboard page.</p>
      <button onClick={handleLogout}>Logout</button>
      <ul className="flex flex-row items-center justify-center gap-8 mt-8">
        <li><Link href={go("/announcements")}>Ogłoszenia</Link></li>
        <li><Link href={go("/groups")}>Grupy</Link></li>
        <li><Link href={go("/discounts")}>Zniżki</Link></li>
        <li><Link href={go("/events")}>Wydarzenia</Link></li>
        <li><Link href={go("/profile")}>Profil</Link></li>
      </ul>
    </div>
  );
}
