import { useNavigate } from "react-router-dom";
import { formations } from "../data/courseData";
import { BookOpen, Clock, ArrowRight, Sparkles, GraduationCap } from "lucide-react";
import ParticlesBg from "../components/ParticlesBg";

const IMAGES = {
  python: "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800&q=80",
  "machine-learning": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80",
};

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <>
      <ParticlesBg />
      <div className="home-page">
        <div className="home-hero anim">
          <div className="home-badge">
            <Sparkles size={13} />
            Plateforme de formation
          </div>
          <h1 className="home-title">
            Apprenez à coder,<br />
            <span className="grad">maîtrisez l'avenir.</span>
          </h1>
          <p className="home-subtitle">
            Des formations complètes et progressives pour devenir un développeur Python
            et un expert en Intelligence Artificielle.
          </p>
          <div className="home-stats anim anim-d2">
            <div><div className="home-stat-value">40+</div><div className="home-stat-label">Cours & TP</div></div>
            <div><div className="home-stat-value">3</div><div className="home-stat-label">Niveaux</div></div>
            <div><div className="home-stat-value">7</div><div className="home-stat-label">Examens</div></div>
            <div><div className="home-stat-value">6</div><div className="home-stat-label">Projets</div></div>
          </div>
          <div className="anim anim-d3" style={{ marginTop: "2rem" }}>
            <button className="pr-cta" style={{ maxWidth: 340, margin: "0 auto", fontSize: "0.95rem", padding: "0.85rem" }} onClick={() => navigate("/pricing")}>
              <Sparkles size={16} />
              Voir le tarif —  a partir de 350€
            </button>
          </div>
        </div>

        <div className="formations-grid stagger">
          {formations.map((f) => (
            <div
              key={f.id}
              className={`formation-card ${!f.available ? "unavailable" : ""}`}
              onClick={() => f.available && navigate(`/${f.id}`)}
            >
              <div className="fc-img">
                <img src={IMAGES[f.id]} alt={f.title} loading="lazy" />
                <div className="fc-badge">
                  {f.available
                    ? <><BookOpen size={12} /> {f.levels?.length || 0} niveaux</>
                    : <><Clock size={12} /> Bientôt</>}
                </div>
              </div>
              <div className="fc-body">
                <div className="fc-row">
                  <div className="fc-icon" style={{
                    background: f.id === "python"
                      ? "linear-gradient(135deg,#2563eb,#7c3aed)"
                      : "linear-gradient(135deg,#7c3aed,#a855f7)",
                    boxShadow: f.id === "python"
                      ? "0 4px 14px rgba(37,99,235,0.3)"
                      : "0 4px 14px rgba(124,58,237,0.3)",
                  }}>
                    {f.id === "python" ? "🐍" : "🧠"}
                  </div>
                  <div>
                    <h2 className="fc-title">{f.title}</h2>
                    <p className="fc-subtitle">{f.subtitle}</p>
                  </div>
                </div>
                <p className="fc-desc">{f.description}</p>
                <div className="fc-tags">
                  {f.available ? (
                    <>
                      <span className="fc-tag"><GraduationCap size={12} /> Débutant → Avancé</span>
                      <span className="fc-tag enter">Commencer <ArrowRight size={12} /></span>
                    </>
                  ) : (
                    <span className="fc-tag coming"><Clock size={12} /> Bientôt disponible</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
