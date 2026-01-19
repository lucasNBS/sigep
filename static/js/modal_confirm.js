document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('removeModal');
  const form = document.getElementById('form-remove');

  document.querySelectorAll('.btn-icon.delete').forEach(button => {
    button.addEventListener('click', () => {
      const url = button.dataset.url;

      form.action = url;
      modal.classList.add('active');
    });
  });

  document.querySelectorAll('#conclude').forEach(button => {
    button.addEventListener('click', () => {
      const url = button.dataset.url;

      form.action = url;
      modal.classList.add('active');
    });
  });

  document.getElementById('removeModalCloseBtn').onclick = () => {
    modal.classList.remove('active');
  };

  document.getElementById('removeModalCancelBtn').onclick = () => {
    modal.classList.remove('active');
  };
});
