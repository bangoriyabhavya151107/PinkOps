import React, { useState, useEffect } from 'react';
import PinkOpsHeader from './components/PinkOpsHeader';
import HeroWarRoom from './components/HeroWarRoom';
import MissionSection from './components/MissionSection';
import PressureEngineSection from './components/PressureEngineSection';
import AnalyticsPillarsSection from './components/AnalyticsPillarsSection';
import InteractiveMethodology from './components/InteractiveMethodology';
import PinkOpsBoard from './components/PinkOpsBoard';
import RRSquadContext from './components/RRSquadContext';
import MissionBriefFinal from './components/MissionBriefFinal';
import Footer from './components/Footer';
import TargetFileModal from './components/TargetFileModal';
import CustomCursor from './components/CustomCursor';
import PrivacyPage from './pages/PrivacyPage';
import TermsPage from './pages/TermsPage';

export default function App() {
  const [currentRoute, setCurrentRoute] = useState(() => {
    const path = window.location.pathname;
    if (path === '/privacy' || path === '/terms') return path;
    return '/';
  });

  const [activeSection, setActiveSection] = useState('hero');
  const [scrollProgress, setScrollProgress] = useState(0);
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  // Sync route with browser history (Back / Forward buttons)
  useEffect(() => {
    const handlePopState = () => {
      const path = window.location.pathname;
      if (path === '/privacy' || path === '/terms') {
        setCurrentRoute(path);
      } else {
        setCurrentRoute('/');
      }
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const navigate = (route) => {
    if (route !== currentRoute) {
      window.history.pushState({}, '', route);
      setCurrentRoute(route);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  // Track scroll progress and active section spy
  useEffect(() => {
    if (currentRoute !== '/') return;

    const handleScroll = () => {
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      setScrollProgress(scrolled);

      // Section spy
      const sections = ['hero', 'mission', 'pressure', 'intelligence', 'methodology', 'board', 'rr-context', 'brief'];
      for (const sectionId of sections) {
        const el = document.getElementById(sectionId);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.top <= 240 && rect.bottom >= 100) {
            setActiveSection(sectionId);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [currentRoute]);

  const scrollToSection = (sectionId) => {
    if (currentRoute !== '/') {
      navigate('/');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 120);
    } else {
      const el = document.getElementById(sectionId);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="relative min-h-screen bg-[#09060B] text-text-main selection:bg-pinkops/30 selection:text-white font-body">
      {/* Scroll Progress Bar */}
      <div className="scroll-progress-container" aria-hidden="true">
        <div 
          className="scroll-progress-bar"
          style={{ width: `${scrollProgress}%` }}
        />
      </div>

      {/* Subtle Tactical Cursor (Desktop Only) */}
      <CustomCursor />

      {/* Dedicated Legal Route: Confidentiality & Privacy */}
      {currentRoute === '/privacy' && (
        <>
          <PinkOpsHeader currentRoute="/privacy" onNavigate={navigate} />
          <main>
            <PrivacyPage onNavigate={navigate} />
          </main>
          <Footer onNavigate={navigate} />
        </>
      )}

      {/* Dedicated Legal Route: Terms & Governance */}
      {currentRoute === '/terms' && (
        <>
          <PinkOpsHeader currentRoute="/terms" onNavigate={navigate} />
          <main>
            <TermsPage onNavigate={navigate} />
          </main>
          <Footer onNavigate={navigate} />
        </>
      )}

      {/* Main War Room Presentation Layer */}
      {currentRoute === '/' && (
        <>
          <PinkOpsHeader
            currentRoute="/"
            onNavigate={navigate}
            activeSection={activeSection}
          />
          <main>
            {/* Hero War Room & Strategic Question */}
            <HeroWarRoom
              onExploreMission={() => scrollToSection('mission')}
              onExploreBoard={() => scrollToSection('board')}
            />

            {/* The Mission & 7 Non-Negotiable Criteria */}
            <MissionSection />

            {/* Live Interactive Pressure Engine Simulator */}
            <PressureEngineSection />

            {/* 4 Proprietary Analytics Pillars */}
            <AnalyticsPillarsSection />

            {/* 8-Stage Methodology Pipeline & Data Integrity Audit */}
            <InteractiveMethodology />

            {/* The PinkOps Board: Final 10 Batters & Final 10 Bowlers */}
            <PinkOpsBoard onSelectPlayer={(player) => setSelectedPlayer(player)} />

            {/* Rajasthan Royals IPL 2027 Context */}
            <RRSquadContext onSelectPlayer={(player) => setSelectedPlayer(player)} />

            {/* Executive Synthesis: Key Findings & Tactical Takeaways */}
            <MissionBriefFinal onSelectPlayer={(player) => setSelectedPlayer(player)} />
          </main>
          <Footer onNavigate={navigate} />
        </>
      )}

      {/* Interactive Target File Dossier Modal */}
      {selectedPlayer && (
        <TargetFileModal
          player={selectedPlayer}
          onClose={() => setSelectedPlayer(null)}
        />
      )}
    </div>
  );
}
