import React, { useState } from 'react';
import ScrollReveal from './ScrollReveal';
import OrnamentalDivider from './OrnamentalDivider';
import { IMAGES_DATA, CATEGORIES } from '../assets/imagesData';
import { Eye, Tag, Sparkles } from 'lucide-react';

export default function GallerySection({ onSelectImage }) {
  const [selectedFilter, setSelectedFilter] = useState('all');

  const filteredItems = IMAGES_DATA.filter(item => {
    if (selectedFilter === 'all') return true;
    return item.category === selectedFilter;
  });

  return (
    <section id="gallery" className="section-py bg-parchment relative">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-14">
          <ScrollReveal animation="fade-up">
            <span className="text-xs font-bold uppercase tracking-widest text-gold block mb-2">
              Visual Archive
            </span>
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-maroon mb-4">
              The 28 Cultural Masterpieces
            </h2>
            <p className="text-base sm:text-lg text-ink-muted">
              Complete photographic and illustrative registry of royal Rajputana architecture, Thar folklore, textile embroidery, and street art.
            </p>
            <OrnamentalDivider motif="✦" className="mt-4" />
          </ScrollReveal>
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center justify-center gap-2 mb-10">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedFilter(cat.id)}
              className={`category-pill ${selectedFilter === cat.id ? 'active' : ''}`}
              aria-label={`Show ${cat.label}`}
            >
              <span>{cat.label}</span>
              {selectedFilter === cat.id && (
                <span className="ml-1 text-[11px] opacity-80">({filteredItems.length})</span>
              )}
            </button>
          ))}
        </div>

        {/* Gallery Grid */}
        <div className="gallery-grid">
          {filteredItems.map((item, idx) => (
            <ScrollReveal key={item.id} animation="fade-up" delay={(idx % 6) * 50}>
              <div
                className="jharokha-frame p-3 bg-white/90 group cursor-pointer h-full flex flex-col justify-between"
                onClick={() => onSelectImage(item.id)}
              >
                <div className="relative overflow-hidden rounded-lg bg-parchment p-3 h-72 flex items-center justify-center">
                  <img
                    src={item.src}
                    alt={item.alt}
                    className="max-h-full max-w-full object-contain mx-auto transition-transform duration-500 group-hover:scale-105"
                    loading="lazy"
                  />

                  {/* Hover Overlay */}
                  <div className="absolute inset-0 bg-maroon-dark/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center p-4 text-center text-white backdrop-blur-xs">
                    <span className="p-2 rounded-full bg-gold/90 text-maroon mb-2 transform translate-y-2 group-hover:translate-y-0 transition-transform">
                      <Eye className="w-5 h-5" />
                    </span>
                    <span className="text-xs font-bold uppercase tracking-wider text-gold block">
                      Inspect Details
                    </span>
                    <span className="text-xs text-white/90 font-medium mt-1">
                      {item.title}
                    </span>
                  </div>

                  {/* Category Chip */}
                  <div className="absolute top-2 left-2 px-2 py-0.5 rounded bg-white/90 backdrop-blur text-[10px] font-bold text-maroon border border-gold/30">
                    {item.categoryLabel}
                  </div>
                </div>

                <div className="pt-3 px-1 flex items-center justify-between">
                  <div className="truncate pr-2">
                    <h4 className="text-sm font-bold text-maroon truncate group-hover:text-rani-pink transition-colors">
                      {item.title}
                    </h4>
                    <p className="text-[11px] text-ink-subtle truncate">
                      {item.subtitle}
                    </p>
                  </div>
                  <span className="text-xs font-bold text-gold shrink-0">↗</span>
                </div>
              </div>
            </ScrollReveal>
          ))}
        </div>

      </div>
    </section>
  );
}
