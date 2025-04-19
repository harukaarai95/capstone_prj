const hamburger = document.getElementById('hamburger');
const menu = document.getElementById('menu');
const openIcon = document.querySelector('.openBar');
const closeIcon = document.querySelector('.closeIcon');

hamburger.addEventListener('click', () => {
  menu.classList.toggle('hiddenJs');
  openIcon.classList.toggle('hiddenJs');
  closeIcon.classList.toggle('hiddenJs');
});


document.querySelectorAll(".parent_g").forEach((item) => {
  item.addEventListener("click", () => {
      const genreWrap = item.querySelector(".ByGenreProductWrap");
      const genreId = item.getAttribute("data-id");

      if (genreWrap) {
          const productItems = genreWrap.querySelectorAll('p');
          if (productItems.length > 0) {
              genreWrap.classList.toggle("hiddenJs");
          }
      }
  });
});


document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('toggleBtn');
  const hiddenItems = document.querySelectorAll('.more-item');
  let expanded = false;

  toggleBtn.addEventListener('click', function () {
    expanded = !expanded;

    hiddenItems.forEach(item => {
      item.classList.toggle('hidden');
    });

    toggleBtn.textContent = expanded ? 'Show Less' : 'See More';
  });
});