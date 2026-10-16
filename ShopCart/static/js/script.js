// Progressive enhancement: every shopping action also works without JavaScript.
document.querySelectorAll('[data-submit-once]').forEach(form => {
  form.addEventListener('submit', () => {
    const button = form.querySelector('button[type="submit"], button:not([type])');
    if (button) { button.disabled = true; button.textContent = 'Placing your order…'; }
  });
});
