(() => {
  'use strict';

  const content = {
    "id": {
      "projectCta": "Bahas Proyek",
      "backHero": "Kembali ke beranda",
      "floatingWhatsapp": "Chat WhatsApp",
      "skip": "Ke konten utama",
      "navigation": "Navigasi utama",
      "mobileNavigation": "Navigasi mobile",
      "languageLabel": "Pilihan bahasa",
      "menu": "Menu",
      "menuLabel": "Menu navigasi",
      "close": "Tutup",
      "navAbout": "Tentang",
      "navProcess": "Cara kerja",
      "navContact": "Kontak",
      "heroEyebrow": "Studio desain & pengembangan",
      "brandTagline": "Studio pengembangan software untuk bisnis.",
      "heroLine1": "Software",
      "heroLine2": "untuk cara kerja",
      "heroLine3": "bisnis Anda.",
      "heroDescription": "Arsa merancang dan membangun software sesuai kebutuhan bisnis. Kami mulai dengan memahami proses kerja tim Anda, lalu menyusun fungsi dan tampilan yang dibutuhkan.",
      "heroCta": "Bahas Proyek",
      "viewServices": "Lihat layanan",
      "navServices": "Layanan",
      "servicesLabel": "Apa yang bisa kami bantu?",
      "servicesNote": "sesuai kebutuhan bisnis Anda",
      "statementLine1": "Kebutuhannya kita bahas.",
      "statementLine2": "Pengerjaannya kami rencanakan.",
      "processLink": "Lihat cara kerja",
      "aboutLabel": "Tentang studio",
      "aboutTitle1": "Kami mulai dengan",
      "aboutTitle2": "memahami bisnis Anda.",
      "aboutDescription": "Kami membahas tujuan proyek, siapa yang akan menggunakan software, dan pekerjaan yang perlu dibantu. Hasil pembahasan ini menjadi dasar rancangan dan pengembangan.",
      "serviceBusinessTitle": "Website & aplikasi bisnis",
      "serviceBusinessBody": "Kami merancang website dan aplikasi sesuai kebutuhan bisnis, baik untuk melayani pelanggan maupun mendukung pekerjaan tim.",
      "serviceOperationsTitle": "Sistem operasional",
      "serviceOperationsBody": "Kami membangun software untuk membantu proses kerja internal, seperti pencatatan, pengelolaan data, persetujuan, dan pelaporan.",
      "serviceAiTitle": "Implementasi AI",
      "serviceAiBody": "Kami membantu menerapkan AI ke dalam proses bisnis. Kita mulai dengan menentukan pekerjaan yang bisa dibantu AI, lalu merancang penerapannya sesuai kebutuhan tim.",
      "otherNeeds": "Punya kebutuhan lain? Mari diskusikan.",
      "processLine1": "Cara kami mengerjakan",
      "processLine2": "proyek Anda.",
      "phase1Title": "Bahas kebutuhan.",
      "phase1Body": "Kami membahas tujuan dan proses kerja tim Anda, lalu menyepakati kebutuhan, ruang lingkup, dan rancangan sebelum pengembangan dimulai.",
      "phase2Title": "Kembangkan & uji.",
      "phase2Body": "Kami mengembangkan software berdasarkan rancangan, lalu menguji fungsi dan alurnya sesuai kebutuhan yang telah disepakati.",
      "phase3Title": "Tinjau & serahkan.",
      "phase3Body": "Kita meninjau hasilnya bersama. Kami menyiapkan penyerahan software dan membahas kebutuhan berikutnya.",
      "processLabel": "Cara kerja",
      "workLine1": "Ruang untuk",
      "workLine2": "hasil kerja.",
      "workLabel": "Karya",
      "workStatus": "Portfolio",
      "workEmptyTitle": "Karya belum\nditampilkan.",
      "workEmptyBody": "Belum ada materi proyek yang dipublikasikan di halaman ini. Hubungi kami untuk membahas kebutuhan bisnis Anda.",
      "workContact": "Diskusikan proyek Anda",
      "workCaption": "Gambar merupakan ilustrasi studio, bukan dokumentasi proyek atau ruang kerja asli.",
      "contactLine1": "Mari bahas",
      "contactLine2": "kebutuhan bisnis Anda.",
      "contactLabel": "Ada kebutuhan software?",
      "contactBody": "Ceritakan proses kerja yang ingin dibantu atau software yang ingin dikembangkan. Jika kebutuhannya belum terperinci, kita bisa membahasnya bersama.",
      "contactCta": "Bahas Proyek",
      "footerExplore": "Jelajahi",
      "footerConnect": "Terhubung",
      "footerAddress": "Grogol Petamburan, Jakarta Barat, Indonesia",
      "footerEmail": "hello@arsamk.com",
      "footerStudio": "Software sesuai kebutuhan bisnis Anda.",
      "imageError": "Ilustrasi tidak dapat ditampilkan.",
      "whatsappMessage": "Halo Arsa, saya ingin membahas kebutuhan software untuk bisnis saya.",
      "metaDescription": "Arsa Miliar Kreasi membantu pengembangan software, sistem operasional, dan implementasi AI sesuai kebutuhan serta proses kerja bisnis Anda.",
      "pageTitle": "Arsa Miliar Kreasi | Pengembangan Software & Implementasi AI"
    },
    "en": {
      "projectCta": "Discuss a Project",
      "backHero": "Back to the top",
      "floatingWhatsapp": "Chat on WhatsApp",
      "skip": "Skip to main content",
      "navigation": "Main navigation",
      "mobileNavigation": "Mobile navigation",
      "languageLabel": "Choose language",
      "menu": "Menu",
      "menuLabel": "Navigation menu",
      "close": "Close",
      "navAbout": "About",
      "navProcess": "Process",
      "navContact": "Contact",
      "heroEyebrow": "Design & development studio",
      "brandTagline": "A software development studio for businesses.",
      "heroLine1": "Software",
      "heroLine2": "built around",
      "heroLine3": "your business.",
      "heroDescription": "Arsa designs and builds software around your business needs. We start by understanding how your team works, then plan the features and interface you need.",
      "heroCta": "Discuss a Project",
      "viewServices": "See our services",
      "navServices": "Services",
      "servicesLabel": "How can we help?",
      "servicesNote": "shaped around your business",
      "statementLine1": "We discuss what you need.",
      "statementLine2": "Then we plan the work.",
      "processLink": "See our process",
      "aboutLabel": "About the studio",
      "aboutTitle1": "We start by understanding",
      "aboutTitle2": "your business.",
      "aboutDescription": "We discuss your project goals, who will use the software, and the work it needs to support. These discussions guide the design and development.",
      "serviceBusinessTitle": "Business websites & apps",
      "serviceBusinessBody": "We design websites and apps around your business needs, whether to serve customers or support your team’s work.",
      "serviceOperationsTitle": "Operational systems",
      "serviceOperationsBody": "We build software to support internal processes such as record keeping, data management, approvals, and reporting.",
      "serviceAiTitle": "AI implementation",
      "serviceAiBody": "We help apply AI to business processes. Together, we identify tasks AI can support, then plan how to implement it around your team’s needs.",
      "otherNeeds": "Have another project in mind? Let’s discuss it.",
      "processLine1": "How we work",
      "processLine2": "on your project.",
      "phase1Title": "Discuss requirements.",
      "phase1Body": "We discuss your goals and how your team works, then agree on requirements, scope, and design before development begins.",
      "phase2Title": "Build & test.",
      "phase2Body": "We build your software, then test its features and flows against the agreed requirements.",
      "phase3Title": "Review & hand over.",
      "phase3Body": "We review the result together, prepare the handover, and discuss what you need next.",
      "processLabel": "Our process",
      "workLine1": "A space for",
      "workLine2": "the work.",
      "workLabel": "Our work",
      "workStatus": "Portfolio",
      "workEmptyTitle": "No projects\ndisplayed yet.",
      "workEmptyBody": "No project materials have been published on this page yet. Contact us directly to discuss what your business needs.",
      "workContact": "Talk about your project",
      "workCaption": "This is a studio illustration, not documentation of a project or an actual workspace.",
      "contactLine1": "Let’s discuss",
      "contactLine2": "your business needs.",
      "contactLabel": "Need software for your business?",
      "contactBody": "Tell us about the work you need to support or the software you want to develop. If the details are still taking shape, we can discuss them together.",
      "contactCta": "Discuss a Project",
      "footerExplore": "Explore",
      "footerConnect": "Connect",
      "footerAddress": "Grogol Petamburan, Jakarta Barat, Indonesia",
      "footerEmail": "hello@arsamk.com",
      "footerStudio": "Software built around your business needs.",
      "imageError": "The illustration could not be displayed.",
      "whatsappMessage": "Hi Arsa, I would like to discuss software for my business.",
      "metaDescription": "Arsa Miliar Kreasi designs and builds business software, operational systems, and AI implementations around your team’s needs and workflows.",
      "pageTitle": "Software Development & AI Implementation | Arsa Miliar Kreasi"
    }
  };

  function setMeta(selector, value) {
    const element = document.querySelector(selector);
    if (element) element.setAttribute('content', value);
  }

  function initializeLanguage() {
    function setLanguage(next) {
      const language = Object.hasOwn(content, next) ? next : 'id';
      const copy = content[language];
      document.documentElement.lang = language;
      document.querySelectorAll('[data-i18n]').forEach((element) => {
        const key = element.getAttribute('data-i18n');
        const value = copy[key] ?? content.id[key];
        if (typeof value === 'string') element.textContent = value;
      });
      document.querySelectorAll('[data-i18n-aria]').forEach((element) => {
        const key = element.getAttribute('data-i18n-aria');
        const value = copy[key] ?? content.id[key];
        if (typeof value === 'string') element.setAttribute('aria-label', value);
      });
      document.querySelectorAll('[data-language]').forEach((button) => {
        button.setAttribute('aria-pressed', String(button.dataset.language === language));
      });
      document.querySelectorAll('.whatsapp').forEach((link) => {
        link.href = 'https://wa.me/6289670001606?text=' + encodeURIComponent(copy.whatsappMessage);
      });
      document.title = copy.pageTitle;
      setMeta('meta[name="description"]', copy.metaDescription);
      for (const selector of ['meta[property="og:title"]', 'meta[name="twitter:title"]']) setMeta(selector, copy.pageTitle);
      for (const selector of ['meta[property="og:description"]', 'meta[name="twitter:description"]']) setMeta(selector, copy.metaDescription);
      for (const selector of ['meta[property="og:image"]', 'meta[name="twitter:image"]']) {
        setMeta(selector, 'https://arsamk.com/assets/img/social/og-' + language + '.png');
      }
      const imageAlt = 'Arsa Miliar Kreasi: ' + [copy.heroLine1, copy.heroLine2, copy.heroLine3].join(' ');
      setMeta('meta[property="og:image:alt"]', imageAlt);
      setMeta('meta[name="twitter:image:alt"]', imageAlt);
      setMeta('meta[property="og:locale"]', language === 'en' ? 'en_US' : 'id_ID');
      try { localStorage.setItem('arsa-language', language); } catch {
        // Language switching remains available when browser storage is blocked.
      }
    }

    let initialLanguage = 'id';
    try { initialLanguage = localStorage.getItem('arsa-language') || 'id'; } catch {
      // Local files and private browsing may restrict persistent storage.
    }
    document.querySelectorAll('[data-language]').forEach((button) => {
      button.addEventListener('click', () => setLanguage(button.dataset.language));
    });
    setLanguage(initialLanguage);
    document.body.classList.add('language-ready');
  }

  function initializeMenu() {
    const menu = document.querySelector('#mobile-menu');
    const openButton = document.querySelector('#menu-open');
    const closeButton = document.querySelector('#menu-close');
    if (!menu || !openButton || !closeButton || typeof menu.showModal !== 'function') return;

    function closeMenu(restoreFocus = true) {
      if (menu.open) menu.close();
      document.body.classList.remove('menu-open');
      openButton.setAttribute('aria-expanded', 'false');
      if (restoreFocus && getComputedStyle(openButton).display !== 'none') openButton.focus();
    }
    openButton.addEventListener('click', () => {
      menu.showModal();
      openButton.setAttribute('aria-expanded', 'true');
      document.body.classList.add('menu-open');
    });
    closeButton.addEventListener('click', () => closeMenu());
    menu.addEventListener('cancel', (event) => {
      event.preventDefault();
      closeMenu();
    });
    menu.addEventListener('keydown', (event) => {
      if (event.key !== 'Tab') return;
      const controls = [...menu.querySelectorAll('button:not([disabled]), a[href]')]
        .filter((element) => element.getClientRects().length);
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (!first) return;
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
    menu.addEventListener('close', () => {
      document.body.classList.remove('menu-open');
      openButton.setAttribute('aria-expanded', 'false');
    });
    menu.querySelectorAll('a[href^="#"]').forEach((link) => {
      link.addEventListener('click', (event) => {
        const target = document.getElementById(link.hash.slice(1));
        if (!target) return;
        event.preventDefault();
        closeMenu(false);
        target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
        target.scrollIntoView({ block: 'start' });
        history.pushState(null, '', link.hash);
      });
    });
    menu.querySelector('.whatsapp')?.addEventListener('click', () => closeMenu());
    matchMedia('(min-width: 901px)').addEventListener('change', (event) => {
      if (event.matches) closeMenu(false);
    });
    document.body.classList.add('js-ready');
  }

  function initializeSectionNavigation() {
    if (!('IntersectionObserver' in window)) return;
    const links = document.querySelectorAll('.nav a');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((link) => {
          if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-15% 0px -55% 0px', threshold: 0 });
    document.querySelectorAll('main section[id], main #layanan').forEach((section) => observer.observe(section));
  }

  function initializeImageFallbacks() {
    document.querySelectorAll('img').forEach((image) => {
      function showError() {
        if (image.parentElement.querySelector('.image-error')) {
          image.parentElement.classList.add('asset-error');
        }
      }
      image.addEventListener('error', showError);
      if (image.complete && image.naturalWidth === 0) showError();
    });
  }

  initializeLanguage();
  initializeMenu();
  initializeSectionNavigation();
  initializeImageFallbacks();
  const year = document.querySelector('#year');
  if (year) year.textContent = new Intl.DateTimeFormat('en', { year: 'numeric', timeZone: 'Asia/Jakarta' }).format(new Date());
})();
