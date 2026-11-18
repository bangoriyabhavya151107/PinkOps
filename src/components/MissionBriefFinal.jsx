import React from 'react';
import ScrollReveal from './ScrollReveal';
import { MISSION_BRIEF_SYNTHESIS } from '../data/pinkopsData';
import { Award, Zap, ShieldCheck, Flame, HelpCircle, Lightbulb } from 'lucide-react';

export default function MissionBriefFinal({ onScrollToTop }) {
  const cards = [
    {
      title: 'STRONGEST SIGNAL',
      icon: Award,
      color: 'text-pinkops',
      borderColor: 'border-pinkops/50',
      data: MISSION_BRIEF_SYNTHESIS.strongestSignal
    },
    {
      title: 'BIGGEST SURPRISE',
      icon: Zap,
      color: 'text-gold',
      borderColor: 'border-gold/50',
      data: MISSION_BRIEF_SYNTHESIS.biggestSurprise
    },
    {
      title: 'MOST ROBUST PLAYER',
      icon: ShieldCheck,
      color: 'text-icevein',
      borderColor: 'border-icevein/50',
      data: MISSION_BRIEF_SYNTHESIS.mostRobustPlayer
    },
    {
      title: 'STRONGEST PRESSURE PERFORMER',
      icon: Flame,
      color: 'text-status-green',
      borderColor: 'border-status-green/50',
      data: MISSION_BRIEF_SYNTHESIS.strongestPressurePerformer
    },
    {
      title: 'HIGHEST UNCERTAINTY PLAYER',
      icon: HelpCircle,
      color: 'text-text-faint',
      borderColor: 'border-dark-border',
      data: MISSION_BRIEF_SYNTHESIS.highestUncertaintyPlayer
    },
    {
      title: 'STRATEGIC IMPLICATION',
      icon: Lightbulb,
      color: 'text-white',
      borderColor: 'border-gold/40',
      data: {
        player: MISSION_BRIEF_SYNTHESIS.strategicImplication.headline,
        role: 'Rajasthan Royals IPL 2027',
        stat: 'Downside Protection Wins Championships',
        detail: MISSION_BRIEF_SYNTHESIS.strategicImplication.detail
      }
    }
  ];

  return (
    <section className="section-py bg-void relative border-t border-dark-border">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="max-w-4xl mx-auto text-center mb-16">
          <ScrollReveal animation="fade-up">
            <span className="font-mono text-xs font-bold uppercase tracking-widest text-gold block mb-3">
              07 • EXECUTIVE SYNTHESIS
            </span>
            <h2 className="text-3xl sm:text-5xl md:text-6xl font-black text-white uppercase tracking-tight mb-4">
              FINAL MISSION BRIEF
            </h2>
            <p className="text-xl sm:text-2xl font-editorial italic text-gold max-w-2xl mx-auto mb-6">
              "The definitive answers to the competition mandate."
            </p>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed max-w-2xl mx-auto">
              Grounded in 200,999 competition deliveries, 867 contested matches, and 24 multiverse specifications.
            </p>
          </ScrollReveal>
        </div>

        {/* 6 Key Findings Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {cards.map((card, idx) => {
            const IconComp = card.icon;

            return (
              <ScrollReveal key={idx} animation="fade-up" delay={idx * 60}>
                <div className={`hud-panel p-6 h-full flex flex-col justify-between bg-dark-elevated border ${card.borderColor}`}>
                  <div>
                    <div className="flex items-center justify-between pb-3 border-b border-dark-border/40 mb-4">
                      <div className="flex items-center gap-2">
                        <IconComp className={`w-4 h-4 ${card.color}`} />
                        <span className={`font-mono text-xs font-bold uppercase tracking-wider ${card.color}`}>
                          {card.title}
                        </span>
                      </div>
                      <span className="font-mono text-xs text-text-faint">0{idx + 1}</span>
                    </div>

                    <h3 className="text-xl font-bold text-white font-mono mb-1">
                      {card.data.player}
                    </h3>
                    <p className="text-xs font-semibold text-gold mb-3 font-editorial text-base italic">
                      {card.data.role}
                    </p>

                    <div className="p-2 rounded bg-black/40 border border-dark-border font-mono text-xs text-pinkops font-bold mb-4">
                      {card.data.stat}
                    </div>

                    <p className="text-xs sm:text-sm text-text-muted leading-relaxed font-body">
                      {card.data.detail}
                    </p>
                  </div>
                </div>
              </ScrollReveal>
            );
          })}
        </div>

        {/* Closing Action */}
        <div className="text-center">
          <button
            onClick={onScrollToTop}
            className="btn-pinkops-primary py-3 px-8 text-sm"
          >
            <span>RETURN TO WAR ROOM ZENITH</span>
          </button>
        </div>

      </div>
    </section>
  );
}
