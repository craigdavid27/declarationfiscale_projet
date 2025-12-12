// Particulier Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Animate progress circle on page load
    animateProgressCircle();
    
    // Add interactivity to nav items
    initializeNavigation();
});

/**
 * Animate the progress circle SVG
 */
function animateProgressCircle() {
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
        // Get the circumference
        const circle = progressFill.parentElement.querySelector('.progress-circle');
        const radius = 54;
        const circumference = 2 * Math.PI * radius;
        
        // Set initial state
        progressFill.style.strokeDasharray = circumference;
        progressFill.style.strokeDashoffset = circumference;
        
        // Animate to 35%
        setTimeout(() => {
            const offset = circumference - (circumference * 0.35);
            progressFill.style.transition = 'stroke-dashoffset 1s ease-in-out';
            progressFill.style.strokeDashoffset = offset;
        }, 100);
    }
}

/**
 * Initialize navigation items click handlers
 */
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            const isPlaceholder = !href || href.trim() === '' || href.trim() === '#';

            // Empêche uniquement la navigation pour les liens de type placeholder (#)
            if (isPlaceholder) {
                e.preventDefault();
            }

            const span = this.querySelector('span');
            const section = span ? span.textContent.trim() : this.textContent.trim();
            console.log('Navigating to:', section);
        });
    });
}

/**
 * Update progress circle based on completion percentage
 * @param {number} percentage - Completion percentage (0-100)
 */
function updateProgress(percentage) {
    const progressFill = document.querySelector('.progress-fill');
    const progressPercentage = document.querySelector('.progress-percentage');
    
    if (progressFill && progressPercentage) {
        const circle = progressFill.parentElement.querySelector('.progress-circle');
        const radius = 54;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (circumference * (percentage / 100));
        
        progressFill.style.strokeDashoffset = offset;
        progressPercentage.textContent = percentage + '%';
    }
}

/**
 * Add ripple effect to nav cards on click
 */
function addRippleEffect() {
    const navCards = document.querySelectorAll('.nav-card');
    
    navCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.closest('.nav-item')) {
                const ripple = document.createElement('span');
                ripple.classList.add('ripple');
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            }
        });
    });
}

// Call ripple effect initialization
document.addEventListener('DOMContentLoaded', addRippleEffect);
