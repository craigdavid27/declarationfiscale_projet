// Smooth scroll behavior
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

// Header scroll effect
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        header.style.boxShadow = '0 4px 6px -1px rgb(0 0 0 / 0.1)';
    } else {
        header.style.boxShadow = '0 1px 2px 0 rgb(0 0 0 / 0.05)';
    }
    
    lastScroll = currentScroll;
});

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.espace-card, .feature-card').forEach(card => {
    card.classList.add('animate-on-scroll');
    observer.observe(card);
});

// Button click animations
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
        // Create ripple effect
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
        
        // Alert message based on button
        const buttonText = this.textContent.trim();
        if (buttonText.includes('Comptables')) {
            showNotification('Redirection vers l\'espace Comptables...', 'info');
        } else if (buttonText.includes('Clients')) {
            showNotification('Redirection vers l\'espace Clients...', 'info');
        }
    });
});

// Add ripple effect styles dynamically
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .notification {
        position: fixed;
        top: 100px;
        right: 20px;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        z-index: 10000;
        animation: slideInRight 0.3s ease, slideOutRight 0.3s ease 2.7s;
        display: flex;
        align-items: center;
        gap: 1rem;
        min-width: 300px;
    }
    
    .notification.info {
        border-left: 4px solid #4F46E5;
    }
    
    .notification.success {
        border-left: 4px solid #10B981;
    }
    
    .notification-icon {
        font-size: 1.5rem;
    }
    
    .notification-message {
        color: #111827;
        font-weight: 500;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Notification function
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    const icon = type === 'info' ? 'ℹ️' : '✅';
    
    notification.innerHTML = `
        <span class="notification-icon">${icon}</span>
        <span class="notification-message">${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const hero = document.querySelector('.hero');
    const scrolled = window.pageYOffset;
    const rate = scrolled * 0.5;
    
    hero.style.transform = `translate3d(0, ${rate}px, 0)`;
});

// Animate feature icons
const featureIcons = document.querySelectorAll('.feature-card-icon');
featureIcons.forEach((icon, index) => {
    icon.style.animationDelay = `${index * 0.2}s`;
});

// Counter animation for stats (if needed in future)
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

// Active navigation link
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Add active class style
const activeStyle = document.createElement('style');
activeStyle.textContent = `
    .nav-link.active {
        color: #4F46E5;
    }
    
    .nav-link.active::after {
        width: 100%;
    }
`;
document.head.appendChild(activeStyle);

// Hover effect for feature list items
document.querySelectorAll('.features-list li').forEach(item => {
    item.addEventListener('mouseenter', function() {
        this.style.transform = 'translateX(10px)';
    });
    
    item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateX(0)';
    });
});

// Loading animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
});

// Add dynamic year to footer
const yearElement = document.querySelector('.footer-info p:last-child');
if (yearElement) {
    const currentYear = new Date().getFullYear();
    yearElement.textContent = yearElement.textContent.replace('2024', currentYear);
}

// Console welcome message
console.log('%c🎉 Bienvenue sur My Fisc!', 'color: #4F46E5; font-size: 20px; font-weight: bold;');
console.log('%cApplication de gestion fiscale professionnelle', 'color: #6B7280; font-size: 14px;');
