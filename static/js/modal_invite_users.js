(() => {
  const modal = document.getElementById('inviteUserModal');
  const form  = document.getElementById('form-invite-user');

  const inputEmail = document.getElementById('invite-email');
  const inputCargo = document.getElementById('invite-role');

  function open(email = '', cargo = 'consultor') {

    if (inputEmail) inputEmail.value = email;
    if (inputCargo) inputCargo.value = cargo;

    modal.classList.add('active');
  }

  function close() {
    modal.classList.remove('active');
  }

  window.openInviteUserModal = open;

  document.getElementById('inviteUserModalCloseBtn')
    ?.addEventListener('click', close);

  document.getElementById('inviteUserModalCancelBtn')
    ?.addEventListener('click', close);

  // close for buttons and outside click
  modal.addEventListener('mousedown', (e) => {
    if (e.target === modal) close();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) close();
  });

})();
