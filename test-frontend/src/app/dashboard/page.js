"use client";

import { useContext, useEffect } from "react";
import { useRouter } from "next/navigation";
import { logout } from "@/api/authApi";



export default function DashboardPage() {
  
  const router = useRouter();

  const handleLogout = async () => {
    try{
      const response = await logout();
      router.push('/'); // Redirect to home page after logout
    } catch (error) {
      console.error("Logout error:", error);
      alert('An error occurred while logging out. Please try again.');
    }
  }

  return(
        <div className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
        <p className="text-gray-600">This is the dashboard page.</p>
        <button onClick = {handleLogout}>Logout</button>
        </div>
    );
}