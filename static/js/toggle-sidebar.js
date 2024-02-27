document.addEventListener('click', function(event) {
  const offCanvasMenu = document.querySelector('.sidebar');
  const toggleButton = document.querySelector('.toggle-button');

  // Verifica se o clique foi dentro do menu ou no botão de alternância
  if (!offCanvasMenu.contains(event.target) && event.target !== toggleButton) {
    offCanvasMenu.style.left = '-250px'; // Fecha o menu
  }
});

function toggleMenu() {
    const offCanvasMenu = document.querySelector('.sidebar');
    offCanvasMenu.style.left = offCanvasMenu.style.left === '0px' ? '-250px' : '0px';
  }