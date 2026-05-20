// Mobile nav toggle
document.addEventListener('click', (e) => {
  const toggle = e.target.closest('[data-nav-toggle]');
  if (toggle) {
    document.querySelector('[data-nav-mobile]')?.classList.toggle('open');
  }
});

// Tabs (Timetable)
document.querySelectorAll('[data-tabs]').forEach((group) => {
  group.querySelectorAll('.tab').forEach((tab) => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      group.querySelectorAll('.tab').forEach((t) => t.classList.toggle('active', t === tab));
      const panels = document.querySelectorAll(`[data-panel-group="${group.dataset.tabs}"]`);
      panels.forEach((p) => {
        p.hidden = p.dataset.panel !== target;
      });
    });
  });
});

// Blog filter (visual only)
document.querySelectorAll('.blog-filter').forEach((el) => {
  el.addEventListener('click', () => {
    document.querySelectorAll('.blog-filter').forEach((f) => f.classList.remove('active'));
    el.classList.add('active');
  });
});
