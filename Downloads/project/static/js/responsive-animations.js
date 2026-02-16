/* ===== RESPONSIVE & ANIMATION ENHANCEMENTS ===== */

(function() {
    'use strict';

    // ===== DEVICE DETECTION =====
    const isMobile = () => window.innerWidth < 768;
    const isTablet = () => window.innerWidth >= 768 && window.innerWidth < 1024;
    const isDesktop = () => window.innerWidth >= 1024;

    // ===== SMOOTH SCROLL =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ===== ANIMATION ON SCROLL =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observerCallback = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    // Observe cards and elements
    document.querySelectorAll(
        '.card, .feedback-card, .stat-card, .dashboard-card, .form-card, .alert'
    ).forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });

    // ===== RIPPLE EFFECT ON BUTTONS =====
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            // Prevent multiple ripples
            this.querySelectorAll('.ripple').forEach(r => r.remove());
            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // ===== STAR RATING ANIMATION =====
    document.querySelectorAll('.rating-option').forEach(option => {
        option.addEventListener('mouseenter', function() {
            const stars = this.querySelectorAll('.star-display i');
            stars.forEach((star, index) => {
                star.style.animation = `none`;
                setTimeout(() => {
                    star.style.animation = `bounce 0.6s ease-out ${index * 0.1}s`;
                }, 10);
            });
        });
    });

    // ===== FORM INPUT FOCUS ANIMATION =====
    document.querySelectorAll('.form-input, .form-select, .form-textarea').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement?.classList.add('focused');
            this.style.boxShadow = '0 0 0 3px rgba(79, 70, 229, 0.1)';
        });

        input.addEventListener('blur', function() {
            this.parentElement?.classList.remove('focused');
        });
    });

    // ===== COUNTER ANIMATION =====
    const animateCounter = (element, target, duration = 1000) => {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    };

    // Animate stat cards on load
    document.querySelectorAll('.stat-value').forEach(stat => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.textContent);
                    if (!isNaN(target)) {
                        animateCounter(entry.target, target, 1500);
                    }
                    observer.unobserve(entry.target);
                }
            });
        });
        observer.observe(stat);
    });

    // ===== MOBILE MENU TOGGLE =====
    const createMobileMenu = () => {
        const nav = document.querySelector('.navbar');
        const navMenu = document.querySelector('.nav-menu');

        if (!nav || !navMenu) return;

        const menuBtn = document.createElement('button');
        menuBtn.className = 'mobile-menu-btn';
        menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        menuBtn.style.cssText = `
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 10px;
            @media (max-width: 768px) {
                display: block;
            }
        `;

        menuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            const icon = menuBtn.querySelector('i');
            if (navMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        // Close menu when link is clicked
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                menuBtn.querySelector('i').classList.remove('fa-times');
                menuBtn.querySelector('i').classList.add('fa-bars');
            });
        });

        nav.querySelector('.nav-container').appendChild(menuBtn);
    };

    if (isMobile()) {
        createMobileMenu();
    }

    // ===== RESPONSIVE UPDATES ON RESIZE =====
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            if (isMobile()) {
                createMobileMenu();
            }
        }, 250);
    });

    // ===== LAZY LOAD IMAGES =====
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ===== ENHANCE TOUCH EXPERIENCE =====
    document.querySelectorAll('.btn, .feedback-card, .nav-link').forEach(el => {
        el.addEventListener('touchstart', function() {
            this.style.opacity = '0.9';
        });

        el.addEventListener('touchend', function() {
            this.style.opacity = '1';
        });
    });

    // ===== FORM VALIDATION WITH ANIMATION =====
    const validateForm = (form) => {
        let isValid = true;
        
        form.querySelectorAll('.form-input, .form-select, .form-textarea').forEach(input => {
            if (!input.value.trim() && input.required) {
                input.style.borderColor = '#EF4444';
                input.style.animation = 'shake 0.4s ease';
                isValid = false;

                setTimeout(() => {
                    input.style.animation = '';
                }, 400);
            }
        });

        return isValid;
    };

    // Add shake animation style
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            transform: scale(0);
            animation: rippleEffect 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes rippleEffect {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }

        @media (max-width: 768px) {
            .mobile-menu-btn {
                display: block !important;
            }
            
            .nav-menu {
                display: none;
            }
            
            .nav-menu.active {
                display: flex;
            }
        }
    `;
    document.head.appendChild(style);

    // ===== LOCAL STORAGE FOR ANIMATION PREFERENCES =====
    const reduceMotion = () => {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    };

    if (reduceMotion()) {
        document.body.style.setProperty('--animation-duration', '0.01ms');
    }

    // ===== PAGE LOAD COMPLETE ANIMATION =====
    window.addEventListener('load', () => {
        document.body.classList.add('page-loaded');
        
        // Add staggered animation to list items
        document.querySelectorAll('.feedback-row').forEach((row, index) => {
            row.style.animationDelay = `${index * 50}ms`;
        });
    });

    // ===== PERFORMANCE: DEBOUNCE SCROLL EVENTS =====
    let lastScrollTime = 0;
    window.addEventListener('scroll', () => {
        const now = Date.now();
        if (now - lastScrollTime > 150) {
            lastScrollTime = now;
            // Handle scroll-based animations here
        }
    }, { passive: true });

    // ===== ENHANCE ACCESSIBILITY =====
    document.querySelectorAll('.btn, .nav-link, .feedback-card').forEach(el => {
        el.setAttribute('role', 'button');
        el.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                this.click();
            }
        });
    });

    // ===== LOG DEVICE INFO (for testing) =====
    console.log(`Device Type: ${isDesktop() ? 'Desktop' : isTablet() ? 'Tablet' : 'Mobile'}`);
    console.log(`Screen: ${window.innerWidth}x${window.innerHeight}`);
    console.log(`User Agent: ${navigator.userAgent}`);

})();
