import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft, Check, Sparkles, GraduationCap, Users, RefreshCcw,
  GitBranch, Infinity, BookOpen, MessageCircle, Video, Rocket,
  Shield, Star, Zap, ChevronDown, ChevronUp, ArrowRight,
  Code2, Brain, Trophy, Clock, Target, Heart
} from "lucide-react";
import ParticlesBg from "../components/ParticlesBg";

const FEATURES = [
  {
    icon: <GraduationCap size={22} />,
    title: "De Zéro à Expert",
    desc: "Un parcours structuré en 3 niveaux : débutant, intermédiaire et avancé. Chaque étape vous rapproche de la maîtrise totale de Python.",
  },
  {
    icon: <Users size={22} />,
    title: "Accompagnement personnalisé",
    desc: "Un suivi individuel via Discord et des réunions hebdomadaires. Besoin d'aide pour avancer ? Signalez-vous et un membre sera disponible pour vous.",
  },
  {
    icon: <RefreshCcw size={22} />,
    title: "Mises à jour continues",
    desc: "Les cours sont régulièrement mis à jour pour refléter les dernières évolutions de Python et les meilleures pratiques du marché.",
  },
  {
    icon: <GitBranch size={22} />,
    title: "Accès aux repos GitHub",
    desc: "Accès complet aux repositories de tous les cours, projets et exercices. Clonez, pratiquez et construisez votre portfolio.",
  },
  {
    icon: <Infinity size={22} />,
    title: "Accès à vie",
    desc: "Pas d'abonnement, pas de limite de temps. Une fois inscrit, vous gardez l'accès à l'ensemble de la formation pour toujours.",
  },
  {
    icon: <MessageCircle size={22} />,
    title: "Canal Discord privé",
    desc: "Rejoignez notre communauté Discord pour poser vos questions, partager vos préoccupations et obtenir de l'aide en temps réel d'un membre de l'équipe.",
  },
  {
    icon: <Video size={22} />,
    title: "Réunions hebdomadaires",
    desc: "Chaque semaine, une session de suivi est organisée. Besoin d'aide pour avancer ? Signalez-vous et un membre sera disponible pour vous accompagner.",
  },
  {
    icon: <Trophy size={22} />,
    title: "Projets concrets",
    desc: "6 projets guidés de difficulté croissante pour mettre en pratique vos compétences et enrichir votre portfolio professionnel.",
  },
];

const CURRICULUM = [
  {
    level: "Débutant",
    color: "#10b981",
    modules: 17,
    items: [
      "Variables, types, opérateurs",
      "Conditions & boucles",
      "Structures de données (listes, tuples, dictionnaires, ensembles)",
      "Fonctions & gestion de fichiers",
      "Conventions PEP8 & structuration de code",
      "Projet guidé de fin de niveau",
    ],
  },
  {
    level: "Intermédiaire",
    color: "#f59e0b",
    modules: 11,
    items: [
      "Programmation Orientée Objet (POO)",
      "Programmation fonctionnelle",
      "Gestion des exceptions & portée des variables",
      "Récursivité",
      "Modules : collections, itertools, logging, regex, requests",
      "3 projets intermédiaires",
    ],
  },
  {
    level: "Avancé",
    color: "#ef4444",
    modules: 11,
    items: [
      "Tests unitaires",
      "Décorateurs & générateurs",
      "Multithreading & multiprocessing",
      "Programmation asynchrone",
      "Modules : functools, sys, garbage collector",
      "Distribution de packages & projet avancé",
    ],
  },
  {
    level: "Examens & Corrections",
    color: "#6366f1",
    modules: 13,
    items: [
      "7 examens thématiques (POO, décorateurs, tris, binary search…)",
      "6 corrections détaillées avec explications",
      "Auto-évaluation et suivi de progression",
    ],
  },
];

const TESTIMONIALS = [
  {
    name: "Sarah M.",
    role: "Reconversion Data Analyst",
    text: "En 3 mois, je suis passée de zéro en programmation à un niveau suffisant pour décrocher mon premier poste. L'accompagnement fait toute la différence.",
    rating: 5,
  },
  {
    name: "Karim B.",
    role: "Étudiant en informatique",
    text: "Les cours sont incroyablement bien structurés. Chaque notebook est clair, avec des exercices progressifs. Le meilleur investissement de mon parcours.",
    rating: 5,
  },
  {
    name: "Julie L.",
    role: "Développeuse web → Python",
    text: "J'avais des bases en JS mais Python me faisait peur. Grâce au suivi personnalisé, j'ai pu avancer à mon rythme. L'accès aux repos est un vrai plus.",
    rating: 5,
  },
];

