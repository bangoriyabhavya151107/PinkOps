import React from 'react';

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
    <footer className="site-footer pt-16 pb-12">
      <div className="site-container">
        
        {/* Main Footer Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-10 pb-12 border-b border-gold/20">
          
          {/* Brand Column */}
          <div className="md:col-span-5">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-3xl">🦚</span>
              <div>
                <span className="font-heading-royal text-xl font-bold text-[#FFFDF9] block">
                  RAJASTHAN
                </span>
                <span className="text-xs font-semibold tracking-widest text-gold uppercase block">
                  Cultural Dashboard Experience
                </span>
              </div>
            </div>
            <p className="text-sm text-[#D8CAB5] leading-relaxed max-w-sm mb-6">
              A bespoke digital celebration of Rajasthan’s royal architecture, living desert folklore, master craft guilds, and vibrant folk music traditions.
            </p>
            <div className="p-3 rounded-lg bg-black/20 border border-gold/20 text-xs text-[#E8DCC8]">
              <span className="font-devanagari font-bold text-gold text-sm block mb-1">
                अतिथि देवो भव • ATITHI DEVO BHAVA
              </span>
              <span>The guest is truly divine. A tribute to royal Rajasthani hospitality.</span>
            </div>
          </div>

          {/* Quick Navigation Links */}
          <div className="md:col-span-3 sm:col-span-6">
            <h4 className="text-sm font-bold uppercase tracking-wider text-gold mb-4 font-body">
              Heritage Navigation
            </h4>
            <ul className="flex flex-col gap-2.5 text-sm list-none p-0 m-0">
              <li>
                <button
                  onClick={() => handleLink('/', 'hero')}
                  className="bg-transparent border-0 text-[#E0D5C1] hover:text-gold cursor-pointer p-0 text-left"
                >
                  Royal Welcome
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/', 'story')}
                  className="bg-transparent border-0 text-[#E0D5C1] hover:text-gold cursor-pointer p-0 text-left"
                >
                  Visual Chronicles
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/', 'craft')}
                  className="bg-transparent border-0 text-[#E0D5C1] hover:text-gold cursor-pointer p-0 text-left"
                >
                  Three Craft Acts
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/', 'dashboard')}
                  className="bg-transparent border-0 text-[#E0D5C1] hover:text-gold cursor-pointer p-0 text-left"
                >
                  Cultural Dashboard
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/', 'gallery')}
                  className="bg-transparent border-0 text-[#E0D5C1] hover:text-gold cursor-pointer p-0 text-left"
                >
                  28 Artifact Archive
                </button>
              </li>
            </ul>
          </div>

          {/* Legal & Governance */}
          <div className="md:col-span-4 sm:col-span-6">
            <h4 className="text-sm font-bold uppercase tracking-wider text-gold mb-4 font-body">
              Platform & Legal
            </h4>
            <ul className="flex flex-col gap-2.5 text-sm list-none p-0 m-0 mb-6">
              <li>
                <button
                  onClick={() => handleLink('/privacy')}
                  className="bg-transparent border-0 text-[#E0D5C1] hover:text-gold cursor-pointer p-0 text-left flex items-center gap-1.5"
                >
                  <span>Privacy Policy</span>
                  <span className="text-xs text-gold">↗</span>
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleLink('/terms')}
                  className="bg-transparent border-0 text-[#E0D5C1] hover:text-gold cursor-pointer p-0 text-left flex items-center gap-1.5"
                >
                  <span>Terms & Conditions</span>
                  <span className="text-xs text-gold">↗</span>
                </button>
              </li>
            </ul>

            <div className="text-xs text-[#C2B5A0] leading-normal border-t border-gold/10 pt-4">
              <span className="font-semibold text-gold block mb-1">Authentic Project Disclosure</span>
              This dashboard is an interactive frontend cultural showcase. It does not perform commercial booking or collect personal payment data.
            </div>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-[#C4B6A2] gap-4">
          <p>© {currentYear} Rajasthan Cultural Heritage Dashboard • PinkOps Project. All rights reserved.</p>
          <div className="flex items-center gap-6">
            <button
              onClick={() => handleLink('/privacy')}
              className="bg-transparent border-0 text-[#C4B6A2] hover:text-gold cursor-pointer p-0"
            >
              Privacy
            </button>
            <span className="text-gold/40">•</span>
            <button
              onClick={() => handleLink('/terms')}
              className="bg-transparent border-0 text-[#C4B6A2] hover:text-gold cursor-pointer p-0"
            >
              Terms
            </button>
            <span className="text-gold/40">•</span>
            <span className="text-gold">खम्मा घणी सा</span>
          </div>
        </div>

      </div>
    </footer>
  );
}
