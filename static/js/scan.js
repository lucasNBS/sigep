const html5QrCode = new Html5Qrcode("reader");

html5QrCode
  .start(
    { facingMode: "environment" },
    {
      fps: 10,
      qrbox: 350,
      aspectRatio: 1.0,
    },
    (qrCodeMessage) => {
      window.location.href = qrCodeMessage;
    },
    (errorMessage) => {
      console.debug(errorMessage);
    },
  )
  .catch((err) => {
    console.error("Erro ao iniciar câmera", err);
  });
