import React, { useState } from 'react';
import ScrollReveal from './ScrollReveal';
import OrnamentalDivider from './OrnamentalDivider';
import { CULTURAL_METRICS, CATEGORIES, IMAGES_DATA } from '../assets/imagesData';
import { Eye, Sparkles, MapPin, Tag } from 'lucide-react';

export default function DashboardArea({ onSelectImage }) {
  const [selectedCategory, setSelectedCategory] = useState('all');

  const filteredCards = IMAGES_DATA.filter(item => {
    if (selectedCategory === 'all') return item.featured;
    return item.category === selectedCategory;
  });

  return (
    <section id="dashboard" className="section-py bg-parchment relative">
      <div className="site-container">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <ScrollReveal animation="fade-up">
            <span className="text-xs font-bold uppercase tracking-widest text-gold block mb-2">
              Cultural Intelligence Dashboard
            </span>
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-maroon mb-4">
              Living Heritage & Artisan Archive
            </h2>
            <p className="text-base sm:text-lg text-ink-muted">
              Explore authentic archival records, regional craft repositories, and living cultural indicators across the princely states.
            </p>
            <OrnamentalDivider motif="🦚" className="mt-4" />
          </ScrollReveal>
        </div>

        {/* Heritage Metrics Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {CULTURAL_METRICS.map((metric, idx) => (
            <ScrollReveal key={idx} animation="scale-in" delay={idx * 80}>
              <div className="parchment-card text-center h-full flex flex-col justify-between">
                <div className="corner-flourish corner-tl" />
                <div className="corner-flourish corner-tr" />
                <div className="corner-flourish corner-bl" />
                <div className="corner-flourish corner-br" />
                
                <div>
                  <span className="font-heading-royal text-3xl sm:text-4xl font-extrabold text-maroon block mb-2">
                    {metric.number}
                  </span>
                  <h4 className="text-sm sm:text-base font-bold text-ink mb-2">
                    {metric.label}
                  </h4>
                </div>
                <p className="text-xs text-ink-subtle mt-2 pt-2 border-t border-maroon/10">
                  {metric.detail}
                </p>
              </div>
            </ScrollReveal>
          ))}
        </div>

        {/* Category Filter Pills */}
        <div className="flex flex-wrap items-center justify-center gap-2 mb-12">
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`category-pill ${selectedCategory === cat.id ? 'active' : ''}`}
              aria-label={`Filter by ${cat.label}`}
            >
              <Tag className="w-3 h-3" />
              <span>{cat.label}</span>
            </button>
          ))}
        </div>

        {/* Filtered Interactive Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredCards.map((item, idx) => (
            <ScrollReveal key={item.id} animation="fade-up" delay={idx * 60}>
              <div 
                className="jharokha-frame h-full flex flex-col overflow-hidden group cursor-pointer"
                onClick={() => onSelectImage(item.id)}
              >
                {/* Image Container with contain and subtle zoom */}
                <div className="relative h-64 bg-[#FFFDF9] p-4 flex items-center justify-center border-b border-maroon/10 overflow-hidden">
                  <img
                    src={item.src}
                    alt={item.alt}
                    className="max-h-full max-w-full object-contain mx-auto transition-transform duration-500 group-hover:scale-105"
                    loading="lazy"
                  />
                  <div className="absolute top-3 right-3 px-2.5 py-1 rounded-full bg-white/90 backdrop-blur text-[11px] font-bold text-maroon border border-gold/40 shadow-sm">
                    {item.categoryLabel}
                  </div>
                </div>

                {/* Card Content */}
                <div className="p-6 flex-1 flex flex-col justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-maroon mb-1 group-hover:text-rani-pink transition-colors">
                      {item.title}
                    </h3>
                    <p className="text-xs font-semibold text-gold mb-3">
                      {item.subtitle}
                    </p>
                    <p className="text-xs sm:text-sm text-ink-muted leading-relaxed line-clamp-3 mb-4">
                      {item.description}
                    </p>
                  </div>

                  <div className="pt-3 border-t border-maroon/10 flex items-center justify-between text-xs">
                    <span className="text-ink-subtle">Authentic Archival Asset</span>
                    <span className="inline-flex items-center gap-1 font-bold text-maroon group-hover:text-gold transition-colors">
                      <Eye className="w-3.5 h-3.5" />
                      <span>Inspect</span>
                    </span>
                  </div>
                </div>
              </div>
            </ScrollReveal>
          ))}
        </div>

      </div>
    </section>
  );
}
