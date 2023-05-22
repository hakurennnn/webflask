const portraits = document.querySelectorAll('.picture-group');
const originalPositions = {};
let activePortrait = null;

function storeOriginalPosition(portraitNumber) {
  const portrait = document.querySelector(`.picture-group${portraitNumber}`);
  const containerWidth = portrait.parentElement.offsetWidth;
  const portraitWidth = portrait.offsetWidth;
  const originalPosition = (portrait.offsetLeft + portraitWidth / 2) / containerWidth;
  originalPositions[portraitNumber] = originalPosition;
}

function recalculateOriginalPositions() {
  for (let i = 1; i <= 5; i++) {
    storeOriginalPosition(i);
  }
}

function showInformation(portraitNumber) {
  const clickedPortrait = document.querySelector(`.picture-group${portraitNumber}`);
  const isResetPosition = clickedPortrait.style.left === '14%';

  if (isResetPosition) {
    const containerWidth = clickedPortrait.parentElement.offsetWidth;
    const portraitWidth = clickedPortrait.offsetWidth;
    const originalPosition = originalPositions[portraitNumber];
    const targetPosition = originalPosition * containerWidth - portraitWidth / 2;

    clickedPortrait.style.transition = 'left 0.5s ease-in-out';
    clickedPortrait.style.left = `${targetPosition}px`;

    portraits.forEach((portrait, index) => {
      if (index !== portraitNumber - 1) {
        portrait.style.transition = 'opacity 0.5s ease-in-out';
        portrait.style.opacity = '1';
        portrait.style.pointerEvents = 'auto';
      }
    });

    activePortrait = null;

    const information = document.querySelector(`#information${portraitNumber}`);
    information.classList.remove('active');
  } else if (activePortrait === clickedPortrait) {
    const information = document.querySelector(`#information${portraitNumber}`);
    information.classList.remove('active');
    activePortrait = null;
  } else if (!activePortrait) {
    const containerWidth = clickedPortrait.parentElement.offsetWidth;
    const portraitWidth = clickedPortrait.offsetWidth;
    const originalPosition = originalPositions[portraitNumber];
    const targetPosition = originalPosition * containerWidth - portraitWidth / 2;

    const information = document.querySelector(`#information${portraitNumber}`);
    information.classList.add('active');

    clickedPortrait.style.transition = 'left 0.5s ease-in-out';
    clickedPortrait.style.left = '14%';

    portraits.forEach((portrait, index) => {
      if (index !== portraitNumber - 1) {
        portrait.style.transition = 'opacity 0.5s ease-in-out';
        portrait.style.opacity = '0';
        portrait.style.pointerEvents = 'none';
      }
    });

    activePortrait = clickedPortrait;
  }
}

function hideAllInformation() {
  const informationElements = document.querySelectorAll('.information');
  informationElements.forEach((element) => {
    element.classList.remove('active');
  });
}

portraits.forEach((portrait, index) => {
  const portraitNumber = index + 1;
  portrait.addEventListener('click', () => showInformation(portraitNumber));
});

document.addEventListener('click', (event) => {
  const clickedPortrait = event.target.closest('.picture-group');

  if (!clickedPortrait && activePortrait) {
    return;
  }

  if (!clickedPortrait) {
    hideAllInformation();
    activePortrait = null;
    return;
  }

  const portraitNumber = parseInt(clickedPortrait.classList[0].slice(-1));
  showInformation(portraitNumber);
});

recalculateOriginalPositions();
window.addEventListener('resize', recalculateOriginalPositions);
