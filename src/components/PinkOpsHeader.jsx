import React, { useState, useEffect } from 'react';
import { Menu, X, Shield, ChevronRight, Activity } from 'lucide-react';

export default function PinkOpsHeader({ currentRoute = '/', onNavigate, activeSection = 'hero' }) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && mobileMenuOpen) {
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [mobileMenuOpen]);

  const navItems = [
    { label: 'Mission', sectionId: 'mission' },
    { label: 'Pressure Engine', sectionId: 'pressure' },
    { label: 'Intelligence', sectionId: 'intelligence' },
    { label: 'Methodology', sectionId: 'methodology' },
    { label: 'The PinkOps Board', sectionId: 'board' },
    { label: 'RR Context', sectionId: 'rr-context' },
  ];

  const handleNavClick = (sectionId) => {
    setMobileMenuOpen(false);
    if (currentRoute !== '/') {
      onNavigate('/');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      const el = document.getElementById(sectionId);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <>
      <header className={`site-header ${isScrolled ? 'scrolled' : ''}`}>
        <div className="site-container">
          <div className="header-inner">
            {/* Brand Logo */}
            <a
              href="/"
              onClick={(e) => {
                e.preventDefault();
                handleNavClick('hero');
              }}
              className="brand-logo"
              aria-label="PinkOps Operation Pink Panther - Home"
            >
              <div className="w-10 h-10 rounded-lg bg-pinkops/15 border border-pinkops/40 flex items-center justify-center p-1.5 shadow-sm">
                <img
                  src="/images/761671355755999843.jpeg"
                  alt="Rajasthan Royals Crest"
                  className="w-full h-full object-contain rounded"
                />
              </div>
              <div>
                <span className="brand-text-title tracking-wider">PINKOPS</span>
                <span className="brand-text-sub block">OPERATION PINK PANTHER</span>
              </div>
            </a>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex items-center gap-7" aria-label="Tactical Navigation">
              {navItems.map((item) => {
                const isActive = currentRoute === '/' && activeSection === item.sectionId;
                return (
                  <button
                    key={item.sectionId}
                    onClick={() => handleNavClick(item.sectionId)}
                    className={`nav-link-tactical ${isActive ? 'active' : ''}`}
                    aria-current={isActive ? 'page' : undefined}
                  >
                    {item.label}
                  </button>
                );
              })}
            </nav>

            {/* CTA & Mobile Hamburger */}
            <div className="flex items-center gap-4">
              <button
                type="button"
                onClick={() => handleNavClick('board')}
                className="btn-pinkops-primary hidden sm:inline-flex py-2 px-5 text-xs font-bold"
                aria-label="View Top 10 Reliable Players"
              >
                <Activity className="w-3.5 h-3.5 text-white animate-pulse" />
                <span>VIEW TOP 10</span>
              </button>

              <button
                type="button"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="lg:hidden p-2 text-text-main bg-transparent border-0 cursor-pointer"
                style={{ background: 'transparent', border: 'none' }}
                aria-label={mobileMenuOpen ? 'Close Menu' : 'Open Menu'}
                aria-expanded={mobileMenuOpen}
              >
                {mobileMenuOpen ? <X className="w-6 h-6 text-pinkops" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Drawer */}
      <div
        className={`mobile-drawer-overlay ${mobileMenuOpen ? 'open' : ''}`}
        onClick={() => setMobileMenuOpen(false)}
        aria-hidden="true"
      />
      <aside
        className={`mobile-drawer-panel ${mobileMenuOpen ? 'open' : ''}`}
        aria-label="Mobile Tactical Navigation"
      >
        <div className="flex items-center justify-between pb-6 border-b border-dark-border">
          <div className="flex items-center gap-3">
            <span className="text-xl">⚡</span>
            <div>
              <span className="font-heading-royal text-white font-bold text-lg block">PINKOPS</span>
              <span className="text-[10px] font-mono text-pinkops tracking-widest uppercase">RR SUPERR SELECTOR</span>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setMobileMenuOpen(false)}
            className="p-2 text-text-muted hover:text-white border-0 bg-transparent cursor-pointer"
            style={{ background: 'transparent', border: 'none' }}
            aria-label="Close menu"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <nav className="flex flex-col gap-3 py-6">
          {navItems.map((item, idx) => (
            <button
              key={item.sectionId}
              onClick={() => handleNavClick(item.sectionId)}
              className="flex items-center justify-between py-3 text-left font-body text-base font-semibold text-text-main bg-transparent border-0 border-b border-dark-border/40 cursor-pointer hover:text-pinkops"
            >
              <span>{item.label}</span>
              <ChevronRight className="w-4 h-4 text-pinkops/50" />
            </button>
          ))}
          <button
            onClick={() => {
              setMobileMenuOpen(false);
              onNavigate('/privacy');
            }}
            className="flex items-center justify-between py-2 text-left font-body text-sm text-text-muted bg-transparent border-0 cursor-pointer hover:text-white"
          >
            <span>Confidentiality & Privacy</span>
            <ChevronRight className="w-4 h-4 text-text-faint" />
          </button>
          <button
            onClick={() => {
              setMobileMenuOpen(false);
              onNavigate('/terms');
            }}
            className="flex items-center justify-between py-2 text-left font-body text-sm text-text-muted bg-transparent border-0 cursor-pointer hover:text-white"
          >
            <span>Terms & Governance</span>
            <ChevronRight className="w-4 h-4 text-text-faint" />
          </button>
        </nav>

        <div className="mt-auto pt-6 border-t border-dark-border text-center">
          <span className="font-mono text-xs text-pinkops font-bold tracking-widest block mb-1">
            ZERO CHOKE. ALL SMOKE.
          </span>
          <span className="text-[11px] text-text-faint block">
            Operation Pink Panther • RR S2 R1
          </span>
        </div>
      </aside>
    </>
  );
}
