import React, { useState } from 'react';
import ScrollReveal from './ScrollReveal';
import { METHODOLOGY_PIPELINE, AUDIT_STATS } from '../data/pinkopsData';
import { ChevronDown, Database, CheckCircle2, ShieldCheck, FileSpreadsheet } from 'lucide-react';

export default function InteractiveMethodology() {
  const [expandedStep, setExpandedStep] = useState(null);

  const toggleStep = (idx) => {
    setExpandedStep(expandedStep === idx ? null : idx);
  };

  return (
    <section id="methodology" className="section-py bg-dark-surface/50 relative border-t border-dark-border">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="max-w-4xl mx-auto text-center mb-16">
          <ScrollReveal animation="fade-up">
            <span className="font-mono text-xs font-bold uppercase tracking-widest text-gold block mb-3">
              04 • FROZEN METHODOLOGICAL PIPELINE
            </span>
            <h2 className="text-3xl sm:text-5xl md:text-6xl font-black text-white uppercase tracking-tight mb-6">
              AUDITED DATA & <br />
              <span className="neon-gold-text">8-STAGE METHODOLOGY</span>
            </h2>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed max-w-2xl mx-auto">
              A mathematically defensible, reproducible pipeline built on audited competition data with zero leakage and universal multiverse validation.
            </p>
          </ScrollReveal>
        </div>

        {/* Audited Data Telemetry Ticker Banner */}
        <div className="hud-panel p-6 mb-16 bg-dark-elevated/80 border border-gold/40">
          <div className="hud-bracket bracket-tl" />
          <div className="hud-bracket bracket-tr" />
          <div className="hud-bracket bracket-bl" />
          <div className="hud-bracket bracket-br" />

          <div className="flex items-center gap-2 mb-4 font-mono text-xs text-gold font-bold uppercase tracking-wider">
            <Database className="w-4 h-4 text-gold" />
            <span>STAGE 1 AUDITED REPOSITORY TELEMETRY (SHA-256 VERIFIED)</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 font-mono text-center">
            <div className="p-3 rounded bg-black/40 border border-dark-border">
              <span className="text-[10px] text-text-faint uppercase block">PITCH DELIVERIES</span>
              <span className="text-lg sm:text-xl font-bold text-white block mt-0.5">
                {AUDIT_STATS.totalDeliveries.toLocaleString()}
              </span>
            </div>
            <div className="p-3 rounded bg-black/40 border border-dark-border">
              <span className="text-[10px] text-text-faint uppercase block">TOTAL MATCHES</span>
              <span className="text-lg sm:text-xl font-bold text-pinkops block mt-0.5">
                {AUDIT_STATS.totalMatches}
              </span>
            </div>
            <div className="p-3 rounded bg-black/40 border border-dark-border">
              <span className="text-[10px] text-text-faint uppercase block">UNIQUE PLAYERS</span>
              <span className="text-lg sm:text-xl font-bold text-gold block mt-0.5">
                {AUDIT_STATS.distinctPlayers.toLocaleString()}
              </span>
            </div>
            <div className="p-3 rounded bg-black/40 border border-dark-border">
              <span className="text-[10px] text-text-faint uppercase block">SUPER OVERS</span>
              <span className="text-lg sm:text-xl font-bold text-icevein block mt-0.5">
                {AUDIT_STATS.superOverMatches} ({AUDIT_STATS.superOverDeliveries}b)
              </span>
            </div>
            <div className="p-3 rounded bg-black/40 border border-dark-border">
              <span className="text-[10px] text-text-faint uppercase block">ROW DUPLICATES</span>
              <span className="text-lg sm:text-xl font-bold text-status-green block mt-0.5">
                {AUDIT_STATS.exactDuplicates} (0.00%)
              </span>
            </div>
            <div className="p-3 rounded bg-black/40 border border-dark-border">
              <span className="text-[10px] text-text-faint uppercase block">DATA STATUS</span>
              <span className="text-xs font-extrabold text-status-green block mt-2">
                IMMUTABLE
              </span>
            </div>
          </div>
        </div>

        {/* 8-Stage Interactive Pipeline Accordion */}
        <div className="space-y-3 max-w-4xl mx-auto">
          {METHODOLOGY_PIPELINE.map((st, idx) => {
            const isExpanded = expandedStep === idx;

            return (
              <div
                key={st.step}
                className={`hud-panel overflow-hidden transition-all border ${
                  isExpanded ? 'border-pinkops/60 bg-dark-elevated' : 'border-dark-border/80 bg-dark-surface/70'
                }`}
              >
                <button
                  type="button"
                  onClick={() => toggleStep(idx)}
                  className="w-full p-4 sm:p-5 text-left flex items-center justify-between gap-4 cursor-pointer bg-transparent border-0"
                  style={{ background: 'transparent', border: 'none' }}
                  aria-expanded={isExpanded}
                >
                  <div className="flex items-center gap-4">
                    <span className="font-mono text-xs sm:text-sm font-extrabold text-pinkops w-8 h-8 rounded bg-pinkops/15 flex items-center justify-center shrink-0">
                      {st.step}
                    </span>
                    <div>
                      <h3 className="text-base sm:text-lg font-bold text-white font-mono">
                        {st.title}
                      </h3>
                      <p className="text-xs text-text-muted mt-0.5 line-clamp-1 font-body">
                        {st.summary}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span className="font-mono text-[11px] text-text-faint hidden sm:inline">
                      {isExpanded ? 'COLLAPSE' : 'EXPAND'}
                    </span>
                    <ChevronDown
                      className={`w-5 h-5 text-pinkops transition-transform duration-300 ${
                        isExpanded ? 'rotate-180' : ''
                      }`}
                    />
                  </div>
                </button>

                {isExpanded && (
                  <div className="px-5 pb-5 pt-2 border-t border-dark-border/40 font-body text-xs sm:text-sm text-text-muted leading-relaxed">
                    <p className="mb-2">
                      <strong className="text-white font-mono">Scope:</strong> {st.summary}
                    </p>
                    <p>
                      <strong className="text-icevein font-mono">Methodological Detail:</strong> {st.details}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
