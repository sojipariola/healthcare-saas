/* Landing Page - Responsive Enhancements */

document.addEventListener('DOMContentLoaded', function() {
  // Smooth scroll for CTA buttons
  const ctaButtons = document.querySelectorAll('.cta-btn, .plan-cta');
  ctaButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      document.documentElement.style.scrollBehavior = 'smooth';
    });
  });

  // Intersection Observer for fade-in animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe feature and plan cards for animation
  document.querySelectorAll('.feature, .plan').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(element);
  });

  // Responsive image handling
  const heroImage = document.querySelector('.hero-image');
  if (heroImage) {
    const img = new Image();
    img.src = heroImage.src;
  }

  // Add touch-friendly enhancements
  if ('ontouchstart' in window) {
    document.body.classList.add('touch-device');
    
    const buttons = document.querySelectorAll('.cta-btn, .plan-cta');
    buttons.forEach(btn => {
      btn.style.minHeight = '48px';
      btn.style.minWidth = '48px';
      btn.style.display = 'flex';
      btn.style.alignItems = 'center';
      btn.style.justifyContent = 'center';
    });
  }

  // Feature grid card interactions
  const features = document.querySelectorAll('.feature');
  features.forEach(feature => {
    feature.addEventListener('mouseenter', function() {
      this.style.cursor = 'pointer';
    });
  });

  // Plan card pricing visibility
  const plans = document.querySelectorAll('.plan');
  plans.forEach((plan, index) => {
    plan.style.animationDelay = (index * 0.1) + 's';
  });
});

// Detect device type
const isMobile = () => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
};

const isTablet = () => {
  return /iPad|Android(?!.*Mobi)/i.test(navigator.userAgent);
};
