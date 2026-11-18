import React, { useState } from 'react';
import ScrollReveal from './ScrollReveal';
import { METHODOLOGY_PILLARS } from '../data/pinkopsData';
import { ShieldCheck, Cpu, Filter, Flame, CheckCircle2, Sliders } from 'lucide-react';

export default function AnalyticsPillarsSection() {
  const [activePillar, setActivePillar] = useState(0);

  const pillarIcons = [Flame, ShieldCheck, Filter, Cpu];

  return (
    <section id="intelligence" className="section-py bg-void relative border-t border-dark-border">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="max-w-4xl mx-auto text-center mb-16">
          <ScrollReveal animation="fade-up">
            <span className="font-mono text-xs font-bold uppercase tracking-widest text-pinkops block mb-3">
              03 • PROPRIETARY ANALYTICAL PILLARS
            </span>
            <h2 className="text-3xl sm:text-5xl md:text-6xl font-black text-white uppercase tracking-tight mb-6">
              THE FOUR TACTICAL <br />
              <span className="neon-pink-text">INTELLIGENCE ENGINES</span>
            </h2>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed max-w-2xl mx-auto">
              How PinkOps isolates genuine signal from noise, rejects vanity aggregates, and proves that pressure reliability is mathematically measurable.
            </p>
          </ScrollReveal>
        </div>

        {/* 4 Pillars Interactive Tabbed View */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-16">
          
          {/* Left: Tab Selectors */}
          <div className="lg:col-span-5 flex flex-col gap-3">
            {METHODOLOGY_PILLARS.map((pillar, idx) => {
              const isActive = activePillar === idx;
              const IconComp = pillarIcons[idx];

              return (
                <button
                  type="button"
                  key={pillar.id}
                  onClick={() => setActivePillar(idx)}
                  className={`p-4 rounded-lg text-left transition-all border cursor-pointer ${
                    isActive
                      ? 'bg-dark-elevated border-pinkops shadow-tactical text-white'
                      : 'bg-dark-surface/80 border-dark-border text-text-muted hover:border-dark-border-hover hover:text-white'
                  }`}
                  style={{
                    backgroundColor: isActive ? 'var(--color-dark-elevated)' : 'rgba(18, 12, 23, 0.8)',
                    borderColor: isActive ? 'var(--color-pinkops)' : 'var(--color-dark-border)',
                    color: isActive ? '#FFFFFF' : 'var(--color-text-muted)',
                  }}
                >
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center gap-2.5">
                      <IconComp className={`w-4 h-4 ${isActive ? 'text-pinkops' : 'text-text-faint'}`} />
                      <span className="font-mono text-xs font-bold uppercase tracking-wider text-gold">
                        {pillar.badge}
                      </span>
                    </div>
                    <span className="font-mono text-xs text-text-faint">0{idx + 1}</span>
                  </div>

                  <h3 className="text-base sm:text-lg font-bold font-mono tracking-tight mt-1">
                    {pillar.name}
                  </h3>
                  <p className="text-xs text-text-muted mt-1 truncate">
                    {pillar.subtitle}
                  </p>
                </button>
              );
            })}
          </div>

          {/* Right: Active Deep-Dive Intelligence Dossier */}
          <div className="lg:col-span-7">
            {(() => {
              const pillar = METHODOLOGY_PILLARS[activePillar];
              const IconComp = pillarIcons[activePillar];

              return (
                <div className="hud-panel p-6 sm:p-8 bg-dark-elevated/90 border border-pinkops/40 min-h-[400px] flex flex-col justify-between">
                  <div className="hud-bracket bracket-tl" />
                  <div className="hud-bracket bracket-tr" />
                  <div className="hud-bracket bracket-bl" />
                  <div className="hud-bracket bracket-br" />

                  <div>
                    <div className="flex items-center justify-between pb-4 border-b border-dark-border mb-4">
                      <div className="flex items-center gap-2">
                        <IconComp className="w-5 h-5 text-pinkops" />
                        <span className="font-mono text-xs font-bold text-pinkops uppercase tracking-widest">
                          {pillar.badge}
                        </span>
                      </div>
                      <span className="px-2.5 py-0.5 rounded bg-black/60 text-gold font-mono text-xs font-bold border border-gold/30">
                        {pillar.metric}
                      </span>
                    </div>

                    <h3 className="text-2xl sm:text-3xl font-extrabold text-white mb-2 font-mono">
                      {pillar.name}
                    </h3>
                    <p className="text-sm font-semibold text-icevein mb-6 font-editorial text-lg italic">
                      "{pillar.subtitle}"
                    </p>

                    <p className="text-sm sm:text-base text-text-muted leading-relaxed mb-6 font-body">
                      {pillar.description}
                    </p>
                  </div>

                  <div className="pt-4 border-t border-dark-border font-mono text-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                      <span className="text-text-faint block">CORE GOVERNANCE PRINCIPLE:</span>
                      <span className="font-bold text-white">{pillar.principle}</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-status-green font-bold shrink-0">
                      <CheckCircle2 className="w-4 h-4" />
                      <span>100% CODEBASE VERIFIED</span>
                    </div>
                  </div>
                </div>
              );
            })()}
          </div>

        </div>

      </div>
    </section>
  );
}
