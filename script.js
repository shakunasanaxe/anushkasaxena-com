// Navbar scroll effect
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  navbar?.classList.toggle('scrolled', window.scrollY > 10);
});

// Mobile menu toggle
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
hamburger?.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  hamburger.classList.toggle('active');
});

// Close mobile menu on link click
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks?.classList.remove('open');
    hamburger?.classList.remove('active');
  });
});

// Publication tab switching
document.querySelectorAll('.pub-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tab;
    document.querySelectorAll('.pub-tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.pub-tab-content').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(target)?.classList.add('active');
  });
});

// Search filter — publications
document.querySelectorAll('.pub-search-input').forEach(input => {
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase();
    const tabId = input.dataset.search;
    const list = document.getElementById(tabId + '-list');
    if (!list) return;
    list.querySelectorAll('.pub-card').forEach(card => {
      const text = card.textContent.toLowerCase();
      card.style.display = text.includes(q) ? '' : 'none';
    });
  });
});

// Search filter — media page
const mediaSearch = document.getElementById('mediaSearch');
if (mediaSearch) {
  mediaSearch.addEventListener('input', () => {
    const q = mediaSearch.value.toLowerCase();
    document.querySelectorAll('.media-card, .quote-card').forEach(card => {
      const text = card.textContent.toLowerCase();
      // Don't hide cards that are already hidden by load-more
      if (!card.classList.contains('hidden') || q === '') {
        card.style.display = text.includes(q) ? '' : 'none';
      }
      // If searching, temporarily show hidden cards that match
      if (q && card.classList.contains('hidden') && text.includes(q)) {
        card.style.display = '';
      }
      if (!q && card.classList.contains('hidden')) {
        card.style.display = 'none';
      }
    });
  });
}

// Load more functionality
document.querySelectorAll('.load-more').forEach(btn => {
  btn.addEventListener('click', () => {
    const section = btn.closest('section');
    if (!section) return;
    section.querySelectorAll('.hidden').forEach(item => {
      item.classList.remove('hidden');
    });
    btn.style.display = 'none';
  });
});

// Set active nav link based on current page
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav-links a').forEach(link => {
  link.classList.remove('active');
  const href = link.getAttribute('href');
  if (href === currentPage || (currentPage === '' && href === 'index.html')) {
    link.classList.add('active');
  }
});
