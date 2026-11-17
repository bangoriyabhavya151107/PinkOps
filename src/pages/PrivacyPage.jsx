import React, { useEffect } from 'react';
import OrnamentalDivider from '../components/OrnamentalDivider';
import { ArrowLeft, Shield, Lock, EyeOff, FileText, CheckCircle2 } from 'lucide-react';

export default function PrivacyPage({ onNavigate }) {
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
    document.title = 'Privacy Policy — Rajasthan Heritage Dashboard';
  }, []);

  return (
    <div className="min-h-screen bg-parchment-texture py-12">
      <div className="site-container max-w-4xl mx-auto">
        
        {/* Navigation Back */}
        <div className="mb-8">
          <button
            onClick={() => onNavigate('/')}
            className="inline-flex items-center gap-2 text-sm font-bold text-maroon hover:text-gold transition-colors bg-transparent border-0 cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Return to Rajasthan Cultural Dashboard</span>
          </button>
        </div>

        {/* Regal Cultural Header Banner */}
        <div className="jharokha-frame p-8 sm:p-12 text-center bg-gradient-to-b from-[#FFFDF9] to-[#FAF4E8] mb-12">
          <div className="corner-flourish corner-tl" />
          <div className="corner-flourish corner-tr" />
          <div className="corner-flourish corner-bl" />
          <div className="corner-flourish corner-br" />

          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-gold/15 text-maroon text-xs font-bold uppercase tracking-wider mb-4 border border-gold/40">
            <Shield className="w-3.5 h-3.5 text-gold" />
            <span>Legal & Privacy Governance</span>
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-maroon mb-4">
            Privacy Policy
          </h1>

          <p className="text-sm sm:text-base text-ink-muted max-w-xl mx-auto font-editorial text-lg italic">
            Transparent disclosure of digital integrity, user privacy, and zero data-collection principles for the Rajasthan Cultural Heritage Dashboard.
          </p>

          <OrnamentalDivider motif="✦" className="mt-6" />
        </div>

        {/* Legal Policy Content Container */}
        <div className="parchment-card p-6 sm:p-10 space-y-8 text-ink">
          
          {/* Section 1 */}
          <section className="space-y-3">
            <div className="flex items-center gap-2 text-maroon">
              <FileText className="w-5 h-5 text-gold shrink-0" />
              <h2 className="text-xl sm:text-2xl font-bold font-body">1. Introduction & Ethical Stance</h2>
            </div>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              The Rajasthan Cultural Heritage Dashboard ("PinkOps", "we", "our", or "us") is dedicated to celebrating the living heritage, folk arts, and architectural marvels of Rajasthan. We uphold a strict standard of epistemic honesty and privacy protection. This Privacy Policy details the complete operational boundaries of this website.
            </p>
          </section>

          {/* Section 2 */}
          <section className="space-y-3">
            <div className="flex items-center gap-2 text-maroon">
              <EyeOff className="w-5 h-5 text-gold shrink-0" />
              <h2 className="text-xl sm:text-2xl font-bold font-body">2. Information We Do Not Collect</h2>
            </div>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              In accordance with our client-first frontend architecture:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-sm sm:text-base text-ink-muted">
              <li><strong>No User Accounts or Passwords:</strong> We do not require registration, passwords, or personal login profiles.</li>
              <li><strong>No Financial or Payment Data:</strong> There are no commercial bookings, ticket sales, or financial checkout integrations on this site.</li>
              <li><strong>No Tracking Cookies or Cross-Site Beacons:</strong> We do not deploy third-party advertising cookies, fingerprinting scripts, or cross-site behavioral trackers.</li>
              <li><strong>No Server-Side Personal Telemetry:</strong> User interactions remain local to your browser session.</li>
            </ul>
          </section>

          {/* Section 3 */}
          <section className="space-y-3">
            <div className="flex items-center gap-2 text-maroon">
              <Lock className="w-5 h-5 text-gold shrink-0" />
              <h2 className="text-xl sm:text-2xl font-bold font-body">3. Client-Side Preferences & Local Storage</h2>
            </div>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              The website may read system media queries (such as <code className="text-maroon font-semibold">prefers-reduced-motion</code>) directly from your browser to automatically disable animations and customize visual accessibility for individuals sensitive to motion. No personal telemetry is transmitted during this process.
            </p>
          </section>

          {/* Section 4 */}
          <section className="space-y-3">
            <div className="flex items-center gap-2 text-maroon">
              <CheckCircle2 className="w-5 h-5 text-gold shrink-0" />
              <h2 className="text-xl sm:text-2xl font-bold font-body">4. Third-Party CDNs & Fonts</h2>
            </div>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              To deliver cultural typography (Cinzel, Cormorant Garamond, Plus Jakarta Sans, and Devanagari letterforms), this website requests fonts via standard Google Fonts endpoints. These requests are governed by Google's public privacy policies and are cached locally by your browser for optimal performance.
            </p>
          </section>

          {/* Section 5 */}
          <section className="space-y-3">
            <div className="flex items-center gap-2 text-maroon">
              <Shield className="w-5 h-5 text-gold shrink-0" />
              <h2 className="text-xl sm:text-2xl font-bold font-body">5. Children's Privacy</h2>
            </div>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              Our cultural exhibition is entirely educational and suitable for audiences of all ages. Because we do not collect personal information of any kind, we adhere strictly to the Children's Online Privacy Protection Act (COPPA) and international child privacy benchmarks.
            </p>
          </section>

          {/* Section 6 */}
          <section className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold font-body text-maroon">6. Updates & Inquiries</h2>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              Should this policy be amended to reflect architectural updates, changes will be timestamped immediately on this page. For cultural inquiries or archival attribution queries, please contact the PinkOps repository maintainers.
            </p>
            <div className="p-4 rounded-lg bg-gold/10 border border-gold/30 text-xs sm:text-sm text-maroon">
              <strong>Last Updated:</strong> November 2026 • Verified Zero Data-Collection Baseline.
            </div>
          </section>

        </div>

        {/* Bottom Back Button */}
        <div className="text-center mt-10">
          <button
            onClick={() => onNavigate('/')}
            className="btn-royal-primary"
          >
            <ArrowLeft className="w-4 h-4 text-gold" />
            <span>Return to Rajasthan Cultural Dashboard</span>
          </button>
        </div>

      </div>
    </div>
  );
}
