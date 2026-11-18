import React from 'react';
import { ArrowDown, Activity, ShieldCheck, Flame, Compass } from 'lucide-react';
import { AUDIT_STATS } from '../data/pinkopsData';

export default function HeroWarRoom({ onExploreMission, onExploreBoard }) {
  return (
    <section id="hero" className="relative min-h-[94vh] flex flex-col justify-between pt-8 pb-10 overflow-hidden bg-tactical-grid">
      {/* Background Ambient Glows */}
      <div 
        className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full pointer-events-none opacity-20"
        style={{
          background: 'radial-gradient(circle, var(--color-pinkops) 0%, transparent 70%)',
          filter: 'blur(80px)',
          zIndex: 'var(--z-base)'
        }}
        aria-hidden="true"
      />

      <div className="site-container relative" style={{ zIndex: 'var(--z-content)' }}>
        
        {/* Eyebrow & Status Ticker */}
        <div className="text-center hero-anim-1">
          <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-dark-elevated border border-pinkops/30 shadow-tactical mb-5">
            <span className="w-2 h-2 rounded-full bg-pinkops animate-ping" />
            <span className="font-mono text-xs font-bold tracking-widest text-pinkops uppercase">
              RR SUPERR SELECTOR S2 • ROUND 1
            </span>
            <span className="text-text-faint">•</span>
            <span className="font-mono text-xs text-text-muted">STAGE 6 SUBMISSION ACTIVE</span>
          </div>
        </div>

        {/* Large Cinematic Title */}
        <div className="text-center max-w-5xl mx-auto hero-anim-2">
          <h1 className="text-4xl sm:text-6xl md:text-7xl lg:text-8xl font-black text-white tracking-tight leading-[1.05] uppercase mb-4">
            OPERATION <br />
            <span className="neon-pink-text">PINK PANTHER</span>
          </h1>
        </div>

        {/* Main Tagline & Supporting Line */}
        <div className="text-center max-w-3xl mx-auto hero-anim-3 mb-6">
          <p className="text-xl sm:text-2xl md:text-3xl font-semibold text-gold font-editorial italic mb-3">
            Finding the Next Legend
          </p>
          <p className="text-base sm:text-lg font-mono text-white/90 font-bold tracking-wide">
            10 players. One pressure test. Zero guesswork.
          </p>
        </div>

        {/* Short Mission Explanation */}
        <div className="text-center max-w-2xl mx-auto hero-anim-4 mb-8">
          <p className="text-sm sm:text-base text-text-muted leading-relaxed">
            A pressure-first intelligence system designed to identify the most reliable players in the competition dataset for Rajasthan Royals' IPL 2027 strategy.
          </p>
        </div>

        {/* Tactical CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-4 hero-anim-5 mb-10">
          <button
            onClick={onExploreBoard}
            className="btn-pinkops-primary"
            aria-label="View the Final PinkOps Top 10 Board"
          >
            <Activity className="w-4 h-4 text-white" />
            <span>ACCESS PINKOPS BOARD™</span>
          </button>
          <button
            onClick={onExploreMission}
            className="btn-pinkops-secondary"
            aria-label="Deconstruct the Pressure Engine Methodology"
          >
            <Compass className="w-4 h-4 text-pinkops" />
            <span>ENTER THE WAR ROOM</span>
          </button>
        </div>

        {/* Visual Composition: Halla Bol Neon & Tactical HUD */}
        <div className="relative max-w-4xl mx-auto hero-anim-5">
          <div className="hud-panel p-4 sm:p-6 bg-dark-surface/90 border border-pinkops/30 overflow-hidden">
            <div className="hud-bracket bracket-tl" />
            <div className="hud-bracket bracket-tr" />
            <div className="hud-bracket bracket-bl" />
            <div className="hud-bracket bracket-br" />

            <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
              
              {/* Left: Tactical Metrics Telemetry */}
              <div className="md:col-span-5 space-y-3 font-mono text-xs">
                <div className="flex items-center justify-between p-2.5 rounded bg-black/40 border border-dark-border">
                  <span className="text-text-muted">DELIVERIES AUDITED:</span>
                  <span className="font-bold text-white">{AUDIT_STATS.totalDeliveries.toLocaleString()}</span>
                </div>
                <div className="flex items-center justify-between p-2.5 rounded bg-black/40 border border-dark-border">
                  <span className="text-text-muted">PRESSURE THRESHOLD:</span>
                  <span className="font-bold text-pinkops">PI ≥ 0.5898 (TOP 20%)</span>
                </div>
                <div className="flex items-center justify-between p-2.5 rounded bg-black/40 border border-dark-border">
                  <span className="text-text-muted">SUPER OVER BALLS:</span>
                  <span className="font-bold text-gold">{AUDIT_STATS.superOverDeliveries} (6 MATCHES)</span>
                </div>
                <div className="flex items-center justify-between p-2.5 rounded bg-black/40 border border-dark-border">
                  <span className="text-text-muted">MULTIVERSE BRANCHES:</span>
                  <span className="font-bold text-icevein">24 (8/8 SUPPORT)</span>
                </div>
              </div>

              {/* Center / Right: Rajasthan Royals Halla Bol Hero Visual */}
              <div className="md:col-span-7 relative flex items-center justify-center">
                <div className="relative w-full h-56 sm:h-64 rounded-lg overflow-hidden border border-pinkops/40 shadow-tactical group">
                  <img
                    src="/images/RAJASTHAN%20ROYALS%F0%9F%92%9D.jpeg"
                    alt="Rajasthan Royals Halla Bol Glowing Neon Script"
                    className="w-full h-full object-cover object-center filter contrast-125 transition-transform duration-700 group-hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/30" />
                  
                  <div className="absolute bottom-3 left-4 right-4 flex items-center justify-between text-xs">
                    <span className="font-mono text-pinkops font-bold tracking-wider">
                      HALLA BOL! • ZERO CHOKE. ALL SMOKE.
                    </span>
                    <span className="px-2 py-0.5 rounded bg-pinkops text-white text-[10px] font-extrabold uppercase">
                      VERIFIED
                    </span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>

      {/* Animated Scroll Indicator */}
      <div className="text-center pt-6">
        <button
          onClick={onExploreMission}
          className="inline-flex flex-col items-center gap-1.5 text-text-muted hover:text-pinkops transition-colors bg-transparent border-0 cursor-pointer"
          aria-label="Scroll down to explore the mission"
        >
          <span className="font-mono text-[10px] font-bold tracking-widest uppercase">
            SCROLL TO DECONSTRUCT PRESSURE
          </span>
          <div className="animate-scroll-indicator p-1 rounded-full border border-pinkops/40">
            <ArrowDown className="w-3.5 h-3.5 text-pinkops" />
          </div>
        </button>
      </div>
    </section>
  );
}
