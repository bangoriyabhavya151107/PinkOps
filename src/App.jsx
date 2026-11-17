import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import StorySection from './components/StorySection';
import StickyStorySection from './components/StickyStorySection';
import DashboardArea from './components/DashboardArea';
import HorizontalShowcase from './components/HorizontalShowcase';
import GallerySection from './components/GallerySection';
import CTASection from './components/CTASection';
import Footer from './components/Footer';
import LightboxModal from './components/LightboxModal';
import CustomCursor from './components/CustomCursor';
import PrivacyPage from './pages/PrivacyPage';
import TermsPage from './pages/TermsPage';
import { IMAGES_DATA } from './assets/imagesData';

export default function App() {
  const [currentRoute, setCurrentRoute] = useState(() => {
    const path = window.location.pathname;
    if (path === '/privacy' || path === '/terms') return path;
    return '/';
  });

  const [activeSection, setActiveSection] = useState('hero');
  const [scrollProgress, setScrollProgress] = useState(0);
  const [selectedImageId, setSelectedImageId] = useState(null);

  // Sync route with browser history (Back / Forward buttons)
  useEffect(() => {
    const handlePopState = () => {
      const path = window.location.pathname;
      if (path === '/privacy' || path === '/terms') {
        setCurrentRoute(path);
      } else {
        setCurrentRoute('/');
      }
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const navigate = (route) => {
    if (route !== currentRoute) {
      window.history.pushState({}, '', route);
      setCurrentRoute(route);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  // Track scroll progress and active section
  useEffect(() => {
    if (currentRoute !== '/') return;

    const handleScroll = () => {
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      setScrollProgress(scrolled);

      // Section spy
      const sections = ['hero', 'story', 'craft', 'dashboard', 'gallery'];
      for (const sectionId of sections) {
        const el = document.getElementById(sectionId);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.top <= 200 && rect.bottom >= 200) {
            setActiveSection(sectionId);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [currentRoute]);

  const scrollToSection = (sectionId) => {
    if (currentRoute !== '/') {
      navigate('/');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      const el = document.getElementById(sectionId);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Lightbox Modal helpers
  const currentImageIndex = IMAGES_DATA.findIndex(img => img.id === selectedImageId);
  const currentImage = currentImageIndex !== -1 ? IMAGES_DATA[currentImageIndex] : null;

  const handlePrevImage = () => {
    if (currentImageIndex > 0) {
      setSelectedImageId(IMAGES_DATA[currentImageIndex - 1].id);
    }
  };

  const handleNextImage = () => {
    if (currentImageIndex < IMAGES_DATA.length - 1) {
      setSelectedImageId(IMAGES_DATA[currentImageIndex + 1].id);
    }
  };

  return (
    <div className="relative min-h-screen bg-parchment text-ink selection:bg-gold/30 selection:text-maroon">
      {/* Scroll Progress Bar */}
      <div className="scroll-progress-container">
        <div 
          className="scroll-progress-bar"
          style={{ width: `${scrollProgress}%` }}
        />
      </div>

      {/* Subtle Custom Cursor (Desktop Only) */}
      <CustomCursor />

      {/* Dedicated Legal Route: Privacy Policy */}
      {currentRoute === '/privacy' && (
        <>
          <Header currentRoute="/privacy" onNavigate={navigate} />
          <main>
            <PrivacyPage onNavigate={navigate} />
          </main>
          <Footer onNavigate={navigate} />
        </>
      )}

      {/* Dedicated Legal Route: Terms & Conditions */}
      {currentRoute === '/terms' && (
        <>
          <Header currentRoute="/terms" onNavigate={navigate} />
          <main>
            <TermsPage onNavigate={navigate} />
          </main>
          <Footer onNavigate={navigate} />
        </>
      )}

      {/* Main Interactive Rajasthani Dashboard Experience */}
      {currentRoute === '/' && (
        <>
          <Header
            currentRoute="/"
            onNavigate={navigate}
            activeSection={activeSection}
          />
          <main>
            <Hero
              onExploreStory={() => scrollToSection('story')}
              onExploreGallery={() => scrollToSection('gallery')}
            />
            <StorySection onSelectImage={setSelectedImageId} />
            <StickyStorySection onSelectImage={setSelectedImageId} />
            <DashboardArea onSelectImage={setSelectedImageId} />
            <HorizontalShowcase onSelectImage={setSelectedImageId} />
            <GallerySection onSelectImage={setSelectedImageId} />
            <CTASection
              onScrollToTop={() => scrollToSection('hero')}
              onExploreDashboard={() => scrollToSection('dashboard')}
            />
          </main>
          <Footer onNavigate={navigate} />
        </>
      )}

      {/* Accessible Lightbox Modal */}
      {currentImage && (
        <LightboxModal
          item={currentImage}
          onClose={() => setSelectedImageId(null)}
          onPrev={handlePrevImage}
          onNext={handleNextImage}
          hasPrev={currentImageIndex > 0}
          hasNext={currentImageIndex < IMAGES_DATA.length - 1}
          currentIndex={currentImageIndex}
          totalCount={IMAGES_DATA.length}
        />
      )}
    </div>
  );
}
