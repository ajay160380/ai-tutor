// ============================================
// EduAI — Main JavaScript
// Dark mode, navbar, scroll effects, utilities
// ============================================

document.addEventListener('DOMContentLoaded', function () {

  // ---- Dark Mode Toggle ----
  const themeToggle = document.getElementById('themeToggle');
  const body = document.body;
  const html = document.documentElement;

  // Load saved theme
  const savedTheme = localStorage.getItem('eduai_theme') || 'light';
  html.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('eduai_theme', next);
      updateThemeIcon(next);
    });
  }

  function updateThemeIcon(theme) {
    if (!themeToggle) return;
    const icon = themeToggle.querySelector('i');
    if (icon) {
      icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
    }
  }

  // ---- Scroll to Top Button ----
  const scrollTopBtn = document.getElementById('scrollTopBtn');
  if (scrollTopBtn) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 400) {
        scrollTopBtn.classList.add('visible');
      } else {
        scrollTopBtn.classList.remove('visible');
      }
    });

    scrollTopBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ---- Navbar Active Link Highlight ----
  const currentPath = window.location.pathname;
  document.querySelectorAll('.navbar-custom .nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
      link.classList.add('active');
    }
  });

  // ---- Smooth Scroll for Anchor Links ----
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Close mobile menu if open
        const navCollapse = document.querySelector('.navbar-collapse.show');
        if (navCollapse) {
          const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
          if (bsCollapse) bsCollapse.hide();
        }
      }
    });
  });

  // ---- Animate Elements on Scroll ----
  const animateOnScroll = function () {
    const elements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-fadeinup');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    elements.forEach(el => observer.observe(el));
  };
  animateOnScroll();

  // ---- Hero Particles ----
  const particlesContainer = document.getElementById('heroParticles');
  if (particlesContainer) {
    for (let i = 0; i < 20; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = Math.random() * 100 + '%';
      particle.style.animationDuration = (Math.random() * 10 + 8) + 's';
      particle.style.animationDelay = (Math.random() * 5) + 's';
      particle.style.width = (Math.random() * 4 + 3) + 'px';
      particle.style.height = particle.style.width;
      particlesContainer.appendChild(particle);
    }
  }

  // ---- Auto-resize Textarea ----
  const autoResizeTextareas = document.querySelectorAll('.auto-resize');
  autoResizeTextareas.forEach(textarea => {
    textarea.addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 150) + 'px';
    });
  });

  // ---- Toast Notifications (auto-dismiss Django messages) ----
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // ---- Format Timestamp ----
  window.formatTime = function (dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);

    if (diff < 60) return 'Abhi abhi';
    if (diff < 3600) return Math.floor(diff / 60) + ' min pehle';
    if (diff < 86400) return Math.floor(diff / 3600) + ' ghante pehle';
    return Math.floor(diff / 86400) + ' din pehle';
  };

  // ---- Countdown Timer Utility ----
  window.startCountdown = function (elementId, totalSeconds, onComplete) {
    const el = document.getElementById(elementId);
    if (!el) return;

    let remaining = totalSeconds;

    const interval = setInterval(() => {
      remaining--;
      const hours = Math.floor(remaining / 3600);
      const mins = Math.floor((remaining % 3600) / 60);
      const secs = remaining % 60;

      el.textContent = `${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

      // Turn red when < 5 minutes
      if (remaining <= 300) {
        el.classList.add('danger');
      }

      if (remaining <= 0) {
        clearInterval(interval);
        if (onComplete) onComplete();
      }
    }, 1000);

    return interval;
  };

  // ---- Render Markdown-like content ----
  window.renderMarkdown = function (text) {
    if (!text) return '';
    let html = text
      // Code blocks
      .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
      // Inline code
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      // Bold
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      // Italic
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      // Headers
      .replace(/^### (.+)$/gm, '<h5 class="fw-bold mt-3 mb-2">$1</h5>')
      .replace(/^## (.+)$/gm, '<h4 class="fw-bold mt-3 mb-2">$1</h4>')
      // Numbered lists
      .replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>')
      // Bullet lists
      .replace(/^[-•]\s+(.+)$/gm, '<li>$1</li>')
      // Line breaks
      .replace(/\n\n/g, '<br><br>')
      .replace(/\n/g, '<br>');

    // Wrap consecutive <li> elements
    html = html.replace(/((?:<li>.*?<\/li>\s*<br>?)+)/g, '<ol class="ps-3 mb-2">$1</ol>');

    return html;
  };

});