const FAQ = [
  {
    q: "Combien de temps faut-il pour terminer la formation ?",
    a: "Le parcours est conçu pour être complété en 2 à 4 mois à raison de quelques heures par semaine. Mais comme l'accès est à vie, vous pouvez prendre le temps qu'il vous faut.",
  },
  {
    q: "Faut-il des prérequis ?",
    a: "Aucun. La formation commence de zéro. Si vous savez utiliser un ordinateur, vous pouvez apprendre Python avec nous.",
  },
  {
    q: "Comment fonctionne l'accompagnement ?",
    a: "Vous avez accès à un canal Discord privé où vous pouvez poser vos questions et demander de l'aide à tout moment. Chaque semaine, une réunion de suivi est organisée. Si vous avez besoin d'aide pour avancer, signalez-vous et un membre sera disponible pour travailler avec vous.",
  },
  {
    q: "Les cours sont-ils mis à jour ?",
    a: "Oui, régulièrement. Quand Python évolue ou que de meilleures pratiques apparaissent, les cours sont mis à jour et vous y accédez automatiquement.",
  },
  {
    q: "Puis-je accéder aux cours depuis mon téléphone ?",
    a: "Oui, la plateforme est entièrement responsive et accessible depuis n'importe quel appareil.",
  },
  {
    q: "Y a-t-il une garantie ?",
    a: "Oui. Si la formation ne vous convient pas dans les 14 premiers jours, vous êtes remboursé intégralement, sans condition.",
  },
];

function FAQItem({ item }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="faq-item" onClick={() => setOpen(!open)}>
      <div className="faq-q">
        <span>{item.q}</span>
        {open ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </div>
      {open && <div className="faq-a">{item.a}</div>}
    </div>
  );
}

