import React from 'react';
import ScrollReveal from './ScrollReveal';
import OrnamentalDivider from './OrnamentalDivider';
import { Sparkles, Eye, ChevronRight } from 'lucide-react';

export default function HorizontalShowcase({ onSelectImage }) {
  const showcaseItems = [
    {
      id: 'truck-art-rickshaw',
      num: '01',
      title: 'Horn OK Please Auto',
      tag: 'Street Art',
      desc: 'Vibrant truck art patterns, lotus petals, and iconic typography decorating an urban auto-rickshaw.',
      src: '/images/289074869855567219.jpeg',
      alt: 'Painted Indian auto-rickshaw with folk art and Horn OK Please'
    },
    {
      id: 'peacock-cycle-rickshaw',
      num: '02',
      title: 'The Peacock Rickshaw',
      tag: 'Folk Carriage',
      desc: 'Hand-painted dancing peacocks and marigold wheel spokes on a traditional passenger cycle.',
      src: '/images/872361390338004286.jpeg',
      alt: 'Traditional cycle rickshaw lavishly painted with colorful peacocks and floral patterns'
    },
    {
      id: 'desert-camel-cart',
      num: '03',
      title: 'Royal Camel Wagon',
      tag: 'Desert Transit',
      desc: 'Sheesham wood canopy draped in mirrored curtains, bells, and embroidered cushions.',
      src: '/images/872361390338004288.jpeg',
      alt: 'Traditional decorated Rajasthani camel cart with ornate wooden canopy'
    },
    {
      id: 'royal-tutari-horn',
      num: '04',
      title: 'Sovereign Kahal Horn',
      tag: 'Ceremonial Music',
      desc: 'An antique crescent trumpet inscribed with micro-scenes of palaces, forts, and musicians.',
      src: '/images/tailand.jpeg',
      alt: 'Ornate crescent shaped royal Indian trumpet horn'
    },
    {
      id: 'khamma-ghani-jaisalmer',
      num: '05',
      title: 'Khamma Ghani Mural',
      tag: 'Sandstone Graffiti',
      desc: 'Jaisalmer alley street portrait of a modern Rajput in dark shades and royal pagri.',
      src: '/images/%F0%9F%93%8D%20Jaisalmer,%20Rajasthan.jpeg',
      alt: 'Khamma Ghani street art mural in Jaisalmer'
    },
    {
      id: 'dekho-magar-pyar-se',
      num: '06',
      title: 'Dekho Magar Pyar Se',
      tag: 'Folk Signboard',
      desc: 'Pop-folk Indian sign lettering in hot pink inside a scalloped sun-yellow arch.',
      src: '/images/Wall%20Art%20-%20Masoom%20Ansari.jpeg',
      alt: 'Dekho Magar Pyar Se folk art typography'
    }
  ];

  return (
    <section className="section-py bg-parchment-light border-t border-gold/20 overflow-hidden relative">
      <div className="site-container">
        
        {/* Header with Horizontal Drag Hint */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8">
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-gold block mb-2">
              Discovery Rail
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-maroon">
              Folk Wheels & Street Vignettes
            </h2>
            <p className="text-sm sm:text-base text-ink-muted mt-2">
              From village camel carts to painted auto-rickshaws and Golden Fort murals.
            </p>
          </div>
          <div className="hidden sm:flex items-center gap-2 text-xs font-bold text-maroon mt-4 md:mt-0">
            <span>Scroll Horizontally to Discover</span>
            <ChevronRight className="w-4 h-4 text-gold" />
          </div>
        </div>

        {/* Horizontal Scroll Showcase Rail */}
        <div className="horizontal-scroll-container">
          {showcaseItems.map((item) => (
            <div
              key={item.id}
              className="horizontal-card-item cursor-pointer"
              onClick={() => onSelectImage(item.id)}
            >
              <div className="jharokha-frame h-full flex flex-col justify-between p-4 bg-white/90 hover:shadow-parchment-hover transition-all">
                <div className="flex items-center justify-between text-xs pb-2 border-b border-maroon/10 mb-3">
                  <span className="font-heading-royal font-bold text-gold text-base">{item.num}</span>
                  <span className="px-2 py-0.5 rounded-full bg-maroon/5 text-maroon font-bold text-[10px]">
                    {item.tag}
                  </span>
                </div>

                <div className="relative h-56 bg-parchment rounded-lg p-2 flex items-center justify-center overflow-hidden mb-3">
                  <img
                    src={item.src}
                    alt={item.alt}
                    className="max-h-full max-w-full object-contain mx-auto transition-transform duration-500 hover:scale-105"
                    loading="lazy"
                  />
                </div>

                <div>
                  <h4 className="font-bold text-maroon text-base mb-1">
                    {item.title}
                  </h4>
                  <p className="text-xs text-ink-muted line-clamp-2 leading-relaxed mb-3">
                    {item.desc}
                  </p>
                  <div className="flex items-center justify-between text-[11px] font-bold text-maroon/70 pt-2 border-t border-maroon/10">
                    <span>Inspect</span>
                    <Eye className="w-3.5 h-3.5 text-gold" />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
