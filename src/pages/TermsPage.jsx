import React, { useEffect } from 'react';
import { ArrowLeft, BookOpen, Scale, AlertCircle, FileCheck, Award, Zap } from 'lucide-react';

export default function TermsPage({ onNavigate }) {
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
    document.title = 'Competition Terms & Governance — PinkOps War Room';
  }, []);

  return (
    <div className="min-h-screen bg-[#09060B] py-12 text-text-main">
      <div className="site-container max-w-4xl mx-auto">
        
        {/* Navigation Back */}
        <div className="mb-8">
          <button
            onClick={() => onNavigate('/')}
            className="inline-flex items-center gap-2 text-sm font-mono font-bold text-pinkops hover:text-white transition-colors bg-transparent border-0 cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>RETURN TO WAR ROOM</span>
          </button>
        </div>

        {/* War Room Header Banner */}
        <div className="hud-panel p-8 sm:p-12 text-center bg-gradient-to-b from-[#140E1B] to-[#0D0813] mb-12 border border-pinkops/30">
          <div className="corner-bracket bracket-tl" />
          <div className="corner-bracket bracket-tr" />
          <div className="corner-bracket bracket-bl" />
          <div className="corner-bracket bracket-br" />

          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-icevein/15 text-icevein text-xs font-mono font-bold uppercase tracking-wider mb-4 border border-icevein/30">
            <Scale className="w-3.5 h-3.5" />
            <span>TERMS & COMPETITION GOVERNANCE</span>
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">
            Terms of Use & Analytical Integrity
          </h1>

          <p className="text-sm sm:text-base text-text-muted max-w-xl mx-auto font-mono text-xs uppercase tracking-widest text-text-faint">
            Rajasthan Royals SupeRR Selector Season 2 • Round 1 Competition Governance
          </p>
        </div>

        {/* Terms Content Container */}
        <div className="space-y-8">
          
          {/* Section 1 */}
          <div className="hud-panel p-6 sm:p-8 bg-dark-card border border-dark-border space-y-3">
            <div className="flex items-center gap-2 text-white">
              <FileCheck className="w-5 h-5 text-pinkops shrink-0" />
              <h2 className="text-xl font-bold font-heading-royal">1. Competition Purpose & Framework</h2>
            </div>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              This interactive dashboard is the presentation artifact of <strong className="text-white">Operation Pink Panther (PinkOps)</strong>, created specifically for the <strong className="text-white">Rajasthan Royals SupeRR Selector Season 2 — Round 1</strong>. By exploring this interface, you acknowledge that all evaluations represent analytical methodologies developed to solve the competition objective: determining the 10 most reliable batters and bowlers under high-leverage pressure.
            </p>
          </div>

          {/* Section 2 */}
          <div className="hud-panel p-6 sm:p-8 bg-dark-card border border-dark-border space-y-3">
            <div className="flex items-center gap-2 text-white">
              <Zap className="w-5 h-5 text-icevein shrink-0" />
              <h2 className="text-xl font-bold font-heading-royal">2. Proprietary Methodology & Intellectual Property</h2>
            </div>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              The proprietary analytics engines demonstrated on this platform—including:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-sm sm:text-base text-text-muted">
              <li><strong className="text-white">Choke Detector™:</strong> Empirical gap analysis between baseline performance and high-pressure index conditions.</li>
              <li><strong className="text-white">IceVein Score™:</strong> Multi-dimensional composure and high-leverage efficiency formulation.</li>
              <li><strong className="text-white">Pressure Lens™:</strong> Non-linear leverage weight distribution based on match situation, run rate req., and wickets remaining.</li>
              <li><strong className="text-white">Smoke Test™:</strong> Robustness screening through 24 multiverse specifications and 10,000 bootstrap resamples.</li>
              <li><strong className="text-white">LUB20 Lower Bound Metric:</strong> 20th percentile conservative uncertainty floor preventing small-sample distortion.</li>
            </ul>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              are original analytical models authored by the PinkOps research group. All rights to the mathematical formulations and execution code remain with the project authors.
            </p>
          </div>

          {/* Section 3 */}
          <div className="hud-panel p-6 sm:p-8 bg-dark-card border border-dark-border space-y-3">
            <div className="flex items-center gap-2 text-white">
              <BookOpen className="w-5 h-5 text-sandstone shrink-0" />
              <h2 className="text-xl font-bold font-heading-royal">3. Rajasthan Royals & IPL Intellectual Property</h2>
            </div>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              The Rajasthan Royals name, official team crest, "Halla Bol" motto, "Dil Thanda Rakh" art motifs, and royal pink/blue visual elements are the exclusive intellectual property of the Rajasthan Royals and Royal Multisport Private Limited. This site uses these references strictly in compliance with competition submission guidelines.
            </p>
          </div>

          {/* Section 4 */}
          <div className="hud-panel p-6 sm:p-8 bg-dark-card border border-dark-border space-y-3">
            <div className="flex items-center gap-2 text-white">
              <AlertCircle className="w-5 h-5 text-amber-400 shrink-0" />
              <h2 className="text-xl font-bold font-heading-royal">4. Competition Invariants & Auction Availability Rules</h2>
            </div>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              In accordance with official SupeRR Selector competition rules:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-sm sm:text-base text-text-muted">
              <li>Candidates are evaluated objectively on the provided competition dataset regardless of current franchise retention or availability status.</li>
              <li>Final auction targets and role portfolios differentiate between tactical benchmarks (e.g. Jasprit Bumrah as the universal bowling gold standard) and auction-viable targets (e.g. Jamie Overton, Abrar Ahmed).</li>
              <li>No synthetic auction prices or imaginary purse caps are fabricated outside verified RR 2027 context (19 retained, 6 open slots, ₹27.05 Cr available).</li>
            </ul>
          </div>

          {/* Section 5 */}
          <div className="hud-panel p-6 sm:p-8 bg-dark-card border border-dark-border space-y-3">
            <div className="flex items-center gap-2 text-white">
              <Scale className="w-5 h-5 text-pinkops shrink-0" />
              <h2 className="text-xl font-bold font-heading-royal">5. Disclaimer of Warranties</h2>
            </div>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              The data visualisations, statistics, and model outputs are provided "as-is" for competition judgment. While audited with 0 duplicates across 200,999 balls, future performance under varying real-world conditions remains inherently stochastic. PinkOps makes no financial or sporting guarantees beyond empirical mathematical rigor.
            </p>
          </div>

        </div>

        {/* Bottom Back Button */}
        <div className="text-center mt-12">
          <button
            onClick={() => onNavigate('/')}
            className="btn-pinkops-primary py-3 px-8 text-xs font-mono font-bold tracking-wider"
          >
            <ArrowLeft className="w-4 h-4 text-white" />
            <span>RETURN TO WAR ROOM</span>
          </button>
        </div>

      </div>
    </div>
  );
}