export default function PricingPage() {
  const navigate = useNavigate();

  return (
    <>
      <ParticlesBg />
      <div className="pricing-page">

        {/* HERO */}
        <section className="pr-hero anim">
          <div className="pr-hero-badge">
            <Sparkles size={13} />
            Formation complète Python
          </div>
          <h1 className="pr-hero-title">
            Devenez développeur Python,
            <br />
            <span className="grad">de zéro à expert.</span>
          </h1>
          <p className="pr-hero-sub">
            40+ cours interactifs, 6 projets concrets, 7 examens, un canal Discord privé,
            des réunions de suivi hebdomadaires et un accès à vie. Tout ce qu'il faut pour maîtriser Python.
          </p>
          <div className="pr-hero-stats">
            <div className="pr-stat"><BookOpen size={18} /><span>40+ cours</span></div>
            <div className="pr-stat"><Code2 size={18} /><span>6 projets</span></div>
            <div className="pr-stat"><Target size={18} /><span>7 examens</span></div>
            <div className="pr-stat"><Infinity size={18} /><span>Accès à vie</span></div>
          </div>
        </section>

        {/* PRICING CARD */}
        <section className="pr-pricing-section anim anim-d2">
          <div className="pr-card">
            <div className="pr-card-glow" />
            <div className="pr-card-badge">
              <Zap size={14} />
              Formation complète
            </div>
            <div className="pr-card-price">
              <span className="pr-price-amount">350</span>
              <span className="pr-price-currency">€</span>
              <span className="pr-price-period">paiement unique</span>
            </div>
            <p className="pr-card-sub">Accès à vie · Mises à jour incluses · Discord privé · Accompagnement hebdomadaire</p>

            <div className="pr-card-features">
              <div className="pr-cf"><Check size={16} /><span>40+ cours Jupyter Notebooks interactifs</span></div>
              <div className="pr-cf"><Check size={16} /><span>3 niveaux : débutant → intermédiaire → avancé</span></div>
              <div className="pr-cf"><Check size={16} /><span>6 projets concrets avec corrections</span></div>
              <div className="pr-cf"><Check size={16} /><span>7 examens + corrections détaillées</span></div>
              <div className="pr-cf"><Check size={16} /><span>Accompagnement et suivi personnalisé</span></div>
              <div className="pr-cf"><Check size={16} /><span>Mises à jour continues des cours</span></div>
              <div className="pr-cf"><Check size={16} /><span>Accès aux repos GitHub (cours + projets)</span></div>
              <div className="pr-cf"><Check size={16} /><span>Canal Discord privé — posez vos questions à tout moment</span></div>
              <div className="pr-cf"><Check size={16} /><span>Réunion hebdomadaire de suivi — aide personnalisée</span></div>
              <div className="pr-cf"><Check size={16} /><span>Accès à vie — pas d'abonnement</span></div>
              <div className="pr-cf"><Check size={16} /><span>Garantie satisfait ou remboursé 14 jours</span></div>
            </div>

            <button className="pr-cta" onClick={() => window.location.href = "mailto:hippolytetchoffo3@gmail.com?subject=Inscription%20Formation%20Python%20-%20350%E2%82%AC&body=Bonjour%2C%0A%0AJe%20souhaite%20m%E2%80%99inscrire%20%C3%A0%20la%20formation%20Python%20compl%C3%A8te%20(350%E2%82%AC).%0A%0ANom%20%3A%20%0APr%C3%A9nom%20%3A%20%0A%0AMerci%20!"}>
              <Rocket size={18} />
              Rejoindre la formation
            </button>

            <div className="pr-guarantee">
              <Shield size={15} />
              <span>Garantie 14 jours satisfait ou remboursé</span>
            </div>
          </div>
        </section>

        {/* FEATURES */}
        <section className="pr-features-section">
          <h2 className="pr-section-title anim">Ce que vous obtenez</h2>
          <p className="pr-section-sub anim anim-d1">Tout ce dont vous avez besoin pour devenir un développeur Python compétent et opérationnel.</p>
          <div className="pr-features-grid stagger">
            {FEATURES.map((f, i) => (
              <div key={i} className="pr-feature-card">
                <div className="pr-feature-icon">{f.icon}</div>
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* CURRICULUM */}
        <section className="pr-curriculum-section">
          <h2 className="pr-section-title anim">Le programme complet</h2>
          <p className="pr-section-sub anim anim-d1">Un parcours structuré et progressif pour vous emmener du premier <code>print()</code> à la distribution de vos propres packages.</p>
          <div className="pr-curriculum-grid stagger">
            {CURRICULUM.map((c, i) => (
              <div key={i} className="pr-curric-card">
                <div className="pr-curric-header" style={{ borderColor: c.color }}>
                  <span className="pr-curric-level" style={{ color: c.color }}>{c.level}</span>
                  <span className="pr-curric-count">{c.modules} modules</span>
                </div>
                <ul className="pr-curric-list">
                  {c.items.map((item, j) => (
                    <li key={j}><Check size={14} style={{ color: c.color, flexShrink: 0 }} /><span>{item}</span></li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {/* TESTIMONIALS */}
        <section className="pr-testimonials-section">
          <h2 className="pr-section-title anim">Ce qu'en disent nos étudiants</h2>
          <div className="pr-testimonials-grid stagger">
            {TESTIMONIALS.map((t, i) => (
              <div key={i} className="pr-testi-card">
                <div className="pr-testi-stars">
                  {Array.from({ length: t.rating }).map((_, s) => (
                    <Star key={s} size={14} fill="#fbbf24" color="#fbbf24" />
                  ))}
                </div>
                <p className="pr-testi-text">"{t.text}"</p>
                <div className="pr-testi-author">
                  <div className="pr-testi-avatar">{t.name[0]}</div>
                  <div>
                    <div className="pr-testi-name">{t.name}</div>
                    <div className="pr-testi-role">{t.role}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* FAQ */}
        <section className="pr-faq-section">
          <h2 className="pr-section-title anim">Questions fréquentes</h2>
          <div className="pr-faq-list anim anim-d1">
            {FAQ.map((item, i) => (
              <FAQItem key={i} item={item} />
            ))}
          </div>
        </section>

        {/* FINAL CTA */}
        <section className="pr-final-cta anim" id="contact">
          <div className="pr-final-glow" />
          <Heart size={28} className="pr-final-heart" />
          <h2>Prêt à maîtriser Python ?</h2>
          <p>Rejoignez la formation et commencez votre parcours dès aujourd'hui.</p>
          <div className="pr-final-price">
            <span className="pr-fp-amount">350€</span>
            <span className="pr-fp-note">paiement unique · accès à vie</span>
          </div>
          <button className="pr-cta pr-cta-final" onClick={() => window.location.href = "mailto:hippolytetchoffo3@gmail.com?subject=Inscription%20Formation%20Python%20-%20350%E2%82%AC&body=Bonjour%2C%0A%0AJe%20souhaite%20m%E2%80%99inscrire%20%C3%A0%20la%20formation%20Python%20compl%C3%A8te%20(350%E2%82%AC).%0A%0ANom%20%3A%20%0APr%C3%A9nom%20%3A%20%0A%0AMerci%20!"}>
            <Rocket size={18} />
            Commencer maintenant
          </button>
          <p className="pr-final-guarantee">
            <Shield size={14} /> Garantie 14 jours satisfait ou remboursé
          </p>
        </section>

        {/* BACK */}
        <div className="pr-back">
          <button className="back-btn" onClick={() => navigate("/")}>
            <ArrowLeft size={14} /> Retour à l'accueil
          </button>
        </div>

      </div>
    </>
  );
}
