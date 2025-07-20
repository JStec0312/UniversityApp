"use client";

import React, { createContext, useContext, useEffect, useState } from "react";

// Create the context
const UserContext = createContext(null);
UserContext.displayName = "UserContext";  

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState();

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem("user");
      if (stored) {
        try {
          setUser(JSON.parse(stored));
        } catch (err) {
          console.error("Error parsing user from localStorage", err);
        }
      }
    }
  }, []);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      if (user) {
        localStorage.setItem("user", JSON.stringify(user));
      } else {
        localStorage.removeItem("user");
      }
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
    throw new Error("useUser must be used within <UserProvider>");
  }
  return ctx;
};

export const useSetUser = () => useUser().setUser;
