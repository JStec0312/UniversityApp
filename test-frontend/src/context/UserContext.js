// src/context/UserContext.js
"use client";
import React, {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

const UserContext = createContext();
UserContext.displayName = "UserContext";  

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState();

  useEffect(() => {
    const stored = localStorage.getItem("user");
    if (stored) {
      try {
        setUser(JSON.parse(stored));
      } catch (err) {
        console.error("Błąd parsowania usera z localStorage");
      }
    }
  }, []);

  useEffect(() => {
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("user");
    }
  }, [user]);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const ctx = useContext(UserContext);
  if (!ctx) {
    throw new Error("useUser musi być używany wewnątrz <UserProvider>");
  }
  return ctx;
};

export const useSetUser = () => useUser().setUser;
