// Initialize Chart
const ctx = document.getElementById('declarationsChart');
if (ctx) {
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
            datasets: [
                {
                    label: 'Alimentation et batterie',
                    data: [45, 52, 48, 60, 55, 68],
                    borderColor: '#F97316',
                    backgroundColor: 'rgba(249, 115, 22, 0.05)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointBackgroundColor: '#F97316',
                    pointBorderColor: '#FFFFFF',
                    pointBorderWidth: 2,
                    pointHoverRadius: 8,
                    borderCapStyle: 'round'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            weight: '500'
                        },
                        color: '#6B7280'
                    }
                },
                tooltip: {
                    backgroundColor: '#FFFFFF',
                    titleColor: '#111827',
                    bodyColor: '#6B7280',
                    borderColor: '#E5E7EB',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        afterLabel: function(context) {
                            return context.formattedValue + ' déclarations';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 80,
                    grid: {
                        color: '#E5E7EB',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6B7280',
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6B7280',
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
}

// Animate progress bars on scroll
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            if (entry.target.classList.contains('progress-fill')) {
                const width = entry.target.style.width;
                entry.target.style.width = '0';
                setTimeout(() => {
                    entry.target.style.width = width;
                }, 100);
            }
            
            if (entry.target.classList.contains('stat-card')) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    entry.target.style.transition = 'all 0.5s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
            }
        }
    });
}, observerOptions);

document.querySelectorAll('.progress-fill').forEach(el => observer.observe(el));
document.querySelectorAll('.stat-card').forEach(el => observer.observe(el));

// Action buttons interactions
document.querySelectorAll('.action-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const action = this.getAttribute('title');
        showActionNotification(action);
    });
});

// Action cards click
document.querySelectorAll('.action-card').forEach(card => {
    card.addEventListener('click', function() {
        const title = this.querySelector('h3').textContent;
        showActionNotification(`Accès à "${title}"`);
    });
});

function showActionNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
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
        border-left: 4px solid #4F46E5;
    `;
    
    notification.innerHTML = `
        <span style="font-size: 1.5rem;">ℹ️</span>
        <span style="color: #111827; font-weight: 500;">${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Stat cards animation on load
window.addEventListener('load', () => {
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// Responsive table scroll on mobile
const tableWrapper = document.querySelector('.table-wrapper');
if (tableWrapper && window.innerWidth < 768) {
    tableWrapper.addEventListener('scroll', function() {
        const isScrolled = this.scrollLeft > 0;
        const table = this.querySelector('.clients-table');
        if (isScrolled) {
            table.style.boxShadow = 'inset 10px 0 10px -5px rgba(0, 0, 0, 0.1)';
        } else {
            table.style.boxShadow = 'none';
        }
    });
}

// Stats counter animation
function animateCounter(element, targetValue, duration = 1000) {
    const startValue = 0;
    const startTime = Date.now();
    
    const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const currentValue = Math.floor(startValue + (targetValue - startValue) * progress);
        
        element.textContent = currentValue;
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    };
    
    animate();
}

// Animate stat numbers on scroll
const statNumbers = document.querySelectorAll('.stat-number');
let hasAnimated = false;

const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !hasAnimated) {
            hasAnimated = true;
            statNumbers.forEach(number => {
                const targetValue = parseInt(number.textContent);
                if (!isNaN(targetValue)) {
                    animateCounter(number, targetValue, 1500);
                }
            });
        }
    });
}, { threshold: 0.5 });

document.querySelector('.stats-grid') && statsObserver.observe(document.querySelector('.stats-grid'));

// Add styles for animations
const style = document.createElement('style');
style.textContent = `
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

// Console message
console.log('%c🎉 Dashboard Comptable chargé!', 'color: #4F46E5; font-size: 16px; font-weight: bold;');
console.log('%cBienvenue dans l\'espace comptable My Fisc', 'color: #6B7280; font-size: 12px;');
