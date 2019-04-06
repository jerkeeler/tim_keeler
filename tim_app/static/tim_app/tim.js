try {
  (function () {
    // ===============================================
    // LANDING PAGE
    // ===============================================
    function loadingAnimation() {
      var elements = document.querySelectorAll('.headshot, .btn-top, .btn-right, .btn-bottom, .btn-left');
      elements.forEach(function (value, index) {
        value.classList.remove('invisible');
      });
    }

    loadingAnimation();

    // ===============================================
    // NAVBAR
    // ===============================================
    function burgerToggle() {
      var navBurger = document.getElementsByClassName('navbar-burger')[0];
      if (navBurger) {
        navBurger.addEventListener('click', () => {
          var target = document.getElementById(navBurger.dataset.target);
          target.classList.toggle('is-active');
          navBurger.classList.toggle('is-active');
        });
      }
    }

    burgerToggle();

    // ===============================================
    // FOOTER
    // ===============================================
    function getCopyrightYear() {
      var year = new Date().getFullYear();
      var yearElement = document.getElementById('currentYear');
      if (yearElement)
        yearElement.innerHTML = year.toString();
    }

    getCopyrightYear();
  })();

  var onRecaptchaLoadCallback = function () {
    function verifyCallback(response) {
      document.getElementById('contactSubmit').disabled = false;
    }

    grecaptcha.render('recaptcha', {
      'sitekey': document.getElementById('_recaptcha_site_key').innerHTML,
      'callback': verifyCallback,
      'theme': 'dark'
    });
  };
} catch (err) {
  console.error(err);
  gtag('event', 'exception', {
    'description': err,
    'fatal': false
  });
}
