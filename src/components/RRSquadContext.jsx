import React from 'react';
import ScrollReveal from './ScrollReveal';
import { RR_SQUAD_CONTEXT } from '../data/pinkopsData';
import { ShieldCheck, ArrowRightLeft, Users, Coins, Target, AlertCircle } from 'lucide-react';

export default function RRSquadContext() {
  return (
    <section id="rr-context" className="section-py bg-dark-surface/60 relative border-t border-dark-border">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="max-w-4xl mx-auto text-center mb-14">
          <ScrollReveal animation="fade-up">
            <span className="font-mono text-xs font-bold uppercase tracking-widest text-pinkops block mb-3">
              06 • STRATEGIC FRANCHISE INTERPRETATION
            </span>
            <h2 className="text-3xl sm:text-5xl md:text-6xl font-black text-white uppercase tracking-tight mb-4">
              ROYALS CONTEXT
            </h2>
            <p className="text-xl sm:text-2xl font-editorial italic text-gold max-w-2xl mx-auto mb-6">
              "What the pressure intelligence means for Rajasthan Royals."
            </p>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed max-w-2xl mx-auto">
              Synthesizing objective pressure reliability metrics with Rajasthan Royals' current official squad telemetry for the IPL 2027 strategic horizon.
            </p>
          </ScrollReveal>
        </div>

        {/* Official RR Public Telemetry Card */}
        <div className="hud-panel p-6 sm:p-8 mb-12 bg-dark-elevated border border-pinkops/40 max-w-5xl mx-auto">
          <div className="hud-bracket bracket-tl" />
          <div className="hud-bracket bracket-tr" />
          <div className="hud-bracket bracket-bl" />
          <div className="hud-bracket bracket-br" />

          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-dark-border gap-4">
            <div>
              <span className="font-mono text-xs text-pinkops uppercase font-bold tracking-widest block">
                OFFICIAL FRANCHISE AUDIT
              </span>
              <h3 className="text-xl sm:text-2xl font-bold text-white mt-1">
                Rajasthan Royals IPL 2027 Retention Roster
              </h3>
            </div>
            <div className="flex items-center gap-2 px-3 py-1.5 rounded bg-black/60 border border-gold/40 text-gold font-mono text-xs font-bold">
              <Coins className="w-4 h-4" />
              <span>REMAINING PURSE: {RR_SQUAD_CONTEXT.purseRemaining}</span>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 py-6 font-mono text-center border-b border-dark-border">
            <div className="p-3 rounded bg-black/40 border border-dark-border">
              <span className="text-[10px] text-text-faint uppercase block">RETAINED PLAYERS</span>
              <span className="text-xl font-bold text-white block mt-0.5">
                {RR_SQUAD_CONTEXT.retainedGroupCount}
              </span>
            </div>
            <div className="p-3 rounded bg-black/40 border border-dark-border">
              <span className="text-[10px] text-text-faint uppercase block">SLOTS AVAILABLE</span>
              <span className="text-xl font-bold text-pinkops block mt-0.5">
                {RR_SQUAD_CONTEXT.slotsRemaining}
              </span>
            </div>
            <div className="p-3 rounded bg-black/40 border border-dark-border">
              <span className="text-[10px] text-text-faint uppercase block">SHAMI TRADE</span>
              <span className="text-xs font-bold text-status-green block mt-2">
                TRADED IN (PACE)
              </span>
            </div>
            <div className="p-3 rounded bg-black/40 border border-dark-border">
              <span className="text-[10px] text-text-faint uppercase block">CURRAN TRADE</span>
              <span className="text-xs font-bold text-status-amber block mt-2">
                TRADED OUT (AR)
              </span>
            </div>
          </div>

          {/* Recent Confirmed Trades */}
          <div className="pt-6">
            <span className="font-mono text-xs text-text-faint uppercase block mb-3 font-bold">
              OFFICIAL TRADING WINDOW ACTIONS:
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {RR_SQUAD_CONTEXT.recentTrades.map((tr, idx) => (
                <div key={idx} className="p-3 rounded bg-dark-surface border border-dark-border flex items-center justify-between">
                  <div>
                    <h4 className="text-sm font-bold text-white">{tr.player}</h4>
                    <span className="text-[11px] text-text-muted">{tr.role}</span>
                  </div>
                  <span className={`px-2 py-0.5 rounded font-mono text-[10px] font-bold uppercase ${
                    tr.type.includes('In') ? 'bg-status-green/15 text-status-green border border-status-green/30' : 'bg-status-amber/15 text-status-amber border border-status-amber/30'
                  }`}>
                    {tr.type}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Strategic Need & PinkOps Solutions Map */}
        <div className="max-w-5xl mx-auto space-y-4 mb-12">
          <h3 className="font-mono text-xs font-bold text-gold uppercase tracking-wider text-center mb-6">
            HOW PINKOPS TARGETS SOLVE STRUCTURAL FRANCHISE VACANCIES
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {RR_SQUAD_CONTEXT.tacticalNeeds.map((need, idx) => (
              <ScrollReveal key={idx} animation="fade-up" delay={idx * 80}>
                <div className="hud-panel p-5 h-full flex flex-col justify-between bg-dark-elevated border border-dark-border hover:border-pinkops/50">
                  <div>
                    <div className="flex items-center justify-between pb-3 border-b border-dark-border/40 mb-3 font-mono">
                      <span className="text-xs font-bold text-pinkops">{need.status}</span>
                      <span className="text-[10px] text-text-faint">TACTICAL AREA</span>
                    </div>

                    <h4 className="text-base font-bold text-white mb-2 font-mono">
                      {need.area}
                    </h4>

                    <div className="p-2.5 rounded bg-black/50 border border-dark-border/60 mb-3">
                      <span className="text-[10px] text-text-faint font-mono uppercase block">PINKOPS SOLUTION:</span>
                      <span className="text-xs font-bold text-gold font-mono block mt-0.5">{need.solution}</span>
                    </div>

                    <p className="text-xs text-text-muted leading-relaxed font-body">
                      {need.analysis}
                    </p>
                  </div>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>

        {/* Competition Rules Transparency Alert */}
        <div className="max-w-4xl mx-auto p-4 rounded-lg bg-pinkops/10 border border-pinkops/30 flex items-start gap-3 text-xs font-body text-text-main">
          <AlertCircle className="w-5 h-5 text-pinkops shrink-0 mt-0.5" />
          <div>
            <strong className="text-white font-mono block mb-0.5">COMPETITION GOVERNANCE INVARIANT:</strong>
            {RR_SQUAD_CONTEXT.eligibilityClarification}
          </div>
        </div>

      </div>
    </section>
  );
}
