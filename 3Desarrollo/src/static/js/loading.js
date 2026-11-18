// Animación táctica \ | / - hasta 100% para cada línea leída del CSV (HU-02)
function iniciarAnimacionCSV() {
  const rows = document.querySelectorAll('tr.coord-row');
  const frames = ['\\ 10%', '| 35%', '/ 65%', '- 90%', '100%'];

  rows.forEach((row) => {
    row.style.opacity = '0.25';
    const cell = row.querySelector('.loading-cell');
    if (cell) {
      cell.textContent = '\\ 0%';
      cell.style.color = '#f5a623';
    }
  });

  let rowIndex = 0;

  function animateNextRow() {
    if (rowIndex >= rows.length) return;
    const row = rows[rowIndex];
    const cell = row.querySelector('.loading-cell');
    row.style.opacity = '1';
    let step = 0;

    const timer = setInterval(() => {
      if (cell) {
        cell.textContent = frames[step];
        if (step === frames.length - 1) {
          cell.style.color = '#2ee59d';
        }
      }
      step++;
      if (step >= frames.length) {
        clearInterval(timer);
        rowIndex++;
        setTimeout(animateNextRow, 15);
      }
    }, 15);
  }

  animateNextRow();
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.querySelector('tr.coord-row')) {
    iniciarAnimacionCSV();
  }
});
