import React, { createContext, useContext, useState } from "react";

/**
 * Placeholder auth state for the frontend shell.
 *
 * There is no real authentication backend yet — the SOP for this
 * project explicitly excludes Spring Security/JWT for now. This
 * context exists so the UI (nav bar, protected-route behavior, etc.)
 * is already structured correctly. Once JWT endpoints exist on the
 * backend (e.g. POST /api/auth/login, POST /api/auth/register), swap
 * the TODO-marked bodies of login()/register() below for real calls
 * to `api` (see src/api/client.js) and nothing else needs to change.
 */
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("bhasa_user");
    return stored ? JSON.parse(stored) : null;
  });

  function login(email) {
    // TODO: replace with a real call once the backend exposes
    // POST /api/auth/login, e.g.:
    //   const { data } = await api.post("/api/auth/login", { email, password });
    //   localStorage.setItem("bhasa_token", data.token);
    const fakeUser = { email };
    localStorage.setItem("bhasa_user", JSON.stringify(fakeUser));
    setUser(fakeUser);
  }

  function register(email) {
    // TODO: replace with a real call to POST /api/auth/register
    const fakeUser = { email };
    localStorage.setItem("bhasa_user", JSON.stringify(fakeUser));
    setUser(fakeUser);
  }

  function logout() {
    localStorage.removeItem("bhasa_user");
    localStorage.removeItem("bhasa_token");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
