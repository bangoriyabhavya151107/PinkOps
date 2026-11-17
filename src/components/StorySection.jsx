import React from 'react';
import ScrollReveal from './ScrollReveal';
import OrnamentalDivider from './OrnamentalDivider';
import { Sparkles, Music, Compass, Shield } from 'lucide-react';

export default function StorySection({ onSelectImage }) {
  return (
    <section id="story" className="section-py bg-parchment relative">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <ScrollReveal animation="fade-up">
            <span className="text-xs font-bold uppercase tracking-widest text-gold block mb-2">
              Visual Chronicle
            </span>
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-maroon mb-4">
              Stories Carved in Sandstone & Silk
            </h2>
            <p className="text-base sm:text-lg text-ink-muted">
              Every motif, archway, and instrument carries an unbroken lineage of desert wisdom, hospitality, and royal artistry.
            </p>
            <OrnamentalDivider motif="🦚" className="mt-4" />
          </ScrollReveal>
        </div>

        {/* Chapter 1: Left Image / Right Text */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center mb-24">
          <div className="lg:col-span-6">
            <ScrollReveal animation="fade-right">
              <div 
                className="jharokha-frame p-4 cursor-pointer group"
                onClick={() => onSelectImage('desert-camel-cart')}
              >
                <div className="corner-flourish corner-tl" />
                <div className="corner-flourish corner-tr" />
                <div className="corner-flourish corner-bl" />
                <div className="corner-flourish corner-br" />
                <div className="relative overflow-hidden rounded-xl bg-white/50 p-2">
                  <img
                    src="/images/872361390338004288.jpeg"
                    alt="Traditional decorated Rajasthani camel cart with ornate wooden canopy"
                    className="w-full h-[400px] sm:h-[460px] object-contain mx-auto transition-transform duration-700 group-hover:scale-105"
                    loading="lazy"
                  />
                  <div className="absolute bottom-4 left-4 right-4 bg-white/90 backdrop-blur p-3 rounded-lg border border-gold/40 text-center">
                    <span className="text-xs font-bold text-maroon tracking-wider uppercase block">
                      The Royal Camel Wagon
                    </span>
                    <span className="text-[11px] text-ink-subtle">
                      Handcrafted Canopy • Mirrored Gorbandh
                    </span>
                  </div>
                </div>
              </div>
            </ScrollReveal>
          </div>

          <div className="lg:col-span-6">
            <ScrollReveal animation="fade-left" delay={150}>
              <div className="pl-0 lg:pl-6">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-saffron/10 text-saffron text-xs font-bold uppercase tracking-wider mb-4">
                  <Compass className="w-3.5 h-3.5" />
                  <span>Chapter I • The Thar Voyage</span>
                </div>
                <h3 className="text-2xl sm:text-3xl md:text-4xl font-bold text-maroon mb-6 leading-tight">
                  The Nomadic Rhythm of the Golden Sands
                </h3>
                <p className="text-base text-ink-muted leading-relaxed mb-4">
                  Across the shifting dunes of Jaisalmer, Barmer, and Bikaner, travel has always been an art form. The desert caravan is not merely transit — it is a moving gallery of Rajasthani craftsmanship.
                </p>
                <p className="text-base text-ink-muted leading-relaxed mb-6">
                  Carved from native sheesham and rohida wood, camel carts are adorned with brass bells whose rhythmic chime echoes across kilometers of silent desert. Saddles are hand-embroidered with mirror-work to deflect the desert sun and catch moonbeams at night.
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="category-pill">Desert Caravans</span>
                  <span className="category-pill">Mirror Needlework</span>
                  <span className="category-pill">Nomadic Lore</span>
                </div>
              </div>
            </ScrollReveal>
          </div>
        </div>

        {/* Chapter 2: Right Image / Left Text */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center mb-24">
          <div className="lg:col-span-6 order-2 lg:order-1">
            <ScrollReveal animation="fade-right" delay={150}>
              <div className="pr-0 lg:pr-6">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-peacock/10 text-peacock text-xs font-bold uppercase tracking-wider mb-4">
                  <Music className="w-3.5 h-3.5" />
                  <span>Chapter II • Soundscapes of Rajputana</span>
                </div>
                <h3 className="text-2xl sm:text-3xl md:text-4xl font-bold text-maroon mb-6 leading-tight">
                  The Ravanahatha & The Living Bardic Lineages
                </h3>
                <p className="text-base text-ink-muted leading-relaxed mb-4">
                  Long before written history, the Manganiyar, Langa, and Bhopa bards carried the memory of Rajasthan in sacred verse. With the horsehair bow of the ancient Ravanahatha, master musicians conjure the soul of the Thar.
                </p>
                <p className="text-base text-ink-muted leading-relaxed mb-6">
                  From celebratory songs welcoming the monsoon clouds (Maand) to epic ballads of warrior devotion (Pabu Ji Ki Phad), these haunting melodies transcend generations, fusing antique acoustic power with vibrant desert celebration.
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="category-pill">Ravanahatha Bow</span>
                  <span className="category-pill">Bhopa Troubadours</span>
                  <span className="category-pill">Desert Ragas</span>
                </div>
              </div>
            </ScrollReveal>
          </div>

          <div className="lg:col-span-6 order-1 lg:order-2">
            <ScrollReveal animation="fade-left">
              <div 
                className="jharokha-frame p-4 cursor-pointer group"
                onClick={() => onSelectImage('folk-musician-sarangi')}
              >
                <div className="corner-flourish corner-tl" />
                <div className="corner-flourish corner-tr" />
                <div className="corner-flourish corner-bl" />
                <div className="corner-flourish corner-br" />
                <div className="relative overflow-hidden rounded-xl bg-white/50 p-2">
                  <img
                    src="/images/Incredible%20Rajasthan.jpeg"
                    alt="Master Rajasthani folk musician playing Ravanahatha"
                    className="w-full h-[400px] sm:h-[460px] object-contain mx-auto transition-transform duration-700 group-hover:scale-105"
                    loading="lazy"
                  />
                  <div className="absolute bottom-4 left-4 right-4 bg-white/90 backdrop-blur p-3 rounded-lg border border-gold/40 text-center">
                    <span className="text-xs font-bold text-maroon tracking-wider uppercase block">
                      The Master Bard
                    </span>
                    <span className="text-[11px] text-ink-subtle">
                      Leheriya Turban • Ancestral Strings
                    </span>
                  </div>
                </div>
              </div>
            </ScrollReveal>
          </div>
        </div>

        {/* Chapter 3: Full Width Visual Composition */}
        <ScrollReveal animation="scale-in">
          <div className="jharokha-frame p-6 sm:p-10 bg-gradient-to-br from-[#FFFDF9] via-[#FAF4E8] to-[#FFFBF5]">
            <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
              <div className="md:col-span-5">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rani-pink/10 text-rani-pink text-xs font-bold uppercase tracking-wider mb-3">
                  <Shield className="w-3.5 h-3.5" />
                  <span>Chapter III • Palaces & Peacocks</span>
                </div>
                <h3 className="text-2xl sm:text-3xl font-bold text-maroon mb-4">
                  Hawa Mahal & The Architecture of Wind
                </h3>
                <p className="text-sm sm:text-base text-ink-muted leading-relaxed mb-4">
                  Constructed in 1799 from pink and red sandstone, Jaipur's Hawa Mahal stands as an engineering feat: 953 honeycombed jharokhas that channel natural wind tunnels, keeping royal chambers cool through scorching desert summers.
                </p>
                <div className="p-3 bg-parchment rounded-xl border border-gold/30">
                  <p className="text-xs font-devanagari text-maroon font-semibold">
                    "महल की खिड़कियों से हवाएं गाती हैं, राजपूत आन की कहानियां।"
                  </p>
                  <p className="text-[11px] text-ink-subtle mt-1">
                    Through palace lattice screens, the breezes sing stories of Rajput honor.
                  </p>
                </div>
              </div>

              <div className="md:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div 
                  className="rounded-xl overflow-hidden border border-gold/30 p-2 bg-white/70 hover:shadow-lg transition-all cursor-pointer"
                  onClick={() => onSelectImage('hawa-mahal-palace')}
                >
                  <img
                    src="/images/784541197593507390.jpeg"
                    alt="Hawa Mahal Palace of Winds architectural illustration"
                    className="w-full h-56 object-contain mx-auto"
                    loading="lazy"
                  />
                  <p className="text-xs font-bold text-center text-maroon mt-2">Hawa Mahal • Jaipur</p>
                </div>
                <div 
                  className="rounded-xl overflow-hidden border border-gold/30 p-2 bg-white/70 hover:shadow-lg transition-all cursor-pointer"
                  onClick={() => onSelectImage('music-arch-frame')}
                >
                  <img
                    src="/images/382594930870467842.jpeg"
                    alt="Sangeet Arch Gateway with traditional musical instruments"
                    className="w-full h-56 object-contain mx-auto"
                    loading="lazy"
                  />
                  <p className="text-xs font-bold text-center text-maroon mt-2">Sangeet Arch • Heritage</p>
                </div>
              </div>
            </div>
          </div>
        </ScrollReveal>

      </div>
    </section>
  );
}
