import React from 'react';
import ScrollReveal from './ScrollReveal';
import { Target, AlertTriangle, ShieldCheck, TrendingUp, Filter } from 'lucide-react';

export default function MissionSection() {
  const pillars = [
    { label: 'Pressure Exposure', detail: 'Isolating top 20% leverage deliveries (PI ≥ 0.5898) rather than unpressured volume.' },
    { label: 'Opportunity & Context', detail: 'Evaluating performance relative to situational par (phase, wickets, venue, opponent).' },
    { label: 'Contextual Performance', detail: 'Value Added (Actual - Expected runs) rather than vanity aggregate strike rates.' },
    { label: 'Consistency & Spread', detail: 'Penalizing high match dispersion (MAD) to filter volatile one-match anomalies.' },
    { label: 'Uncertainty Control', detail: 'Empirical Bayes shrinkage to prior (K=100) guaranteeing downside floor (LUB20).' },
    { label: 'Downside Risk Hard Gates', detail: 'Strict elimination of collapse-prone players: Early Dismissal Rate ≤ 20%, Blowout Rate ≤ 20%.' },
    { label: 'Multiverse Robustness', detail: 'Verifying that selection survives across 24 specification perturbations with 8/8 support.' },
  ];

  return (
    <section id="mission" className="section-py bg-void relative border-t border-dark-border">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="max-w-4xl mx-auto text-center mb-16">
          <ScrollReveal animation="fade-up">
            <span className="font-mono text-xs font-bold uppercase tracking-widest text-pinkops block mb-3">
              01 • STRATEGIC MANDATE
            </span>
            <h2 className="text-3xl sm:text-5xl md:text-6xl font-black text-white uppercase tracking-tight mb-6">
              THE MISSION
            </h2>
            <p className="text-xl sm:text-2xl font-editorial italic text-gold max-w-3xl mx-auto mb-6">
              "Find the players who perform when the pressure is highest."
            </p>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed max-w-2xl mx-auto">
              Championships are not won by players who pad aggregate averages in low-leverage dead rubbers. They are decided in the high-stress crucible where game leverage spikes, required run rates surge past 10.5 rpo, and an unforced error precipitates catastrophic win-probability collapse.
            </p>
          </ScrollReveal>
        </div>

        {/* Two-Column Tactical Architecture */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          
          {/* Left Column: Visual Asset - Dil Thanda Rakh ("Keep Your Heart Cool") */}
          <div className="lg:col-span-5">
            <ScrollReveal animation="fade-right">
              <div className="hud-panel p-4 bg-dark-surface/90 border border-gold/30">
                <div className="hud-bracket bracket-tl" />
                <div className="hud-bracket bracket-tr" />
                <div className="hud-bracket bracket-bl" />
                <div className="hud-bracket bracket-br" />

                <div className="relative rounded-lg overflow-hidden bg-black/60 p-2">
                  <img
                    src="/images/850969292136947300.jpeg"
                    alt="Dil Thanda Rakh poster - Keep Cool Under Pressure"
                    className="w-full h-[400px] sm:h-[450px] object-contain mx-auto rounded"
                    loading="lazy"
                  />
                  <div className="absolute bottom-4 left-4 right-4 p-3 rounded bg-black/85 backdrop-blur border border-gold/30 text-center">
                    <span className="font-mono text-xs font-bold text-gold uppercase tracking-wider block">
                      DIL THANDA RAKH • ZERO CHOKE
                    </span>
                    <span className="text-[11px] text-text-muted">
                      Composure Under Pressure as an Empirical Estimand
                    </span>
                  </div>
                </div>
              </div>
            </ScrollReveal>
          </div>

          {/* Right Column: The 7 Analytical Rigor Pillars */}
          <div className="lg:col-span-7 space-y-4">
            <ScrollReveal animation="fade-left" delay={150}>
              <div className="mb-4">
                <span className="font-mono text-xs text-icevein uppercase tracking-widest block font-bold mb-1">
                  TACTICAL EVALUATION CRITERIA
                </span>
                <h3 className="text-xl sm:text-2xl font-bold text-white">
                  Why Raw Totals Deceive IPL Decision-Makers
                </h3>
              </div>

              <div className="space-y-3 font-body">
                {pillars.map((p, idx) => (
                  <div 
                    key={idx}
                    className="p-3.5 rounded-lg bg-dark-elevated border border-dark-border/60 hover:border-pinkops/40 transition-colors flex items-start gap-3.5"
                  >
                    <div className="w-6 h-6 rounded-full bg-pinkops/15 text-pinkops flex items-center justify-center font-mono text-xs font-bold shrink-0 mt-0.5">
                      0{idx + 1}
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-white mb-0.5">
                        {p.label}
                      </h4>
                      <p className="text-xs text-text-muted leading-relaxed">
                        {p.detail}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollReveal>
          </div>

        </div>

      </div>
    </section>
  );
}
