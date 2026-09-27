import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Auth.css";
import { useAuth } from "../auth/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    // Placeholder sign-in — see AuthContext.js for what changes once
    // the backend exposes a real JWT login endpoint.
    login(email);
    navigate("/");
  }

  return (
    <div className="auth">
      <div className="auth__card">
        <h1 className="auth__title">Welcome back</h1>
        <p className="auth__sub">Log in to keep your translation history in one place.</p>

        <form onSubmit={handleSubmit}>
          <div className="auth__field">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
            />
          </div>
          <div className="auth__field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>
          <button type="submit" className="auth__submit">Log in</button>
        </form>

        <p className="auth__footer">
          New here? <Link to="/register">Create an account</Link>
        </p>
        <p className="auth__note">
          Sign-in is a placeholder for now — connect it once JWT login is added on the backend.
        </p>
      </div>
    </div>
  );
}
