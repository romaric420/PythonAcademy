import { useNavigate } from "react-router-dom";
import { useCourse } from "../context/CourseContext";
import { pythonLevels, debutantCourses, intermediaireCourses, avanceCourses, examensCourses } from "../data/courseData";
import { Sprout, Flame, Rocket, ClipboardList, CheckCircle, ArrowLeft, Unlock } from "lucide-react";
import ParticlesBg from "../components/ParticlesBg";

const levelIcons = {
  debutant: <Sprout size={18} />,
  intermediaire: <Flame size={18} />,
  avance: <Rocket size={18} />,
  examens: <ClipboardList size={18} />,
  corrections: <CheckCircle size={18} />,
};

const levelColors = {
  debutant:      { bg: "rgba(16,185,129,0.1)",  color: "#10b981", bar: "linear-gradient(90deg,#10b981,#34d399)" },
  intermediaire: { bg: "rgba(245,158,11,0.1)",   color: "#f59e0b", bar: "linear-gradient(90deg,#f59e0b,#fbbf24)" },
  avance:        { bg: "rgba(239,68,68,0.1)",    color: "#ef4444", bar: "linear-gradient(90deg,#ef4444,#f87171)" },
  examens:       { bg: "rgba(99,102,241,0.1)",   color: "#6366f1", bar: "linear-gradient(90deg,#6366f1,#818cf8)" },
  corrections:   { bg: "rgba(6,182,212,0.1)",    color: "#06b6d4", bar: "linear-gradient(90deg,#06b6d4,#22d3ee)" },
};

const coursesMap = { debutant: debutantCourses, intermediaire: intermediaireCourses, avance: avanceCourses, examens: examensCourses };

export default function PythonPage() {
  const navigate = useNavigate();
  const { isFullyUnlocked, getProgress } = useCourse();

  const handleClick = (level) => {
    if (level.id === "corrections") {
      navigate("/python/corrections");
    } else {
      navigate(`/python/${level.id}`);
    }
  };

  return (
    <>
      <ParticlesBg />
      <div className="python-page">
        <div className="python-header anim">
          <button className="back-btn" onClick={() => navigate("/")}>
            <ArrowLeft size={14} /> Retour aux formations
          </button>
          <h1>🐍 Formation Python</h1>
          <p>
            {isFullyUnlocked
              ? "Tous les cours sont débloqués. Bonne formation !"
              : "Le premier cours de chaque module est gratuit. Débloquez tout avec le code d'accès."}
          </p>
        </div>

        <div className="levels-grid stagger">
          {pythonLevels.map((level, idx) => {
            const courses = coursesMap[level.id] || [];
            const progress = getProgress(level.id, courses);
            const c = levelColors[level.id];

            return (
              <div key={level.id} className="level-card" onClick={() => handleClick(level)}>
                <div className="lc-img">
                  <img src={level.image} alt={level.title} loading="lazy" />
                  <div className="lc-num">{String(idx + 1).padStart(2, "0")}</div>
                </div>
                <div className="lc-body">
                  <div className="lc-icon" style={{ background: c.bg, color: c.color }}>
                    {levelIcons[level.id]}
                  </div>
                  <h3 className="lc-title">{level.title}</h3>
                  <p className="lc-subtitle">{level.subtitle}</p>
                  {courses.length > 0 && (
                    <>
                      <div className="lc-progress">
                        <div className="lc-progress-bar" style={{ width: `${progress}%`, background: c.bar }} />
                      </div>
                      <p className="lc-progress-text">{progress}% complété · {courses.length} cours</p>
                    </>
                  )}
                  {!isFullyUnlocked && (
                    <div className="lc-free-badge">
                      <Unlock size={11} /> 1er cours gratuit
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}
