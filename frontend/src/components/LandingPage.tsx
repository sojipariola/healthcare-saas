//
import React from "react";

const LandingPage: React.FC = () => (
  <div style={{
    minHeight: "100vh",
    background: "linear-gradient(135deg, #4f8cff 0%, #38e8ff 100%)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    color: "#fff",
    fontFamily: "Inter, sans-serif"
  }}>
    <h1 style={{ fontSize: "3rem", fontWeight: 800, marginBottom: "1rem" }}>
      Welcome to ClinicCloud
    </h1>
    <p style={{ fontSize: "1.5rem", maxWidth: 600, textAlign: "center", marginBottom: "2rem" }}>
      The next-generation multi-tenant healthcare SaaS platform. Secure, compliant, and built for modern clinics.
    </p>
    <a
      href="/login"
      style={{
        padding: "1rem 2.5rem",
        background: "#fff",
        color: "#4f8cff",
        borderRadius: "2rem",
        fontWeight: 700,
        fontSize: "1.2rem",
        textDecoration: "none",
        boxShadow: "0 4px 24px rgba(0,0,0,0.08)"
      }}
    >
      Get Started
    </a>
  </div>
);

export default LandingPage;