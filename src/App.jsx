import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { CourseProvider } from "./context/CourseContext";
import Header from "./components/Header";
import HomePage from "./pages/HomePage";
import PythonPage from "./pages/PythonPage";
import CourseViewerPage from "./pages/CourseViewerPage";
import CorrectionsPage from "./pages/CorrectionsPage";
import PricingPage from "./pages/PricingPage";
import MLPage from "./pages/MLPage";
import "./styles/global.css";

export default function App() {
  return (
    <CourseProvider>
      <Router>
        <div className="app-layout">
          <div className="main-content">
            <Header />
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/python" element={<PythonPage />} />
              <Route path="/python/corrections" element={<CorrectionsPage />} />
              <Route path="/python/:levelId" element={<CourseViewerPage />} />
              <Route path="/pricing" element={<PricingPage />} />
              <Route path="/machine-learning" element={<MLPage />} />
            </Routes>
          </div>
        </div>
      </Router>
    </CourseProvider>
  );
}
