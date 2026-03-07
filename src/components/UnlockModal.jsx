import { useState } from "react";
import { Lock, KeyRound } from "lucide-react";
import { useCourse } from "../context/CourseContext";

export default function UnlockModal({ onClose }) {
  const [code, setCode] = useState("");
  const [error, setError] = useState(false);
  const { enterCode } = useCourse();

  const handleSubmit = () => {
    const success = enterCode(code.trim());
    if (success) {
      onClose();
    } else {
      setError(true);
      setTimeout(() => setError(false), 1500);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSubmit();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-icon">
          <KeyRound size={28} color="white" />
        </div>
        <h2 className="modal-title">Débloquer tous les cours</h2>
        <p className="modal-desc">
          Entrez le code d'accès pour débloquer l'ensemble des cours, examens et corrections.
        </p>
        <input
          type="text"
          className={`modal-input ${error ? "error" : ""}`}
          placeholder="Code d'accès"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          onKeyDown={handleKeyDown}
          autoFocus
        />
        {error && <p className="modal-error">Code incorrect. Réessayez.</p>}
        <button className="modal-submit" onClick={handleSubmit}>
          Débloquer
        </button>
        <button className="modal-cancel" onClick={onClose}>
          Annuler
        </button>
      </div>
    </div>
  );
}
