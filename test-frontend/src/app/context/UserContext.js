"use client";

import React, { createContext, useContext, useEffect, useState } from "react";

// Create the context
const UserContext = createContext(null);
UserContext.displayName = "UserContext";  

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState();

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
