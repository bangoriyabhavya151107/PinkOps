import React, { useEffect } from 'react';
import { ArrowLeft, Shield, Lock, EyeOff, FileText, CheckCircle2, Database, AlertCircle } from 'lucide-react';

export default function PrivacyPage({ onNavigate }) {
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
    document.title = 'Confidentiality & Privacy Policy — PinkOps War Room';
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

          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-pinkops/15 text-pinkops text-xs font-mono font-bold uppercase tracking-wider mb-4 border border-pinkops/30">
            <Shield className="w-3.5 h-3.5" />
            <span>GOVERNANCE & DATA RIGOR</span>
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">
            Confidentiality & Privacy Policy
          </h1>

          <p className="text-sm sm:text-base text-text-muted max-w-xl mx-auto font-mono text-xs uppercase tracking-widest text-text-faint">
            Operation Pink Panther • PinkOps Intelligence Group • Rajasthan Royals SupeRR Selector S2 R1
          </p>
        </div>

        {/* Legal Policy Content Container */}
        <div className="space-y-8">
          
          {/* Section 1 */}
          <div className="hud-panel p-6 sm:p-8 bg-dark-card border border-dark-border space-y-3">
            <div className="flex items-center gap-2 text-white">
              <FileText className="w-5 h-5 text-pinkops shrink-0" />
              <h2 className="text-xl font-bold font-heading-royal">1. Analytical Scope & Competition Context</h2>
            </div>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              Operation Pink Panther ("PinkOps", "we", "our") is the research and competition engineering deployment created for the <strong className="text-white">Rajasthan Royals SupeRR Selector Season 2 — Round 1</strong>. Our objective is strictly analytical: answering <em>"Which 10 players in the provided competition dataset are the most reliable under pressure?"</em> This policy establishes our epistemic integrity, user confidentiality, and data protection boundaries.
            </p>
          </div>

          {/* Section 2 */}
          <div className="hud-panel p-6 sm:p-8 bg-dark-card border border-dark-border space-y-3">
            <div className="flex items-center gap-2 text-white">
              <Database className="w-5 h-5 text-icevein shrink-0" />
              <h2 className="text-xl font-bold font-heading-royal">2. Proprietary Competition Dataset Protection</h2>
            </div>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              In strict accordance with the SupeRR Selector competition terms:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-sm sm:text-base text-text-muted">
              <li><strong>Zero Raw Dataset Exposure:</strong> No raw ball-by-ball delivery microdata from the 200,999 delivery dataset is published, redistributable, or downloadable via this web interface.</li>
              <li><strong>Presentation Layer Only:</strong> The frontend only renders aggregated statistical indicators, lower bound estimates (LUB20), exposure counts, and empirical evaluations generated through validated offline analytical stages.</li>
              <li><strong>Audit Transparency:</strong> The dataset underwent a zero-defect audit (0 duplicate delivery rows across 883 matches and 6 Super Overs) documented in our verification reports.</li>
            </ul>
          </div>

          {/* Section 3 */}
          <div className="hud-panel p-6 sm:p-8 bg-dark-card border border-dark-border space-y-3">
            <div className="flex items-center gap-2 text-white">
              <EyeOff className="w-5 h-5 text-pinkops shrink-0" />
              <h2 className="text-xl font-bold font-heading-royal">3. User Data We Do Not Collect</h2>
            </div>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              This dashboard operates entirely client-side for presentation:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-sm sm:text-base text-text-muted">
              <li><strong>No Accounts or Authentication:</strong> Visitors are not asked to register, sign in, or provide personal credentials.</li>
              <li><strong>No Commercial or Financial Telemetry:</strong> No payment gateways, bidding systems, or personal financial details are processed.</li>
              <li><strong>No Cross-Site Ad Tracking:</strong> We do not deploy third-party advertising cookies, behavioral beacons, or marketing tracking pixels.</li>
              <li><strong>No Server-Side Analytics:</strong> Interaction states (such as active role tabs or simulated pressure levels) are transient to your browser session.</li>
            </ul>
          </div>

          {/* Section 4 */}
          <div className="hud-panel p-6 sm:p-8 bg-dark-card border border-dark-border space-y-3">
            <div className="flex items-center gap-2 text-white">
              <Lock className="w-5 h-5 text-sandstone shrink-0" />
              <h2 className="text-xl font-bold font-heading-royal">4. Client-Side Preferences & Accessibility</h2>
            </div>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              The application queries system accessibility media queries (such as <code className="text-pinkops font-mono">prefers-reduced-motion</code>) directly through your browser to provide comfortable, motion-reduced experiences for users sensitive to animations. No data leaves your machine during this evaluation.
            </p>
          </div>

          {/* Section 5 */}
          <div className="hud-panel p-6 sm:p-8 bg-dark-card border border-dark-border space-y-3">
            <div className="flex items-center gap-2 text-white">
              <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
              <h2 className="text-xl font-bold font-heading-royal">5. Competition Non-Commercial Disclosure</h2>
            </div>
            <p className="text-sm sm:text-base text-text-muted leading-relaxed">
              This web platform is constructed exclusively for non-commercial competition evaluation and analytical peer review for the Rajasthan Royals franchise. All trademarks, player names, and team crests remain the intellectual property of their respective owners.
            </p>
            <div className="p-3.5 rounded bg-black/40 border border-dark-border text-xs text-text-faint font-mono mt-4">
              <strong className="text-pinkops">VERIFIED AUDIT STATUS:</strong> STAGE_4_1_1_RECONCILED = TRUE • COMPOSITE_SCORE_FABRICATION = FALSE • ZERO DATA HARVESTING.
            </div>
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
