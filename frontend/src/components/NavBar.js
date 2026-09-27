import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./NavBar.css";
import { useAuth } from "../auth/AuthContext";

export default function NavBar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return (
    <nav className="nav">
      <Link to="/" className="nav__brand">Bhāṣā</Link>

      <div className="nav__links">
        {user ? (
          <>
            <span className="nav__user">Signed in as <strong>{user.email}</strong></span>
            <button className="nav__ghost" onClick={handleLogout}>Log out</button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav__ghost">Log in</Link>
            <Link to="/register" className="nav__cta">Sign up</Link>
          </>
        )}
      </div>
    </nav>
  );
}
