// context/UserContext.js
import { createContext } from "react";

const UserContext = createContext({
  user: null,
  setUser: () => {},
  isAuthenticated: false,
  hasRole: () => false
});

export default UserContext;
