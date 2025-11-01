(() => {
  const modal = document.getElementById('editModal');
  const form  = document.getElementById('form-edit');
  const nome  = document.getElementById('edit-nome');
  const cnpj  = document.getElementById('edit-cnpj');
  const file  = document.getElementById('logo-input');
  const fileName = document.getElementById('logo-filename');

  function open(instId, instNome = '', instCnpj = '') {
    if (nome) nome.value = instNome || '';
    if (cnpj) cnpj.value = instCnpj || '';
    if (file) file.value = '';
    if (fileName) fileName.textContent = 'Selecione uma imagem…';
    modal.classList.add('active');
  }
  function close() {
    modal.classList.remove('active');
  }

  window.openEditModal = open;

  // close for buttons and outside click
  document.getElementById('editModalCloseBtn')?.addEventListener('click', close);
  document.getElementById('editModalCancelBtn')?.addEventListener('click', close);
  modal.addEventListener('mousedown', (e) => { if (e.target === modal) close(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && modal.classList.contains('active')) close(); });

  // arquiv name
  file?.addEventListener('change', () => {
    fileName.textContent = file.files?.[0]?.name || 'Selecione uma imagem…';
  });

  // CNPJ mask
  cnpj?.addEventListener('input', () => {
    const d = cnpj.value.replace(/\D/g,'').slice(0,14);
    let out = '';
    if (d.length > 0) out = d.substring(0,2);
    if (d.length > 2) out += '.' + d.substring(2,5);
    if (d.length > 5) out += '.' + d.substring(5,8);
    if (d.length > 8) out += '/' + d.substring(8,12);
    if (d.length > 12) out += '-' + d.substring(12,14);
    cnpj.value = out;
  });
})();
