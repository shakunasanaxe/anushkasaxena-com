// Filter inputs — live-filter cards inside the target list
document.querySelectorAll('.as-filter input[data-filter]').forEach(input => {
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase();
    const list = document.getElementById(input.dataset.filter);
    if (!list) return;
    const cards = list.querySelectorAll('.pub-card, .media-card, .quote-card');
    cards.forEach(card => {
      const match = card.textContent.toLowerCase().includes(q);
      if (q) {
        card.style.display = match ? '' : 'none';
        if (match) card.classList.remove('hidden');
      } else {
        card.style.display = '';
      }
    });
    // Hide the load-more button while filtering
    const wrap = list.parentElement.querySelector('.load-more-wrap');
    if (wrap) wrap.style.display = q ? 'none' : '';
  });
});

// Load more — reveal hidden cards in the sibling list
document.querySelectorAll('.load-more').forEach(btn => {
  btn.addEventListener('click', () => {
    const list = btn.closest('.load-more-wrap').previousElementSibling;
    if (!list) return;
    list.querySelectorAll('.hidden').forEach(el => el.classList.remove('hidden'));
    btn.closest('.load-more-wrap').style.display = 'none';
  });
});
