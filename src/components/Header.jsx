import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Lock, Unlock, Menu, X, Home, Code2, Brain, CreditCard } from "lucide-react";
import { useCourse } from "../context/CourseContext";
import UnlockModal from "./UnlockModal";

export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();
  const { isFullyUnlocked } = useCourse();
  const [showModal, setShowModal] = useState(false);
  const [mobileNav, setMobileNav] = useState(false);

  // Close mobile nav on route change
  useEffect(() => {
    setMobileNav(false);
  }, [location.pathname]);

  // Prevent body scroll when mobile nav is open
  useEffect(() => {
    if (mobileNav) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => { document.body.style.overflow = ""; };
  }, [mobileNav]);

  const navItems = [
    { path: "/", label: "Accueil", icon: <Home size={18} /> },
    { path: "/python", label: "Python", icon: <Code2 size={18} />, match: "/python" },
    { path: "/machine-learning", label: "Machine Learning", icon: <Brain size={18} /> },
    { path: "/pricing", label: "Tarif", icon: <CreditCard size={18} /> },
  ];

  const isActive = (item) => {
    if (item.match) return location.pathname.startsWith(item.match);
    return location.pathname === item.path;
  };

  return (
    <>
      <header className="top-header">
        <div className="header-logo" onClick={() => navigate("/")}>
          <div className="header-logo-icon">🐍</div>
          <span>CodeAcademy</span>
        </div>

        <div className="header-nav">
          {navItems.map((item) => (
            <button
              key={item.path}
              className={`header-nav-btn ${isActive(item) ? "active" : ""}`}
              onClick={() => navigate(item.path)}
            >
              {item.label}
            </button>
          ))}

          {!isFullyUnlocked ? (
            <button className="header-unlock-btn" onClick={() => setShowModal(true)}>
              <Lock size={13} style={{ marginRight: 6, verticalAlign: "middle" }} />
              Débloquer
            </button>
          ) : (
            <button className="header-unlock-btn unlocked">
              <Unlock size={13} style={{ marginRight: 6, verticalAlign: "middle" }} />
              Débloqué
            </button>
          )}
        </div>

        <button className="mobile-menu-btn" onClick={() => setMobileNav(!mobileNav)}>
          {mobileNav ? <X size={22} /> : <Menu size={22} />}
        </button>
      </header>

      {/* Full-screen mobile nav */}
      {mobileNav && (
        <>
          <div className="mobile-nav-overlay" onClick={() => setMobileNav(false)} />
          <div className="mobile-nav-dropdown">
            {navItems.map((item) => (
              <button
                key={item.path}
                className={`header-nav-btn ${isActive(item) ? "active" : ""}`}
                onClick={() => navigate(item.path)}
              >
                {item.icon}
                <span style={{ marginLeft: 10 }}>{item.label}</span>
              </button>
            ))}

            <div className="mobile-nav-separator" />

            {!isFullyUnlocked ? (
              <button className="header-unlock-btn" onClick={() => { setShowModal(true); setMobileNav(false); }}>
                <Lock size={14} style={{ marginRight: 8 }} />
                Débloquer tous les cours
              </button>
            ) : (
              <button className="header-unlock-btn unlocked">
                <Unlock size={14} style={{ marginRight: 8 }} />
                Tous les cours débloqués
              </button>
            )}
          </div>
        </>
      )}

      {showModal && <UnlockModal onClose={() => setShowModal(false)} />}
    </>
  );
}
