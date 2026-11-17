import React, { useEffect, useRef } from 'react';
import { X, ChevronLeft, ChevronRight, Tag, ShieldCheck } from 'lucide-react';

export default function LightboxModal({
  item,
  onClose,
  onPrev,
  onNext,
  hasPrev,
  hasNext,
  currentIndex,
  totalCount
}) {
  const modalRef = useRef(null);

  // Keyboard navigation: Escape, ArrowLeft, ArrowRight
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        onClose();
      } else if (e.key === 'ArrowLeft' && hasPrev) {
        onPrev();
      } else if (e.key === 'ArrowRight' && hasNext) {
        onNext();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    // Prevent background scrolling while modal is open
    document.body.style.overflow = 'hidden';

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [onClose, onPrev, onNext, hasPrev, hasNext]);

  if (!item) return null;

  return (
    <div
      className="lightbox-backdrop"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="lightbox-title"
    >
      <div className="lightbox-content" ref={modalRef}>
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-50 p-2 rounded-full bg-white/80 hover:bg-white text-maroon shadow-md border border-gold/40 cursor-pointer transition-colors"
          aria-label="Close modal (Escape)"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Left Image Pane */}
        <div className="lightbox-image-pane relative">
          <img
            src={item.src}
            alt={item.alt}
            className="rounded-lg shadow-inner"
          />

          {/* Previous / Next Arrow Controls */}
          {hasPrev && (
            <button
              onClick={onPrev}
              className="absolute left-3 top-1/2 -translate-y-1/2 p-2 rounded-full bg-black/50 hover:bg-black/75 text-white border border-gold/40 cursor-pointer transition-colors"
              aria-label="Previous artifact (Left Arrow)"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
          )}

          {hasNext && (
            <button
              onClick={onNext}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-full bg-black/50 hover:bg-black/75 text-white border border-gold/40 cursor-pointer transition-colors"
              aria-label="Next artifact (Right Arrow)"
            >
              <ChevronRight className="w-6 h-6" />
            </button>
          )}
        </div>

        {/* Right Details Pane */}
        <div className="lightbox-info-pane">
          <div>
            <div className="flex items-center justify-between text-xs text-ink-subtle pb-3 border-b border-maroon/10 mb-4">
              <span className="inline-flex items-center gap-1 font-bold text-gold uppercase tracking-wider">
                <Tag className="w-3.5 h-3.5" />
                <span>{item.categoryLabel}</span>
              </span>
              <span className="font-semibold text-ink-muted">
                {currentIndex + 1} of {totalCount}
              </span>
            </div>

            <h3 id="lightbox-title" className="text-2xl sm:text-3xl font-extrabold text-maroon mb-2">
              {item.title}
            </h3>
            
            <p className="text-sm font-semibold text-gold mb-4 font-editorial text-lg italic">
              {item.subtitle}
            </p>

            <p className="text-sm text-ink-muted leading-relaxed mb-6">
              {item.description}
            </p>
          </div>

          <div className="pt-4 border-t border-maroon/10">
            <div className="flex items-center gap-2 text-xs text-ink-subtle mb-4">
              <ShieldCheck className="w-4 h-4 text-peacock" />
              <span>Verified Authentic Rajasthani Cultural Asset</span>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-ink-subtle">
                Dimensions: {item.width} × {item.height}px
              </span>
              <div className="flex items-center gap-2">
                <button
                  onClick={onPrev}
                  disabled={!hasPrev}
                  className="px-3 py-1.5 rounded text-xs font-semibold border border-maroon/20 text-maroon disabled:opacity-30 cursor-pointer disabled:cursor-not-allowed hover:bg-maroon/5"
                >
                  Prev
                </button>
                <button
                  onClick={onNext}
                  disabled={!hasNext}
                  className="px-3 py-1.5 rounded text-xs font-semibold border border-maroon/20 text-maroon disabled:opacity-30 cursor-pointer disabled:cursor-not-allowed hover:bg-maroon/5"
                >
                  Next
                </button>
              </div>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
