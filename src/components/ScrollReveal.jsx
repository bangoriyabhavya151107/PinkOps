import React, { useEffect, useRef, useState } from 'react';

export default function ScrollReveal({
  children,
  animation = 'fade-up', // fade-up, fade-left, fade-right, scale-in
  delay = 0,
  threshold = 0.15,
  className = '',
  style = {}
}) {
  const [isVisible, setIsVisible] = useState(false);
  const elementRef = useRef(null);

  useEffect(() => {
    // Respect user's motion preferences
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
      setIsVisible(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.unobserve(entry.target);
        }
      },
      {
        threshold,
        rootMargin: '0px 0px -40px 0px'
      }
    );

    const currentEl = elementRef.current;
    if (currentEl) {
      observer.observe(currentEl);
    }

    return () => {
      if (currentEl) {
        observer.unobserve(currentEl);
      }
    };
  }, [threshold]);

  const animationClass = `reveal-${animation}`;

  return (
    <div
      ref={elementRef}
      className={`reveal-init ${animationClass} ${isVisible ? 'reveal-visible' : ''} ${className}`}
      style={{
        ...style,
        transitionDelay: `${delay}ms`
      }}
    >
      {children}
    </div>
  );
}
