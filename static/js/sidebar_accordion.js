document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.sidebar .accordion-toggle').forEach(function(toggle) {
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      const parent = toggle.closest('.accordion-group');
      parent.classList.toggle('open');
      const panel = parent.querySelector('.accordion-panel');
      if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
      } else {
        panel.style.maxHeight = panel.scrollHeight + 'px';
      }
    });
  });
});
