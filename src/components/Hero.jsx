import React from 'react';
import { ArrowDown, Sparkles, BookOpen, Image as ImageIcon } from 'lucide-react';
import OrnamentalDivider from './OrnamentalDivider';

export default function Hero({ onExploreStory, onExploreGallery }) {
  return (
    <section id="hero" className="relative min-h-[92vh] flex flex-col justify-between pt-8 pb-12 overflow-hidden bg-parchment-texture">
      {/* Decorative Background Watermark */}
      <div 
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] rounded-full pointer-events-none opacity-[0.04]"
        style={{
          background: 'radial-gradient(circle, var(--color-gold) 0%, var(--color-maroon) 70%, transparent 100%)',
          filter: 'blur(40px)',
          zIndex: 'var(--z-base)'
        }}
        aria-hidden="true"
      />

      <div className="site-container relative" style={{ zIndex: 'var(--z-content)' }}>
        {/* Eyebrow & Devanagari Greeting */}
        <div className="text-center hero-anim-1">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-parchment border border-gold/30 shadow-sm mb-4">
            <Sparkles className="w-3.5 h-3.5 text-gold" />
            <span className="font-devanagari text-maroon font-bold text-sm sm:text-base">पधारो म्हारे देश</span>
            <span className="text-xs font-semibold tracking-widest text-ink-muted uppercase">• Padharo Mhare Desh</span>
          </div>
        </div>

        {/* Majestic Display Headline */}
        <div className="text-center max-w-4xl mx-auto hero-anim-2">
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-maroon tracking-tight leading-[1.1] mb-6">
            The Living Soul <br />
            <span className="font-editorial italic font-normal text-saffron">of Rajasthan</span>
          </h1>
        </div>

        {/* Editorial Subtitle */}
        <div className="text-center max-w-2xl mx-auto hero-anim-3 mb-8">
          <p className="text-base sm:text-lg md:text-xl text-ink-muted font-body leading-relaxed">
            Where centuries of Rajputana grandeur meet timeless Thar desert folk art, kaleidoscopic block-prints, and the resonant strings of the ancient Ravanahatha.
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 hero-anim-4 mb-12">
          <button
            onClick={onExploreStory}
            className="btn-royal-primary"
            aria-label="Begin Cultural Story Journey"
          >
            <BookOpen className="w-4 h-4 text-gold" />
            <span>Begin the Journey</span>
          </button>
          <button
            onClick={onExploreGallery}
            className="btn-royal-secondary"
            aria-label="Explore Visual Heritage Gallery"
          >
            <ImageIcon className="w-4 h-4 text-maroon" />
            <span>Explore 28 Artifacts</span>
          </button>
        </div>

        {/* Layered Visual Composition */}
        <div className="relative max-w-5xl mx-auto hero-anim-5 mt-4">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
            
            {/* Left Foreground: Thar Desert Camel */}
            <div className="hidden md:block md:col-span-3 text-center animate-float">
              <div className="p-3 bg-white/70 backdrop-blur rounded-2xl border border-gold/30 shadow-parchment hover:shadow-parchment-hover transition-all">
                <img
                  src="/images/116812184079590264.jpeg"
                  alt="Thar desert camel decorated with traditional mirror-work and pom-poms"
                  className="w-full h-64 object-contain mx-auto"
                  loading="eager"
                />
                <div className="pt-2 text-center">
                  <span className="text-xs font-bold text-maroon tracking-wider uppercase block">Thar Caravan</span>
                  <span className="text-[11px] text-ink-subtle">Gorbandh Mirror-Work</span>
                </div>
              </div>
            </div>

            {/* Centerpiece: Symmetrical Peacock Jharokha Arch */}
            <div className="col-span-12 md:col-span-6 relative">
              <div className="relative mx-auto max-w-[380px] sm:max-w-[420px] rounded-3xl overflow-hidden p-2 bg-gradient-to-b from-gold/20 via-maroon/10 to-transparent border-2 border-gold shadow-2xl">
                <div className="relative bg-[#FFFBF5] rounded-2xl p-4 overflow-hidden">
                  <img
                    src="/images/1120763057291282691.jpeg"
                    alt="Jaipur pink arch with symmetrical royal peacocks"
                    className="w-full h-80 sm:h-96 object-contain mx-auto rounded-xl"
                    loading="eager"
                  />
                  
                  {/* Floating Namaste Host Badge Overlay */}
                  <div className="absolute -bottom-2 -right-2 w-28 h-28 sm:w-32 sm:h-32 bg-white/95 rounded-full p-2 border-2 border-gold shadow-lg flex flex-col items-center justify-center animate-float-delayed">
                    <img
                      src="/images/Indian%20Man%20With%20Turban%20Rajasthani%20Men%20Welcome%20Namaste%20Greetings,%20Icon,%20Illustration,%20Vector%20PNG%20Transparent%20Image%20and%20Clipart%20for%20Free%20Download.jpeg"
                      alt="Traditional Rajasthani Namaste welcome"
                      className="w-16 h-16 sm:w-20 sm:h-20 object-contain rounded-full"
                    />
                    <span className="text-[10px] font-bold text-maroon mt-0.5 font-devanagari">खम्मा घणी</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Foreground: Caparisoned Royal Elephant */}
            <div className="hidden md:block md:col-span-3 text-center animate-float-delayed">
              <div className="p-3 bg-white/70 backdrop-blur rounded-2xl border border-gold/30 shadow-parchment hover:shadow-parchment-hover transition-all">
                <img
                  src="/images/1112389176722280670.jpeg"
                  alt="Decorated royal blue elephant with ceremonial chatri umbrella"
                  className="w-full h-64 object-contain mx-auto"
                  loading="eager"
                />
                <div className="pt-2 text-center">
                  <span className="text-xs font-bold text-maroon tracking-wider uppercase block">Royal Gajraj</span>
                  <span className="text-[11px] text-ink-subtle">Ceremonial Chatri</span>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>

      {/* Animated Scroll Indicator */}
      <div className="text-center pt-8">
        <button
          onClick={onExploreStory}
          className="inline-flex flex-col items-center gap-1 text-maroon/70 hover:text-maroon transition-colors bg-transparent border-0 cursor-pointer"
          aria-label="Scroll down to explore story"
        >
          <span className="text-[11px] font-semibold tracking-widest uppercase">Scroll to Discover</span>
          <div className="animate-scroll-indicator p-1 rounded-full border border-maroon/30">
            <ArrowDown className="w-3.5 h-3.5 text-maroon" />
          </div>
        </button>
      </div>
    </section>
  );
}
