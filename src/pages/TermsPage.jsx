import React, { useEffect } from 'react';
import OrnamentalDivider from '../components/OrnamentalDivider';
import { ArrowLeft, BookOpen, Scale, AlertCircle, FileCheck, CheckCircle2 } from 'lucide-react';

export default function TermsPage({ onNavigate }) {
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
    document.title = 'Terms & Conditions — Rajasthan Heritage Dashboard';
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
            <Scale className="w-3.5 h-3.5 text-gold" />
            <span>Platform Terms & Cultural Stewardship</span>
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-maroon mb-4">
            Terms & Conditions
          </h1>

          <p className="text-sm sm:text-base text-ink-muted max-w-xl mx-auto font-editorial text-lg italic">
            Governance guidelines, intellectual property stewardship, and terms of use for the Rajasthan Cultural Heritage Dashboard.
          </p>

          <OrnamentalDivider motif="✦" className="mt-6" />
        </div>

        {/* Terms Content Container */}
        <div className="parchment-card p-6 sm:p-10 space-y-8 text-ink">
          
          {/* Section 1 */}
          <section className="space-y-3">
            <div className="flex items-center gap-2 text-maroon">
              <FileCheck className="w-5 h-5 text-gold shrink-0" />
              <h2 className="text-xl sm:text-2xl font-bold font-body">1. Agreement to Terms</h2>
            </div>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              By accessing and interacting with the Rajasthan Cultural Heritage Dashboard ("the Platform"), you acknowledge and agree to comply with these Terms and Conditions. If you do not agree with any part of these terms, please discontinue use of the Platform immediately.
            </p>
          </section>

          {/* Section 2 */}
          <section className="space-y-3">
            <div className="flex items-center gap-2 text-maroon">
              <BookOpen className="w-5 h-5 text-gold shrink-0" />
              <h2 className="text-xl sm:text-2xl font-bold font-body">2. Cultural Stewardship & Intellectual Property</h2>
            </div>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              The Rajasthan Cultural Heritage Dashboard honors centuries of traditional Indian craftsmanship. The historical motifs, architectural illustrations, folk song references, and photographic reproductions featured on this platform belong to their respective cultural lineages, traditional artisan communities, and rights holders.
            </p>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              Frontend code, responsive layout systems, and interactive motion designs authored for this repository are protected under applicable software and copyright conventions. Content is provided solely for personal exploration, educational appreciation, and non-commercial study.
            </p>
          </section>

          {/* Section 3 */}
          <section className="space-y-3">
            <div className="flex items-center gap-2 text-maroon">
              <AlertCircle className="w-5 h-5 text-gold shrink-0" />
              <h2 className="text-xl sm:text-2xl font-bold font-body">3. Permitted & Prohibited Use</h2>
            </div>
            <ul className="list-disc pl-6 space-y-2 text-sm sm:text-base text-ink-muted">
              <li><strong>Permitted:</strong> Exploring cultural visual stories, inspecting the 28 archival artifacts in the interactive lightbox, and sharing educational links to the platform.</li>
              <li><strong>Prohibited:</strong> Scraping or re-hosting cultural artwork for commercial merchandise without rights holder authorization, attempting denial-of-service or automated stress-testing against the repository, and misrepresenting affiliations with official state tourism departments.</li>
            </ul>
          </section>

          {/* Section 4 */}
          <section className="space-y-3">
            <div className="flex items-center gap-2 text-maroon">
              <CheckCircle2 className="w-5 h-5 text-gold shrink-0" />
              <h2 className="text-xl sm:text-2xl font-bold font-body">4. Disclaimer of Commercial Functionality</h2>
            </div>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              This website is an interactive digital exhibition. It does not provide hotel bookings, travel agency tickets, commercial tours, or physical merchandise shipments. Any references to regional destinations, festivals, or monuments are curated strictly for cultural appreciation.
            </p>
          </section>

          {/* Section 5 */}
          <section className="space-y-3">
            <div className="flex items-center gap-2 text-maroon">
              <Scale className="w-5 h-5 text-gold shrink-0" />
              <h2 className="text-xl sm:text-2xl font-bold font-body">5. Limitation of Liability</h2>
            </div>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              The platform is provided on an "as-is" and "as-available" basis without warranties of any kind. Under no circumstances shall the creators, contributors, or repository maintainers be liable for any indirect, incidental, or consequential damages resulting from your access to or inability to use the Platform.
            </p>
          </section>

          {/* Section 6 */}
          <section className="space-y-3">
            <h2 className="text-xl sm:text-2xl font-bold font-body text-maroon">6. Governing Law & Amendments</h2>
            <p className="text-sm sm:text-base text-ink-muted leading-relaxed">
              These terms shall be governed by and construed in accordance with the laws of India. We reserve the right to amend these terms periodically to reflect ongoing development.
            </p>
            <div className="p-4 rounded-lg bg-gold/10 border border-gold/30 text-xs sm:text-sm text-maroon">
              <strong>Effective Date:</strong> November 2026 • PinkOps Cultural Platform.
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
