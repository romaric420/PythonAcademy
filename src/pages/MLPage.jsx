import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import ParticlesBg from "../components/ParticlesBg";

export default function MLPage() {
  const navigate = useNavigate();
  return (
    <>
      <ParticlesBg />
      <div className="coming-soon-page">
        <div className="coming-soon-icon">🧠</div>
        <h1>Machine Learning</h1>
        <p>Cette formation est en cours de préparation. Elle couvrira le ML, le Deep Learning et la Data Science appliquée.</p>
        <button className="btn-ghost" onClick={() => navigate("/")}>
          <ArrowLeft size={15} style={{ marginRight: 7, verticalAlign: "middle" }} /> Retour à l'accueil
        </button>
      </div>
    </>
  );
}
