import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { correctionsData } from "../data/courseData";
import { useCourse } from "../context/CourseContext";
import NotebookRenderer from "../components/NotebookRenderer";
import UnlockModal from "../components/UnlockModal";
import ParticlesBg from "../components/ParticlesBg";
import { ArrowLeft, FolderOpen, FileCheck, ChevronRight, Lock, KeyRound } from "lucide-react";

export default function CorrectionsPage() {
  const navigate = useNavigate();
  const { isFullyUnlocked } = useCourse();
  const [viewingFile, setViewingFile] = useState(null);
  const [showModal, setShowModal] = useState(false);

  if (!isFullyUnlocked) {
    return (
      <>
        <ParticlesBg />
        <div className="locked-overlay" style={{ minHeight: "calc(100vh - var(--header-height))" }}>
          <div className="locked-icon-wrap"><Lock size={32} /></div>
          <h2>Accès restreint</h2>
          <p>Entrez le code d'accès pour consulter les corrections.</p>
          <button className="btn-action" onClick={() => setShowModal(true)}>
            <KeyRound size={15} style={{ marginRight: 7, verticalAlign: "middle" }} /> Entrer le code
          </button>
          <button className="btn-ghost" onClick={() => navigate("/python")}>
            <ArrowLeft size={14} style={{ marginRight: 6, verticalAlign: "middle" }} /> Retour
          </button>
        </div>
        {showModal && <UnlockModal onClose={() => setShowModal(false)} />}
      </>
    );
  }

  if (viewingFile) {
    return (
      <div style={{ height: "calc(100vh - var(--header-height))", display: "flex", flexDirection: "column" }}>
        <div className="cv-header">
          <div style={{ display: "flex", alignItems: "center", gap: "0.7rem" }}>
            <button onClick={() => setViewingFile(null)} style={{
              display: "flex", alignItems: "center", justifyContent: "center",
              width: 34, height: 34, borderRadius: 10,
              background: "var(--bg-card)", border: "1px solid var(--border-subtle)",
            }}>
              <ArrowLeft size={15} />
            </button>
            <h1 className="cv-title">{viewingFile.title}</h1>
          </div>
        </div>
        <div className="cv-body" style={{ flex: 1, overflow: "auto" }}>
          <NotebookRenderer filepath={viewingFile.path} isMd={viewingFile.isMd || false} />
        </div>
      </div>
    );
  }

  return (
    <>
      <ParticlesBg />
      <div className="corrections-page anim">
        <button className="back-btn" onClick={() => navigate("/python")}>
          <ArrowLeft size={13} /> Retour aux niveaux
        </button>
        <h1 style={{ marginTop: "0.75rem" }}>📝 Corrections</h1>
        <p>Retrouvez ici les corrections des projets et des examens.</p>

        <div className="cor-section">
          <h3 className="cor-section-title"><FolderOpen size={17} /> Corrections des projets</h3>
          <div className="cor-list stagger">
            {correctionsData.projets.map((projet) => (
              <div key={projet.id}>
                <div className="cor-item" style={{ background: "var(--bg-elevated)", fontWeight: 600 }}>
                  <div className="cor-icon" style={{ background: "rgba(99,102,241,0.07)", color: "var(--indigo-400)" }}>
                    <FolderOpen size={16} />
                  </div>
                  <span className="cor-title">{projet.title}</span>
                </div>
                {projet.files.map((file, fi) => (
                  <div key={fi} className="cor-item" style={{ marginLeft: "1.25rem" }}
                    onClick={() => setViewingFile({
                      title: file.title,
                      path: `/courses/python/corrections/${projet.folder}/${file.filename}`,
                    })}>
                    <div className="cor-icon"><FileCheck size={15} /></div>
                    <span className="cor-title">{file.title}</span>
                    <ChevronRight size={13} style={{ marginLeft: "auto", color: "var(--text-muted)" }} />
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>

        <div className="cor-section">
          <h3 className="cor-section-title"><FileCheck size={17} /> Corrections des examens</h3>
          <div className="cor-list stagger">
            {correctionsData.examens.map((exam, idx) => (
              <div key={idx} className="cor-item"
                onClick={() => setViewingFile({
                  title: exam.title,
                  path: `/courses/python/corrections/Corrections examens/${exam.filename}`,
                })}>
                <div className="cor-icon"><FileCheck size={15} /></div>
                <span className="cor-title">{exam.title}</span>
                <ChevronRight size={13} style={{ marginLeft: "auto", color: "var(--text-muted)" }} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
