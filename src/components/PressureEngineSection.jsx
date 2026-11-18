import React, { useState } from 'react';
import ScrollReveal from './ScrollReveal';
import { Activity, Flame, Gauge, Sliders, Zap, ArrowRight, ShieldAlert } from 'lucide-react';

export default function PressureEngineSection() {
  const [activeStage, setActiveStage] = useState(2); // Default to High Pressure

  const pressureLevels = [
    {
      level: 'CALM',
      piRange: 'PI < 0.35',
      percent: 25,
      color: '#00E5FF',
      desc: 'Early innings, low required rate, all 10 wickets intact. Low leverage, high noise.'
    },
    {
      level: 'BUILDING',
      piRange: '0.35 ≤ PI < 0.48',
      percent: 50,
      color: '#00E676',
      desc: 'Middle overs contest, wicket fell recently, required run rate climbing toward 8.5 rpo.'
    },
    {
      level: 'HIGH',
      piRange: '0.48 ≤ PI < 0.5898',
      percent: 75,
      color: '#FFAB00',
      desc: 'Chasing side 4 down, 42 runs required off 24 balls. Match win probability swinging violently with each boundary.'
    },
    {
      level: 'CRITICAL (PI_80)',
      piRange: 'PI ≥ 0.5898',
      percent: 100,
      color: '#FF2A85',
      desc: 'Top 20% most intense competitive deliveries. 18 required off 10 balls, death yorker vs boundary execution. The PinkOps proving ground.'
    }
  ];

  const pipelineStages = [
    {
      step: '01',
      name: 'MATCH STATE',
      inputs: ['Balls Remaining', 'Runs to Target', 'Wickets in Hand', 'Venue Par'],
      desc: 'Raw situational inputs captured dynamically at the moment the bowler begins their run-up.'
    },
    {
      step: '02',
      name: 'OPPORTUNITY',
      inputs: ['Innings Phase', 'Batting Position', 'Over Number', 'Field Restrictions'],
      desc: 'Differentiates opening luxury from high-urgency death-overs finishing opportunities.'
    },
    {
      step: '03',
      name: 'PRESSURE INDEX (PI)',
      inputs: ['Win Probability Swing (WPA)', 'Required Run Rate Stress', 'Resource Scarcity'],
      desc: 'Continuous non-linear leverage calculation. Isolates top 20% leverage threshold (PI_80 ≥ 0.5898).'
    },
    {
      step: '04',
      name: 'PLAYER ACTION',
      inputs: ['Shot Selection', 'Execution Type', 'Line & Length Target', 'Pace Variation'],
      desc: 'The technical and psychological response of the player under observed match stress.'
    },
    {
      step: '05',
      name: 'CONTEXTUAL OUTCOME',
      inputs: ['Actual Runs vs Spec B Expected', 'Dismissal vs Expected Wicket Probability'],
      desc: 'Evaluates delta value-added relative to situation par without self-conditioning bias.'
    },
    {
      step: '06',
      name: 'RELIABILITY SIGNAL',
      inputs: ['Empirical Bayes LUB20', 'MAD Consistency', 'Downside Hard Gate Check'],
      desc: 'Defensible downside performance floor proving the player will not choke under pressure.'
    }
  ];

  const currentLevel = pressureLevels[activeStage];

  return (
    <section id="pressure" className="section-py bg-dark-surface/60 relative border-t border-dark-border">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="max-w-4xl mx-auto text-center mb-16">
          <ScrollReveal animation="fade-up">
            <span className="font-mono text-xs font-bold uppercase tracking-widest text-icevein block mb-3">
              02 • THE PRESSURE ENGINE
            </span>
            <h2 className="text-3xl sm:text-5xl md:text-6xl font-black text-white uppercase tracking-tight mb-6">
              PRESSURE IS A STATE. <br />
              <span className="neon-cyan-text">NOT A LABEL.</span>
            </h2>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed max-w-2xl mx-auto">
              Pressure is not binary. It is a continuous, dynamic state dictated by resource exhaustion, scoreboard urgency, and win-probability volatility. Here is how PinkOps models leverage.
            </p>
          </ScrollReveal>
        </div>

        {/* Interactive Live Pressure Simulator */}
        <div className="hud-panel p-6 sm:p-8 mb-16 border border-icevein/30">
          <div className="hud-bracket bracket-tl" />
          <div className="hud-bracket bracket-tr" />
          <div className="hud-bracket bracket-bl" />
          <div className="hud-bracket bracket-br" />

          <div className="flex flex-col md:flex-row items-center justify-between gap-6 pb-6 border-b border-dark-border">
            <div>
              <span className="font-mono text-xs text-text-muted uppercase tracking-wider block">
                CONTINUOUS PRESSURE INTENSITY (PI) SIMULATOR
              </span>
              <h3 className="text-xl sm:text-2xl font-bold text-white mt-1">
                Live State: <span style={{ color: currentLevel.color }}>{currentLevel.level}</span>
              </h3>
            </div>

            {/* Stage Selector Buttons */}
            <div className="flex flex-wrap gap-2">
              {pressureLevels.map((lvl, idx) => (
                <button
                  type="button"
                  key={idx}
                  onClick={() => setActiveStage(idx)}
                  className={`px-3 py-1.5 rounded font-mono text-xs font-bold uppercase cursor-pointer transition-all border ${
                    activeStage === idx
                      ? 'bg-pinkops/20 text-white border-pinkops shadow-tactical'
                      : 'bg-dark-elevated text-text-muted border-dark-border hover:text-white'
                  }`}
                  style={{
                    backgroundColor: activeStage === idx ? 'rgba(255, 42, 133, 0.25)' : 'var(--color-dark-elevated)',
                    borderColor: activeStage === idx ? 'var(--color-pinkops)' : 'var(--color-dark-border)',
                    color: activeStage === idx ? '#FFFFFF' : 'var(--color-text-muted)',
                  }}
                >
                  {lvl.level.split(' ')[0]}
                </button>
              ))}
            </div>
          </div>

          {/* Dynamic Meter Bar */}
          <div className="py-6">
            <div className="flex items-center justify-between font-mono text-xs text-text-muted mb-2">
              <span>LEVERAGE SPECTRUM</span>
              <span style={{ color: currentLevel.color }} className="font-bold">
                {currentLevel.piRange} ({currentLevel.percent}%)
              </span>
            </div>
            <div className="pressure-meter-track">
              <div 
                className="pressure-meter-fill"
                style={{ width: `${currentLevel.percent}%` }}
              />
            </div>
            <p className="text-xs sm:text-sm text-text-main mt-4 leading-relaxed font-body">
              {currentLevel.desc}
            </p>
          </div>

          {/* Variable Telemetry Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-dark-border/60 font-mono text-xs">
            <div className="p-2.5 rounded bg-black/40 border border-dark-border">
              <span className="text-text-faint block">RUNS REQ:</span>
              <span className="font-bold text-white">{activeStage === 3 ? '18 off 10 balls' : activeStage === 2 ? '42 off 24 balls' : '76 off 60 balls'}</span>
            </div>
            <div className="p-2.5 rounded bg-black/40 border border-dark-border">
              <span className="text-text-faint block">WICKETS IN HAND:</span>
              <span className="font-bold text-pinkops">{activeStage === 3 ? '3 wickets' : activeStage === 2 ? '5 wickets' : '9 wickets'}</span>
            </div>
            <div className="p-2.5 rounded bg-black/40 border border-dark-border">
              <span className="text-text-faint block">RUN RATE STRESS:</span>
              <span className="font-bold text-gold">{activeStage === 3 ? '10.80 rpo' : activeStage === 2 ? '10.50 rpo' : '7.60 rpo'}</span>
            </div>
            <div className="p-2.5 rounded bg-black/40 border border-dark-border">
              <span className="text-text-faint block">PROVING GROUND:</span>
              <span className="font-bold text-icevein">{activeStage === 3 ? 'TOP 20% (PI_80)' : 'BASELINE'}</span>
            </div>
          </div>
        </div>

        {/* 6-Stage Delivery Pipeline Flow */}
        <div className="mb-8">
          <div className="text-center max-w-xl mx-auto mb-10">
            <h3 className="text-2xl font-bold text-white uppercase tracking-tight">
              Delivery Pipeline Architecture
            </h3>
            <p className="text-xs sm:text-sm text-text-muted mt-1">
              How a single delivery transforms into a statistically defensible reliability signal.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {pipelineStages.map((st, idx) => (
              <ScrollReveal key={idx} animation="fade-up" delay={idx * 60}>
                <div className="hud-panel p-5 h-full flex flex-col justify-between bg-dark-elevated/70 border border-dark-border hover:border-pinkops/40">
                  <div>
                    <div className="flex items-center justify-between pb-3 border-b border-dark-border/40 mb-3 font-mono">
                      <span className="text-xs font-bold text-pinkops">{st.step}</span>
                      <span className="text-[11px] text-text-faint uppercase">ENGINE STAGE</span>
                    </div>
                    <h4 className="text-base font-bold text-white mb-2 font-mono">
                      {st.name}
                    </h4>
                    <p className="text-xs text-text-muted leading-relaxed mb-4">
                      {st.desc}
                    </p>
                  </div>

                  <div className="pt-3 border-t border-dark-border/40 font-mono text-[11px]">
                    <span className="text-text-faint block mb-1">KEY VARIABLES:</span>
                    <div className="flex flex-wrap gap-1.5">
                      {st.inputs.map((inp, i) => (
                        <span key={i} className="px-2 py-0.5 rounded bg-black/50 text-text-muted border border-dark-border/60">
                          {inp}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>

      </div>
    </section>
  );
}
