"use client";
import "./globals.css";
import { useEffect, useState } from "react";
import { fetchStudentMe } from "@/api/fetchUserMe";
import { useRouter } from "next/navigation";

import UserContext from "@/context/UserContext";


export default function RootLayout({ children }) {
  const [user, setUser] = useState(null);
  const router = useRouter();
  useEffect(() => {
    const loadUser = async () => {
      try {
        const me = await fetchStudentMe();
        setUser(me);
        router.push("/dashboard");
      } catch (err) {
        console.log("Nie zalogowany");
      }
    };

    loadUser();
  }, []);

  return (
    <html lang="pl">
      <body>
        <UserContext.Provider value={{ user, setUser }}>
          {children}
        </UserContext.Provider>
      </body>
    </html>
  );
}