import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useCourse } from "../context/CourseContext";
import { getCoursesByLevel, pythonLevels } from "../data/courseData";
import NotebookRenderer from "../components/NotebookRenderer";
import UnlockModal from "../components/UnlockModal";
import { ArrowLeft, Check, Lock, ChevronRight, Menu, KeyRound, Unlock } from "lucide-react";

const folderMap = { debutant: "debutant", intermediaire: "intermediaire", avance: "avance", examens: "examens" };

export default function CourseViewerPage() {
  const { levelId } = useParams();
  const navigate = useNavigate();
  const { isFullyUnlocked, isCourseAccessible, isCourseCompleted, markComplete, getProgress } = useCourse();

  const courses = getCoursesByLevel(levelId);
  const levelInfo = pythonLevels.find((l) => l.id === levelId);
  const [activeCourse, setActiveCourse] = useState(null);
  const [activeIndex, setActiveIndex] = useState(0);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [showLockedMsg, setShowLockedMsg] = useState(false);

  useEffect(() => {
    setActiveCourse(null);
    setActiveIndex(0);
    if (courses.length > 0) {
      setActiveCourse(courses[0]);
      setActiveIndex(0);
    }
  }, [levelId]);

  if (!levelInfo) {
    return (
      <div className="coming-soon-page">
        <h1>Niveau introuvable</h1>
        <button className="btn-ghost" onClick={() => navigate("/python")}>Retour</button>
      </div>
    );
  }

  const progress = getProgress(levelId, courses);
  const folder = folderMap[levelId] || levelId;
  const getFilepath = (course) => `/courses/python/${folder}/${course.filename}`;

  const handleCourseClick = (course, index) => {
    if (!isCourseAccessible(levelId, index)) {
      setShowLockedMsg(true);
      setTimeout(() => setShowLockedMsg(false), 2500);
      return;
    }
    setActiveCourse(course);
    setActiveIndex(index);
    setSidebarOpen(false);
  };

  const handleComplete = () => {
    if (activeCourse) markComplete(levelId, activeCourse.id);
  };

  const handleNext = () => {
    if (activeIndex < courses.length - 1) {
      const nextIdx = activeIndex + 1;
      if (isCourseAccessible(levelId, nextIdx)) {
        setActiveCourse(courses[nextIdx]);
        setActiveIndex(nextIdx);
      }
    }
  };

  return (
    <div className="course-list-page">
      <div className={`mobile-overlay ${sidebarOpen ? "open" : ""}`} onClick={() => setSidebarOpen(false)} />

      {/* Sidebar */}
      <aside className={`course-sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sb-header">
          <button className="back-btn" onClick={() => navigate("/python")}>
            <ArrowLeft size={13} /> Retour
          </button>
          <h2 className="sb-level-title">{levelInfo.title}</h2>
          <p style={{ fontSize: "0.78rem", color: "var(--text-muted)", marginTop: "0.1rem" }}>
            {levelInfo.subtitle}
          </p>
          <div className="sb-progress">
            <div className="sb-progress-bar">
              <div className="sb-progress-fill" style={{ width: `${progress}%` }} />
            </div>
            <span className="sb-progress-text">{progress}% complété · {courses.length} cours</span>
          </div>
        </div>

        <div className="sb-courses">
          {/* Locked toast */}
          {showLockedMsg && (
            <div style={{
              padding: "0.6rem 0.85rem",
              margin: "0.35rem 0.35rem 0.5rem",
              background: "rgba(239,68,68,0.08)",
              border: "1px solid rgba(239,68,68,0.15)",
              borderRadius: "9px",
              fontSize: "0.78rem",
              color: "var(--red-400)",
              display: "flex",
              alignItems: "center",
              gap: "0.4rem",
              animation: "fadeInUp 0.25s ease",
            }}>
              <Lock size={13} />
              Cours verrouillé — entrez le code d'accès
            </div>
          )}

          {courses.map((course, index) => {
            const accessible = isCourseAccessible(levelId, index);
            const completed = isCourseCompleted(levelId, course.id);
            const isActive = activeCourse?.id === course.id;
            const isFree = index === 0 && !isFullyUnlocked;

            return (
              <div
                key={course.id}
                className={`sb-item ${isActive ? "active" : ""} ${completed ? "completed" : ""} ${!accessible ? "locked" : ""} ${isFree ? "free" : ""}`}
                onClick={() => handleCourseClick(course, index)}
              >
                <div className="sb-num">
                  {completed ? <Check size={12} /> : accessible ? String(index + 1).padStart(2, "0") : <Lock size={10} />}
                </div>
                <div className="sb-info">
                  <div className="sb-title">{course.title}</div>
                  <div className="sb-dur">{course.duration}</div>
                </div>
                {isFree && <span className="sb-free-tag">GRATUIT</span>}
                <div className={`sb-status ${completed ? "completed" : !accessible ? "locked" : isFree ? "free" : ""}`} />
              </div>
            );
          })}

          {!isFullyUnlocked && (
            <div style={{ padding: "1rem 0.5rem", borderTop: "1px solid var(--border-subtle)", marginTop: "0.5rem" }}>
              <button className="btn-action" style={{ width: "100%", fontSize: "0.82rem", padding: "0.6rem" }} onClick={() => setShowModal(true)}>
                <KeyRound size={14} style={{ marginRight: 6, verticalAlign: "middle" }} />
                Débloquer tous les cours
              </button>
            </div>
          )}
        </div>
      </aside>

      {/* Main viewer */}
      <div className="course-viewer">
        <button className="mobile-courses-btn" onClick={() => setSidebarOpen(true)}>
          <Menu size={15} /> Voir les cours ({courses.length})
        </button>

        {activeCourse ? (
          isCourseAccessible(levelId, activeIndex) ? (
            <>
              <div className="cv-header">
                <div>
                  <div style={{ fontSize: "0.73rem", color: "var(--text-muted)", marginBottom: "0.15rem" }}>
                    {levelInfo.title} · Cours {activeIndex + 1}/{courses.length}
                  </div>
                  <h1 className="cv-title">{activeCourse.title}</h1>
                </div>
                <div style={{ display: "flex", gap: "0.5rem" }}>
                  {isCourseCompleted(levelId, activeCourse.id) ? (
                    <button className="btn-complete done">
                      <Check size={15} style={{ marginRight: 5, verticalAlign: "middle" }} /> Terminé
                    </button>
                  ) : (
                    <button className="btn-complete" onClick={handleComplete}>
                      Marquer terminé
                    </button>
                  )}
                </div>
              </div>
              <div className="cv-body">
                <NotebookRenderer
                  key={`${levelId}-${activeCourse.id}`}
                  filepath={getFilepath(activeCourse)}
                  isMd={activeCourse.isMd || false}
                />
                <div style={{ display: "flex", justifyContent: "flex-end", marginTop: "1.75rem", paddingTop: "1.25rem", borderTop: "1px solid var(--border-subtle)" }}>
                  {!isCourseCompleted(levelId, activeCourse.id) && (
                    <button className="btn-complete" onClick={() => { handleComplete(); handleNext(); }}>
                      Terminer et continuer <ChevronRight size={15} style={{ marginLeft: 3, verticalAlign: "middle" }} />
                    </button>
                  )}
                </div>
              </div>
            </>
          ) : (
            /* Locked course view */
            <div className="locked-overlay">
              <div className="locked-icon-wrap"><Lock size={32} /></div>
              <h2>Cours verrouillé</h2>
              <p>Ce cours nécessite le code d'accès pour être consulté.</p>
              <p className="hint">Le premier cours de chaque module est gratuit.</p>
              <button className="btn-action" onClick={() => setShowModal(true)}>
                <KeyRound size={15} style={{ marginRight: 7, verticalAlign: "middle" }} />
                Débloquer
              </button>
              <button className="btn-ghost" onClick={() => { setActiveCourse(courses[0]); setActiveIndex(0); }}>
                <ArrowLeft size={14} style={{ marginRight: 6, verticalAlign: "middle" }} />
                Voir le cours gratuit
              </button>
            </div>
          )
        ) : (
          <div className="cv-welcome">
            <div className="cv-welcome-icon">📖</div>
            <h2>Sélectionnez un cours</h2>
            <p>Choisissez un cours dans la liste pour commencer.</p>
          </div>
        )}
      </div>

      {showModal && <UnlockModal onClose={() => setShowModal(false)} />}
    </div>
  );
}
