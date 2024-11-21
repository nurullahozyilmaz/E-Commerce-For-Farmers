document.addEventListener('DOMContentLoaded', () => {
  const confettiContainer = document.querySelector('.confetti');
  const confettiColors = ['#ff5f6d', '#ffc371', '#03a6c3', '#ffffff'];

  function createConfettiPiece() {
      const confettiPiece = document.createElement('div');
      confettiPiece.classList.add('confetti-piece');
      confettiPiece.style.left = `${Math.random() * 100}%`;
      confettiPiece.style.backgroundColor = confettiColors[Math.floor(Math.random() * confettiColors.length)];
      confettiContainer.appendChild(confettiPiece);

      setTimeout(() => {
          confettiPiece.remove();
      }, 5000);
  }

  function generateConfetti() {
      setInterval(createConfettiPiece, 100);
  }

  generateConfetti();
});
