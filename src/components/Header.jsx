import React, { useState, useEffect } from 'react';
import { Menu, X, Compass, ChevronRight } from 'lucide-react';

export default function Header({ currentRoute = '/', onNavigate, activeSection = 'hero' }) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile drawer on escape
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
    { label: 'Home', sectionId: 'hero' },
    { label: 'Story', sectionId: 'story' },
    { label: 'Craft & Guilds', sectionId: 'craft' },
    { label: 'Dashboard', sectionId: 'dashboard' },
    { label: 'Heritage Gallery', sectionId: 'gallery' },
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
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
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
              aria-label="Rajasthan Cultural Heritage Dashboard - Home"
            >
              <span className="text-2xl" role="img" aria-label="Peacock">🦚</span>
              <div>
                <span className="brand-text-title text-maroon block">RAJASTHAN</span>
                <span className="brand-text-sub block">Cultural Dashboard</span>
              </div>
            </a>

            {/* Desktop Navigation Links */}
            <nav className="hidden md:flex items-center gap-8" aria-label="Main Navigation">
              {navItems.map((item) => {
                const isActive = currentRoute === '/' && activeSection === item.sectionId;
                return (
                  <button
                    key={item.sectionId}
                    onClick={() => handleNavClick(item.sectionId)}
                    className={`nav-link-animated bg-transparent border-0 cursor-pointer ${isActive ? 'active' : ''}`}
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
                onClick={() => handleNavClick('dashboard')}
                className="btn-royal-primary hidden sm:inline-flex"
                aria-label="Explore Rajasthan Dashboard"
              >
                <Compass className="w-4 h-4 text-gold" />
                <span>Explore Culture</span>
              </button>

              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2 rounded text-maroon bg-transparent border-0 cursor-pointer"
                aria-label={mobileMenuOpen ? 'Close Menu' : 'Open Menu'}
                aria-expanded={mobileMenuOpen}
              >
                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Navigation Drawer */}
      <div
        className={`mobile-drawer-overlay ${mobileMenuOpen ? 'open' : ''}`}
        onClick={() => setMobileMenuOpen(false)}
        aria-hidden="true"
      />
      <aside
        className={`mobile-drawer-panel ${mobileMenuOpen ? 'open' : ''}`}
        aria-label="Mobile Navigation"
      >
        <div className="flex items-center justify-between pb-6 border-b border-maroon/10">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🦚</span>
            <span className="font-heading-royal text-maroon font-bold text-lg">RAJASTHAN</span>
          </div>
          <button
            onClick={() => setMobileMenuOpen(false)}
            className="p-2 text-maroon border-0 bg-transparent cursor-pointer"
            aria-label="Close menu"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <nav className="flex flex-col gap-4 py-8">
          {navItems.map((item, idx) => (
            <button
              key={item.sectionId}
              onClick={() => handleNavClick(item.sectionId)}
              className="flex items-center justify-between py-3 text-left font-body text-lg font-semibold text-maroon bg-transparent border-0 border-b border-maroon/5 cursor-pointer"
              style={{ transitionDelay: `${idx * 50}ms` }}
            >
              <span>{item.label}</span>
              <ChevronRight className="w-4 h-4 text-gold" />
            </button>
          ))}
          <button
            onClick={() => {
              setMobileMenuOpen(false);
              onNavigate('/privacy');
            }}
            className="flex items-center justify-between py-3 text-left font-body text-base text-ink-muted bg-transparent border-0 cursor-pointer"
          >
            <span>Privacy Policy</span>
            <ChevronRight className="w-4 h-4 text-maroon/30" />
          </button>
          <button
            onClick={() => {
              setMobileMenuOpen(false);
              onNavigate('/terms');
            }}
            className="flex items-center justify-between py-3 text-left font-body text-base text-ink-muted bg-transparent border-0 cursor-pointer"
          >
            <span>Terms & Conditions</span>
            <ChevronRight className="w-4 h-4 text-maroon/30" />
          </button>
        </nav>

        <div className="mt-auto pt-6 border-t border-maroon/10 text-center">
          <p className="font-devanagari text-maroon text-lg font-bold">पधारो म्हारे देश</p>
          <p className="text-xs text-ink-subtle mt-1">Rajasthan Heritage Cultural Experience</p>
        </div>
      </aside>
    </>
  );
}
