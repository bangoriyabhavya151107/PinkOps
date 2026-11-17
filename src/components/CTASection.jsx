import React from 'react';
import ScrollReveal from './ScrollReveal';
import { Sparkles, ArrowUp, Compass } from 'lucide-react';

export default function CTASection({ onScrollToTop, onExploreDashboard }) {
  return (
    <section className="section-py bg-maroon text-[#FAF6EE] relative overflow-hidden">
      {/* Background Motifs */}
      <div 
        className="absolute inset-0 opacity-10 pointer-events-none"
        style={{
          backgroundImage: 'radial-gradient(circle at 50% 50%, var(--color-gold) 1px, transparent 1px)',
          backgroundSize: '24px 24px'
        }}
        aria-hidden="true"
      />

      <div className="site-container relative" style={{ zIndex: 'var(--z-content)' }}>
        <div className="max-w-4xl mx-auto text-center">
          
          <ScrollReveal animation="scale-in">
            {/* Royal Crest / Halla Bol Monogram */}
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-white/10 border-2 border-gold/50 shadow-gold-glow mb-6 p-2">
              <img
                src="/images/761671355755999843.jpeg"
                alt="Rajasthan Royals Crest Logo"
                className="w-full h-full object-contain rounded-full"
              />
            </div>

            <span className="text-xs font-bold uppercase tracking-widest text-gold block mb-3 font-body">
              The Sovereign Spirit of Rajputana
            </span>

            <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold text-[#FFFDF9] mb-6 leading-tight">
              Padharo Mhare Desh <br />
              <span className="font-editorial italic font-normal text-gold">Halla Bol!</span>
            </h2>

            <p className="text-base sm:text-lg text-[#E0D5C1] max-w-2xl mx-auto leading-relaxed mb-10 font-body">
              Experience the timeless valor, radiant craftsmanship, and living folklore of Rajasthan through an authentic digital tribute to our heritage.
            </p>

            <div className="flex flex-wrap items-center justify-center gap-4">
              <button
                onClick={onExploreDashboard}
                className="inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-lg bg-gold hover:bg-gold-light text-maroon font-bold text-base transition-all shadow-lg hover:shadow-gold-glow cursor-pointer"
              >
                <Compass className="w-5 h-5 text-maroon" />
                <span>Explore Archival Intelligence</span>
              </button>

              <button
                onClick={onScrollToTop}
                className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-lg bg-white/10 hover:bg-white/20 text-[#FFFDF9] border border-gold/40 font-semibold text-base transition-all cursor-pointer"
              >
                <ArrowUp className="w-4 h-4 text-gold" />
                <span>Back to Zenith</span>
              </button>
            </div>
          </ScrollReveal>

        </div>
      </div>
    </section>
  );
}
