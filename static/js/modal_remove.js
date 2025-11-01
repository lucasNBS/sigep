(() => {
  const modal = document.getElementById('removeModal');
  const form  = document.getElementById('form-remove');
  const nome  = document.getElementById('remove-nome');

  function open(instId, instNome = '') {
    nome.textContent = instNome || '—';
    modal.classList.add('active');
  }

  function close() {
    modal.classList.remove('active');
  }

  window.openRemoveModal = open;

  // close for buttons and outside click
  document.getElementById('removeModalCloseBtn')?.addEventListener('click', close);
  document.getElementById('removeModalCancelBtn')?.addEventListener('click', close);
  modal.addEventListener('mousedown', (e) => { if (e.target === modal) close(); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) close();
  });
})();

