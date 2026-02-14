/**
 * Toast Notification System
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle',
        warning: 'fas fa-exclamation-triangle'
    };

    toast.innerHTML = `
        <i class="${icons[type] || icons.info}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    const duration = type === 'error' ? 5000 : 3000;
    setTimeout(() => {
        toast.classList.add('removing');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

/**
 * Form Validation Helpers
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhoneNumber(phone) {
    const re = /^[0-9\-\+\(\)\s]{10,}$/;
    return re.test(phone);
}

/**
 * Initialize Event Listeners
 */
document.addEventListener('DOMContentLoaded', function() {
    // Form submission handling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                submitButton.disabled = true;
                submitButton.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Processing...`;
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });

    // Add active class to current nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href)) {
            link.classList.add('active');
        }
    });

    // Initialize tooltips if available
    initializeTooltips();
});

/**
 * Tooltip System
 */
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = e.target.getAttribute('data-tooltip');
    document.body.appendChild(tooltip);

    const rect = e.target.getBoundingClientRect();
    tooltip.style.position = 'fixed';
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
    tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
    tooltip.style.zIndex = '10000';
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

/**
 * Local Storage Helper
 */
const LocalStorage = {
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    },

    get(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return null;
        }
    },

    remove(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Error removing from localStorage:', error);
        }
    },

    clear() {
        try {
            localStorage.clear();
        } catch (error) {
            console.error('Error clearing localStorage:', error);
        }
    }
};

/**
 * API Helper
 */
async function fetchAPI(endpoint, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    };

    const finalOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(endpoint, finalOptions);
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

/**
 * CSRF Token Helper
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Debounce Function
 */
function debounce(func, delay = 300) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * Throttle Function
 */
function throttle(func, limit = 300) {
    let lastFunc;
    let lastRan;
    return function(...args) {
        if (!lastRan) {
            func.apply(this, args);
            lastRan = Date.now();
        } else {
            clearTimeout(lastFunc);
            lastFunc = setTimeout(function() {
                if ((Date.now() - lastRan) >= limit) {
                    func.apply(this, args);
                    lastRan = Date.now();
                }
            }, limit - (Date.now() - lastRan));
        }
    };
}

/**
 * Format Date
 */
function formatDate(date, format = 'short') {
    const d = new Date(date);
    const options = {
        short: { year: 'numeric', month: 'short', day: 'numeric' },
        long: { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' },
        time: { hour: '2-digit', minute: '2-digit', second: '2-digit' }
    };
    return d.toLocaleDateString('en-US', options[format] || options.short);
}

/**
 * Keyboard Shortcuts
 */
const KeyboardShortcuts = {
    register(key, callback) {
        document.addEventListener('keydown', (e) => {
            if (e.key === key) {
                callback();
            }
        });
    },

    registerCombo(keys, callback) {
        const pressed = new Set();
        document.addEventListener('keydown', (e) => {
            pressed.add(e.key);
            if (keys.every(k => pressed.has(k))) {
                callback();
                pressed.clear();
            }
        });
        document.addEventListener('keyup', (e) => {
            pressed.delete(e.key);
        });
    }
};

/**
 * Loading Spinner
 */
function showLoading(message = 'Loading...') {
    const spinner = document.createElement('div');
    spinner.id = 'global-loader';
    spinner.innerHTML = `
        <div class="loader-content">
            <i class="fas fa-spinner fa-spin"></i>
            <p>${message}</p>
        </div>
    `;
    spinner.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;
    document.body.appendChild(spinner);
}

function hideLoading() {
    const loader = document.getElementById('global-loader');
    if (loader) {
        loader.remove();
    }
}

/**
 * Page Transition Effects
 */
function fadeOutPage() {
    const main = document.querySelector('.main-content');
    if (main) {
        main.style.opacity = '0';
        main.style.transition = 'opacity 0.3s ease-out';
    }
}

/**
 * Dark Mode Support (Optional)
 */
const DarkMode = {
    enable() {
        document.documentElement.style.colorScheme = 'dark';
        LocalStorage.set('darkMode', true);
    },

    disable() {
        document.documentElement.style.colorScheme = 'light';
        LocalStorage.set('darkMode', false);
    },

    toggle() {
        const isDark = LocalStorage.get('darkMode');
        if (isDark) {
            this.disable();
        } else {
            this.enable();
        }
    },

    init() {
        const isDark = LocalStorage.get('darkMode');
        if (isDark) {
            this.enable();
        }
    }
};

// Export for use in other scripts
window.APP = {
    showToast,
    validateEmail,
    validatePhoneNumber,
    LocalStorage,
    fetchAPI,
    getCookie,
    debounce,
    throttle,
    formatDate,
    KeyboardShortcuts,
    showLoading,
    hideLoading,
    fadeOutPage,
    DarkMode
};
