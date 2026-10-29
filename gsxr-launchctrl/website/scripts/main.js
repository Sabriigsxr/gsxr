/* GSXR LAUNCHCTRL — Landing Page JavaScript */
// Concept terminal typing effect + navigation enhancements

(function() {
  'use strict';

  // Terminal typing animation for concept preview
  const terminalCommands = [
    'launchctrl plan "build API integration"',
    'launchctrl select ollama:codellama',
    'launchctrl coordinate --agents=3',
    'launchctrl execute --verbose',
    'launchctrl status'
  ];

  const commandOutputs = {
    'launchctrl plan "build API integration"':
      '<div class="terminal-output-label">Mission Plan:</div>' +
      '<div class="terminal-output-value">• Decompose: auth, endpoints, tests</div>' +
      '<div class="terminal-output-value">• Complexity: MODERATE (est. 48 min)</div>' +
      '<div class="terminal-output-value text-cyan">→ Plan created. Run "launchctrl execute"</div>',
    'launchctrl select ollama:codellama':
      '<div class="terminal-output-label">Model:</div>' +
      '<div class="terminal-output-value">ollama:codellama (local) — ready</div>',
    'launchctrl coordinate --agents=3':
      '<div class="terminal-output-label">Agents:</div>' +
      '<div class="terminal-output-value">• planner-agent — active</div>' +
      '<div class="terminal-output-value">• executor-agent — active</div>' +
      '<div class="terminal-output-value">• validator-agent — queued</div>',
    'launchctrl execute --verbose':
      '<div class="terminal-output-label">Status:</div>' +
      '<div class="terminal-output-value">🚧 CONCEPT PREVIEW — not yet implemented</div>',
    'launchctrl status':
      '<div class="terminal-output-label">System:</div>' +
      '<div class="terminal-output-value">🟡 IN DEVELOPMENT</div>'
  };

  function typeText(element, text, speed, callback) {
    let i = 0;
    function type() {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        i++;
        setTimeout(type, speed);
      } else if (callback) {
        callback();
      }
    }
    type();
  }

  function cycleTerminalCommands() {
    const typedCommand = document.getElementById('typedCommand');
    const commandOutput = document.getElementById('commandOutput');

    if (!typedCommand || !commandOutput) return;

    let index = 0;
    function showNext() {
      typedCommand.textContent = '';
      commandOutput.innerHTML = '';

      const cmd = terminalCommands[index];
      typeText(typedCommand, cmd, 50, function() {
        setTimeout(function() {
          commandOutput.innerHTML = commandOutputs[cmd] || '';
          setTimeout(showNext, 3000);
        }, 500);
      });

      index = (index + 1) % terminalCommands.length;
    }

    showNext();
  }

  // Smooth scroll for anchor links
  function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }

  // Scroll spy for active nav links
  function initScrollSpy() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');

    if (!navLinks.length || !sections.length) return;

    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.4
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const id = entry.target.getAttribute('id');
        const navLink = document.querySelector(`.nav-link[href="#${id}"]`);

        if (entry.isIntersecting) {
          navLinks.forEach(link => link.classList.remove('active'));
          if (navLink) navLink.classList.add('active');
        }
      });
    }, observerOptions);

    sections.forEach(section => observer.observe(section));
  }

  // Coming soon button interaction
  function handleComingSoon(event) {
    const btn = event.target;
    btn.textContent = 'NOTIFY ME';
    btn.style.background = 'var(--gsxr-accent-gradient)';
    alert('GSXR LAUNCHCTRL is in development. Stay tuned for launch updates!');
  }

  // Scroll to section
  function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  }

  // Initialize on DOM ready
  document.addEventListener('DOMContentLoaded', function() {
    // Respect reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    if (!prefersReducedMotion.matches) {
      cycleTerminalCommands();
    } else {
      // Show first command immediately without animation
      const typedCommand = document.getElementById('typedCommand');
      const commandOutput = document.getElementById('commandOutput');
      if (typedCommand) {
        typedCommand.textContent = terminalCommands[0];
      }
      if (commandOutput) {
        commandOutput.innerHTML = commandOutputs[terminalCommands[0]] || '';
      }
    }

    initSmoothScroll();
    initScrollSpy();
  });

  // Expose to global scope for inline handlers
  window.scrollToSection = scrollToSection;
  window.handleComingSoon = handleComingSoon;

})();
