// Simple modal logic for confirmation dialogs
function showModal(id) {
  document.getElementById(id).style.display = 'block';
}
function closeModal(id) {
  document.getElementById(id).style.display = 'none';
}
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.modal-trigger').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      showModal(btn.dataset.target);
    });
  });
  document.querySelectorAll('.modal .close').forEach(function(btn) {
    btn.addEventListener('click', function() {
      closeModal(btn.closest('.modal').id);
    });
  });
});
