import React, { useState } from 'react';
import ScrollReveal from './ScrollReveal';
import { FINAL_10_BATTERS, FINAL_10_BOWLERS } from '../data/pinkopsData';
import { Trophy, ShieldCheck, Flame, ChevronRight, Activity, Award } from 'lucide-react';

export default function PinkOpsBoard({ onSelectPlayer }) {
  const [activeTab, setActiveTab] = useState('batters'); // 'batters' | 'bowlers'

  const playerList = activeTab === 'batters' ? FINAL_10_BATTERS : FINAL_10_BOWLERS;

  return (
    <section id="board" className="section-py bg-void relative border-t border-dark-border">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="max-w-4xl mx-auto text-center mb-14">
          <ScrollReveal animation="fade-up">
            <span className="font-mono text-xs font-bold uppercase tracking-widest text-pinkops block mb-3">
              05 • FINAL PORTFOLIOS
            </span>
            <h2 className="text-4xl sm:text-6xl md:text-7xl font-black text-white uppercase tracking-tight mb-4">
              THE PINKOPS BOARD™
            </h2>
            <p className="text-xl sm:text-2xl font-editorial italic text-gold max-w-2xl mx-auto mb-6">
              "The 10 players who survived the pressure test."
            </p>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed max-w-2xl mx-auto">
              Every player on this board possesses a positive lower uncertainty bound (LUB20 &gt; 0), passed hard downside risk gates (EDR / Blowout ≤ 20%), and achieved unanimous 8/8 multiverse support.
            </p>
          </ScrollReveal>
        </div>

        {/* Tactical Discipline Toggle (Batters Top 10 / Bowlers Top 10) */}
        <div className="flex justify-center mb-12">
          <div className="inline-flex p-1.5 rounded-xl bg-dark-elevated border border-pinkops/30 shadow-tactical">
            <button
              onClick={() => setActiveTab('batters')}
              className={`px-6 sm:px-8 py-2.5 rounded-lg font-mono text-xs sm:text-sm font-bold uppercase tracking-wider transition-all cursor-pointer ${
                activeTab === 'batters'
                  ? 'bg-pinkops text-white shadow-tactical'
                  : 'text-text-muted hover:text-white bg-transparent'
              }`}
            >
              FINAL 10 BATTERS
            </button>
            <button
              onClick={() => setActiveTab('bowlers')}
              className={`px-6 sm:px-8 py-2.5 rounded-lg font-mono text-xs sm:text-sm font-bold uppercase tracking-wider transition-all cursor-pointer ${
                activeTab === 'bowlers'
                  ? 'bg-pinkops text-white shadow-tactical'
                  : 'text-text-muted hover:text-white bg-transparent'
              }`}
            >
              FINAL 10 BOWLERS
            </button>
          </div>
        </div>

        {/* Ranked Player Cards Grid */}
        <div className="space-y-4 max-w-5xl mx-auto">
          {playerList.map((player) => {
            const isRank1 = player.rank === 1;
            const isTop3 = player.rank <= 3;
            const isBatter = player.type === 'batter';

            return (
              <ScrollReveal key={player.id} animation="fade-up" delay={player.rank * 40}>
                <div
                  onClick={() => onSelectPlayer(player)}
                  className={`hud-panel p-5 sm:p-6 transition-all cursor-pointer group ${
                    isRank1
                      ? 'border-gold bg-gradient-to-r from-dark-elevated via-[#1F1524] to-dark-elevated shadow-gold-glow'
                      : isTop3
                      ? 'border-pinkops/60 bg-dark-elevated hover:border-pinkops'
                      : 'border-dark-border bg-dark-surface/80 hover:border-pinkops/50'
                  }`}
                >
                  <div className="hud-bracket bracket-tl" />
                  <div className="hud-bracket bracket-tr" />
                  <div className="hud-bracket bracket-bl" />
                  <div className="hud-bracket bracket-br" />

                  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
                    
                    {/* Rank Number & Badge */}
                    <div className="md:col-span-4 flex items-center gap-4">
                      <div className={`w-12 h-12 rounded-lg flex items-center justify-center font-mono font-black text-xl shrink-0 ${
                        isRank1
                          ? 'bg-gold/20 text-gold-light border-2 border-gold shadow-gold-glow'
                          : isTop3
                          ? 'bg-pinkops/20 text-pinkops border border-pinkops/50'
                          : 'bg-black/50 text-text-muted border border-dark-border'
                      }`}>
                        #{player.rank}
                      </div>

                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className="text-lg sm:text-xl font-bold text-white font-mono group-hover:text-pinkops transition-colors">
                            {player.name}
                          </h3>
                          {isRank1 && (
                            <Award className="w-5 h-5 text-gold animate-bounce" />
                          )}
                        </div>
                        <p className="text-xs text-text-muted font-body">
                          {player.role}
                        </p>
                      </div>
                    </div>

                    {/* Metrics Telemetry */}
                    <div className="md:col-span-5 grid grid-cols-3 gap-2 text-center font-mono text-xs">
                      <div className="p-2 rounded bg-black/40 border border-dark-border">
                        <span className="text-[10px] text-text-faint block uppercase">LUB20 FLOOR</span>
                        <span className="font-bold text-pinkops text-sm">
                          +{player.lub20.toFixed(4)}
                        </span>
                      </div>

                      <div className="p-2 rounded bg-black/40 border border-dark-border">
                        <span className="text-[10px] text-text-faint block uppercase">PRESSURE BALLS</span>
                        <span className="font-bold text-white text-sm">
                          {player.pressureExposure}
                        </span>
                      </div>

                      <div className="p-2 rounded bg-black/40 border border-dark-border">
                        <span className="text-[10px] text-text-faint block uppercase">
                          {isBatter ? 'EARLY DISMISSAL' : 'BLOWOUT RATE'}
                        </span>
                        <span className="font-bold text-status-green text-sm">
                          {((isBatter ? player.earlyDismissalRate : player.blowoutRate) * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>

                    {/* Auction Category & Action Trigger */}
                    <div className="md:col-span-3 flex items-center justify-between md:justify-end gap-3 pt-3 md:pt-0 border-t md:border-t-0 border-dark-border/40">
                      <span className={`badge-${player.auctionCategory.toLowerCase().replace(' ', '-')}`}>
                        {player.auctionCategory}
                      </span>

                      <div className="inline-flex items-center gap-1 font-mono text-xs font-bold text-text-muted group-hover:text-pinkops transition-colors">
                        <span className="hidden sm:inline">DOSSIER</span>
                        <ChevronRight className="w-4 h-4 text-pinkops" />
                      </div>
                    </div>

                  </div>
                </div>
              </ScrollReveal>
            );
          })}
        </div>

      </div>
    </section>
  );
}
