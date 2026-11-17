import React, { useState } from 'react';
import ScrollReveal from './ScrollReveal';
import OrnamentalDivider from './OrnamentalDivider';
import { Palette, Sparkles, Feather } from 'lucide-react';

export default function StickyStorySection({ onSelectImage }) {
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    {
      id: 'step-1',
      badge: 'Craft Stage 01',
      icon: Palette,
      title: 'Rangrez & Bandhani: The Alchemy of Desert Dyes',
      subtitle: 'Tie-and-Dye Mastery of Marwar & Mewar',
      description: 'In the arid desert where water is precious, color is sacred joy. The Rangrez artisans pinch fine muslin with copper fingernail thimbles into thousands of microscopic knots, submerging cloth into pomegranate rind, saffron madder, and indigo vats to create ripples of Bandhani and wind-blown Leheriya.',
      paletteHighlight: 'Rani Pink • Scarlet • Marigold • Peacock Green',
      image: {
        src: '/images/Royal%20Indian%20Color%20palette.jpeg',
        alt: 'Royal Indian Color Palette Swatch',
        caption: 'The Master Royal Color Swatch',
        imageId: 'royal-color-palette'
      }
    },
    {
      id: 'step-2',
      badge: 'Craft Stage 02',
      icon: Sparkles,
      title: 'Zardozi & Gold Needlecraft: Courtly Tapestry',
      subtitle: 'Silk & Metallic Filigree on Royal Maroon Velvet',
      description: 'Zardozi — literally gold embroidery (Zar meaning gold, Dozi meaning needlework) — elevated Rajputana royal garments into portable palaces. Master needlecrafters embroider ceremonial caparisons with courtly peacocks, palatial arches, and gajraj elephants using silver bullion wire and fine silk threads.',
      paletteHighlight: 'Royal Maroon • Antique Gold • Raw Silk',
      image: {
        src: '/images/1132233162587708007.jpeg',
        alt: 'Royal Maroon Zardozi Embroidery Tapestry',
        caption: 'Royal Zardozi Court Tapestry',
        imageId: 'zardozi-tapestry'
      }
    },
    {
      id: 'step-3',
      badge: 'Craft Stage 03',
      icon: Feather,
      title: 'The Living Guilds: Parasols, Mirrors & Folk Murals',
      subtitle: 'Celebratory Desert Crafts of Rajasthan',
      description: 'No desert mela (festival) is complete without the kaleidoscope of handcrafted chatris (umbrellas) adorned with sun-reflecting circular mirrors and silk fringe tassels. Paired with wall murals and hand-painted vehicles, each piece carries the artisan’s blessing for safe voyages.',
      paletteHighlight: 'Sunburst Ochre • Terracotta • Mirror Glaze',
      image: {
        src: '/images/This%20is%20an%20online%20Platform%20created%20to%20spread%20the%E2%80%A6.jpeg',
        alt: 'Handcrafted embroidered Rajasthani umbrella with mirrors and tassels',
        caption: 'Artisan Embroidered Festival Chatri',
        imageId: 'embroidered-umbrella'
      }
    }
  ];

  const currentStepData = steps[activeStep];

  return (
    <section id="craft" className="section-py bg-parchment-light border-y border-gold/20 relative">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <ScrollReveal animation="fade-up">
            <span className="text-xs font-bold uppercase tracking-widest text-gold block mb-2">
              Artisan Heritage
            </span>
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-maroon mb-4">
              Three Acts of Rajasthani Craftsmanship
            </h2>
            <p className="text-base sm:text-lg text-ink-muted">
              Interactive narrative exploration through ancient dyeing, metallic needlecraft, and celebratory festival arts.
            </p>
            <OrnamentalDivider motif="✦" className="mt-4" />
          </ScrollReveal>
        </div>

        {/* Step Selector Buttons for Direct Accessibility */}
        <div className="flex flex-wrap items-center justify-center gap-3 mb-12">
          {steps.map((s, idx) => (
            <button
              key={s.id}
              onClick={() => setActiveStep(idx)}
              className={`category-pill ${activeStep === idx ? 'active' : ''}`}
              aria-label={`View ${s.title}`}
            >
              <span>{`0${idx + 1}. ${s.badge.replace('Craft Stage ', '')}`}</span>
            </button>
          ))}
        </div>

        {/* Sticky Split View */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          
          {/* Left: Sticky Image Canvas */}
          <div className="lg:col-span-6 lg:sticky lg:top-28">
            <div 
              className="jharokha-frame p-6 bg-white/80 cursor-pointer group"
              onClick={() => onSelectImage(currentStepData.image.imageId)}
            >
              <div className="corner-flourish corner-tl" />
              <div className="corner-flourish corner-tr" />
              <div className="corner-flourish corner-bl" />
              <div className="corner-flourish corner-br" />
              
              <div className="relative overflow-hidden rounded-xl bg-parchment p-3 min-h-[420px] sm:min-h-[480px] flex items-center justify-center">
                <img
                  key={currentStepData.image.src}
                  src={currentStepData.image.src}
                  alt={currentStepData.image.alt}
                  className="max-h-[440px] w-auto max-w-full object-contain mx-auto transition-transform duration-500 group-hover:scale-105"
                  loading="lazy"
                />
              </div>

              <div className="mt-4 flex items-center justify-between text-xs text-ink-muted border-t border-maroon/10 pt-3">
                <span className="font-semibold text-maroon">{currentStepData.image.caption}</span>
                <span className="text-gold font-bold">Click to Inspect in Lightbox ↗</span>
              </div>
            </div>
          </div>

          {/* Right: Step Content Panel */}
          <div className="lg:col-span-6 flex flex-col gap-8">
            {steps.map((step, idx) => {
              const isActive = activeStep === idx;
              const IconComp = step.icon;

              return (
                <div
                  key={step.id}
                  onClick={() => setActiveStep(idx)}
                  className={`parchment-card cursor-pointer transition-all ${
                    isActive
                      ? 'border-gold shadow-parchment-hover bg-[#FFFDF9]'
                      : 'opacity-70 hover:opacity-100'
                  }`}
                >
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-2 rounded-lg bg-maroon/5 text-maroon">
                      <IconComp className="w-5 h-5 text-gold" />
                    </div>
                    <div>
                      <span className="text-xs font-bold uppercase tracking-wider text-gold block">
                        {step.badge}
                      </span>
                      <span className="text-sm font-semibold text-ink-muted">
                        {step.subtitle}
                      </span>
                    </div>
                  </div>

                  <h3 className="text-xl sm:text-2xl font-bold text-maroon mb-3">
                    {step.title}
                  </h3>

                  <p className="text-sm sm:text-base text-ink-muted leading-relaxed mb-4">
                    {step.description}
                  </p>

                  <div className="flex items-center justify-between pt-3 border-t border-maroon/10 text-xs">
                    <span className="font-semibold text-ink-muted">Palette Accent:</span>
                    <span className="font-bold text-maroon">{step.paletteHighlight}</span>
                  </div>
                </div>
              );
            })}
          </div>

        </div>

      </div>
    </section>
  );
}
