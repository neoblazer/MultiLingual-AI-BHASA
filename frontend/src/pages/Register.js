import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Auth.css";
import { useAuth } from "../auth/AuthContext";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);
  const { register } = useAuth();
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("Passwords don't match.");
      return;
    }
    // Placeholder sign-up — see AuthContext.js for what changes once
    // the backend exposes a real JWT register endpoint.
    register(email);
    navigate("/");
  }

  return (
    <div className="auth">
      <div className="auth__card">
        <h1 className="auth__title">Create your account</h1>
        <p className="auth__sub">Sign up to save translations and pick up where you left off.</p>

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
          <div className="auth__field">
            <label htmlFor="confirmPassword">Confirm password</label>
            <input
              id="confirmPassword"
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>
          {error && <p style={{ color: "var(--danger)", fontSize: "0.85rem" }}>{error}</p>}
          <button type="submit" className="auth__submit">Create account</button>
        </form>

        <p className="auth__footer">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
        <p className="auth__note">
          Sign-up is a placeholder for now — connect it once JWT registration is added on the backend.
        </p>
      </div>
    </div>
  );
}
