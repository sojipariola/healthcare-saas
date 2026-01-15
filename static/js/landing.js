document.addEventListener('DOMContentLoaded', function() {
  // Example: Animate CTA button
  const cta = document.querySelector('.cta-btn');
  if (cta) {
    cta.addEventListener('mouseenter', () => cta.style.transform = 'scale(1.08)');
    cta.addEventListener('mouseleave', () => cta.style.transform = 'scale(1)');
  }
});
