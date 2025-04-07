// Main JavaScript for BookngHotels

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Sticky Header
    initStickyHeader();
    
    // Initialize Back to Top Button
    initBackToTop();
    
    // Initialize Smooth Scroll
    initSmoothScroll();
    
    // Initialize Lazy Loading
    initLazyLoading();
    
    // Initialize Animations
    initAnimations();
});

// Sticky Header
function initStickyHeader() {
    const header = document.querySelector('.site-header');
    const headerHeight = header.offsetHeight;
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll <= headerHeight) {
            header.classList.remove('header-hidden');
            header.classList.remove('header-sticky');
            return;
        }
        
        if (currentScroll > lastScroll && currentScroll > headerHeight) {
            // Scrolling Down
            header.classList.add('header-hidden');
            header.classList.add('header-sticky');
        } else {
            // Scrolling Up
            header.classList.remove('header-hidden');
            header.classList.add('header-sticky');
        }
        
        lastScroll = currentScroll;
    });
}

// Back to Top Button
function initBackToTop() {
    const backToTop = document.querySelector('.back-to-top');
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });
    
    backToTop.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Smooth Scroll
function initSmoothScroll() {
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
}

// Lazy Loading
function initLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
}

// Animations
function initAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const elementObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(element => elementObserver.observe(element));
}

// Mobile Menu
function toggleMobileMenu() {
    const nav = document.querySelector('.main-nav');
    const menuButton = document.querySelector('.menu-toggle');
    
    menuButton.addEventListener('click', () => {
        nav.classList.toggle('active');
        menuButton.classList.toggle('active');
    });
}

// Testimonials Slider
class TestimonialsSlider {
    constructor(container) {
        this.container = container;
        this.slides = container.querySelectorAll('.testimonial-card');
        this.currentSlide = 0;
        this.autoplayInterval = null;
        
        this.init();
    }
    
    init() {
        this.showSlide(0);
        this.startAutoplay();
        this.bindEvents();
    }
    
    showSlide(index) {
        this.slides.forEach((slide, i) => {
            slide.style.display = i === index ? 'block' : 'none';
            slide.classList.toggle('active', i === index);
        });
    }
    
    nextSlide() {
        this.currentSlide = (this.currentSlide + 1) % this.slides.length;
        this.showSlide(this.currentSlide);
    }
    
    prevSlide() {
        this.currentSlide = (this.currentSlide - 1 + this.slides.length) % this.slides.length;
        this.showSlide(this.currentSlide);
    }
    
    startAutoplay() {
        this.autoplayInterval = setInterval(() => this.nextSlide(), 5000);
    }
    
    stopAutoplay() {
        clearInterval(this.autoplayInterval);
    }
    
    bindEvents() {
        this.container.addEventListener('mouseenter', () => this.stopAutoplay());
        this.container.addEventListener('mouseleave', () => this.startAutoplay());
    }
}

// Initialize Testimonials Slider
const testimonialsContainer = document.querySelector('.testimonials-slider');
if (testimonialsContainer) {
    new TestimonialsSlider(testimonialsContainer);
}

// Form Validation
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
    });
    
    return isValid;
}

// Newsletter Form
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm(this)) {
            // Submit form
            console.log('Newsletter form submitted');
        }
    });
} 