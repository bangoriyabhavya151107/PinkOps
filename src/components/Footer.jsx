import React from 'react';
import { Shield, Lock, Activity, ExternalLink, Award, FileCode } from 'lucide-react';

export default function Footer({ onNavigate }) {
  const currentYear = new Date().getFullYear();

  const handleLink = (route, sectionId) => {
    if (route === '/') {
      onNavigate('/');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      onNavigate(route);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <footer className="site-footer bg-[#070409] border-t border-dark-border/80 pt-16 pb-12 text-text-muted">
      <div className="site-container">
        
        {/* Main Footer Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-10 pb-12 border-b border-dark-border/60">
          
          {/* Brand Column */}
          <div className="md:col-span-5">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-lg bg-pinkops/15 border border-pinkops/40 flex items-center justify-center p-1.5 shadow-sm">
                <img
                  src="/images/761671355755999843.jpeg"
                  alt="Rajasthan Royals Crest"
                  className="w-full h-full object-contain rounded"
                />
              </div>
              <div>
                <span className="font-heading-royal text-xl font-bold text-white block tracking-wide">
                  PINKOPS
                </span>
                <span className="font-mono text-xs font-semibold tracking-widest text-pinkops uppercase block">
                  OPERATION PINK PANTHER
                </span>
              </div>
            </div>

            <p className="text-sm text-text-muted leading-relaxed max-w-sm mb-6">
              Official advanced analytics platform engineered for the <strong className="text-white">Rajasthan Royals SupeRR Selector Season 2 (Round 1)</strong>. Objective: Identifying the 10 most pressure-reliable batters and bowlers from 200,999 competition deliveries.
            </p>

            <div className="p-3.5 rounded-lg bg-dark-card/60 border border-dark-border text-xs text-text-muted space-y-1">
              <div className="flex items-center gap-2 text-pinkops font-mono font-bold tracking-wider text-[11px]">
                <Activity className="w-3.5 h-3.5 animate-pulse" />
                <span>ZERO CHOKE. ALL SMOKE.</span>
              </div>
              <p className="text-[11px] text-text-faint">
                Tagline: <em className="text-white">Finding the Next Legend</em> • Powered by Choke Detector™, IceVein Score™, Pressure Lens™, and Smoke Test™.
              </p>
            </div>
          </div>

          {/* Quick Tactical Navigation */}
          <div className="md:col-span-3 sm:col-span-6">
            <h4 className="text-xs font-mono font-bold uppercase tracking-widest text-white mb-4 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-pinkops" />
              <span>War Room Navigation</span>
            </h4>
            <ul className="flex flex-col gap-2.5 text-sm list-none p-0 m-0">
              <li>
                <button
                  onClick={() => handleLink('/', 'mission')}
                  className="bg-transparent border-0 text-text-muted hover:text-pinkops transition-colors cursor-pointer p-0 text-left font-body"
                >
                  The Mission & 7 Criteria
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/', 'pressure')}
                  className="bg-transparent border-0 text-text-muted hover:text-pinkops transition-colors cursor-pointer p-0 text-left font-body"
                >
                  Live Pressure Simulator
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/', 'intelligence')}
                  className="bg-transparent border-0 text-text-muted hover:text-pinkops transition-colors cursor-pointer p-0 text-left font-body"
                >
                  4 Analytical Pillars
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/', 'methodology')}
                  className="bg-transparent border-0 text-text-muted hover:text-pinkops transition-colors cursor-pointer p-0 text-left font-body"
                >
                  8-Stage Pipeline & Data Audit
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/', 'board')}
                  className="bg-transparent border-0 text-text-muted hover:text-pinkops transition-colors cursor-pointer p-0 text-left font-body"
                >
                  The PinkOps Board (Top 10)
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/', 'rr-context')}
                  className="bg-transparent border-0 text-text-muted hover:text-pinkops transition-colors cursor-pointer p-0 text-left font-body"
                >
                  RR 2027 Squad Context
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/', 'brief')}
                  className="bg-transparent border-0 text-text-muted hover:text-pinkops transition-colors cursor-pointer p-0 text-left font-body"
                >
                  Mission Brief & Synthesis
                </button>
              </li>
            </ul>
          </div>

          {/* Governance & Confidentiality */}
          <div className="md:col-span-4 sm:col-span-6">
            <h4 className="text-xs font-mono font-bold uppercase tracking-widest text-white mb-4 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-icevein" />
              <span>Governance & Data Rigor</span>
            </h4>
            <ul className="flex flex-col gap-2.5 text-sm list-none p-0 m-0 mb-5">
              <li>
                <button
                  onClick={() => handleLink('/privacy')}
                  className="bg-transparent border-0 text-text-muted hover:text-icevein transition-colors cursor-pointer p-0 text-left flex items-center gap-1.5 font-body"
                >
                  <Lock className="w-3.5 h-3.5 text-icevein" />
                  <span>Confidentiality & Data Privacy</span>
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/terms')}
                  className="bg-transparent border-0 text-text-muted hover:text-icevein transition-colors cursor-pointer p-0 text-left flex items-center gap-1.5 font-body"
                >
                  <Shield className="w-3.5 h-3.5 text-icevein" />
                  <span>Competition Terms & IP Stewardship</span>
                </button>
              </li>
            </ul>

            <div className="text-xs text-text-faint leading-relaxed border-t border-dark-border/40 pt-4 space-y-2">
              <div className="flex items-center gap-1.5 text-sandstone font-mono font-semibold">
                <Award className="w-3.5 h-3.5" />
                <span>Proprietary Dataset Protection</span>
              </div>
              <p>
                Evaluated against the official competition dataset (200,999 balls, 883 matches, 1,217 players, 6 Super Overs). No raw ball-by-ball microdata is harvested, exposed, or downloaded.
              </p>
            </div>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-text-faint gap-4 font-mono">
          <p>© {currentYear} PinkOps • Operation Pink Panther • Rajasthan Royals SupeRR Selector S2 R1.</p>
          <div className="flex items-center gap-5">
            <button
              onClick={() => handleLink('/privacy')}
              className="bg-transparent border-0 text-text-faint hover:text-pinkops transition-colors cursor-pointer p-0"
            >
              Privacy
            </button>
            <span className="text-dark-border">•</span>
            <button
              onClick={() => handleLink('/terms')}
              className="bg-transparent border-0 text-text-faint hover:text-pinkops transition-colors cursor-pointer p-0"
            >
              Terms
            </button>
            <span className="text-dark-border">•</span>
            <span className="text-pinkops font-bold">HALLA BOL! ⚡</span>
          </div>
        </div>

      </div>
    </footer>
  );
}
