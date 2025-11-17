(() => {
  const modal = document.getElementById('registerItemModal');
  const form  = document.getElementById('form-register-item');

  const inputSerial = document.getElementById('serial-input');

  function open(serial = '') {
    if (inputSerial) inputSerial.value = serial;
    modal.classList.add('active');
  }

  function close() {
    modal.classList.remove('active');
  }

  window.openRegisterItemModal = open;

  document.getElementById('registerItemModalCloseBtn')
    ?.addEventListener('click', close);

  document.getElementById('registerItemModalCancelBtn')
    ?.addEventListener('click', close);

  modal.addEventListener('mousedown', (e) => {
    if (e.target === modal) close();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      close();
    }
  });
})();
