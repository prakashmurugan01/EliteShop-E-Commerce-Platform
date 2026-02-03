/* ================================ */
/* STATIC/JS/SCRIPT.JS */
/* ================================ */

// ====== UTILITY FUNCTIONS ======
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

// ====== INITIALIZE ON LOAD ======
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    setupSearchSuggestions();
    setupTooltips();
});

// ====== CART FUNCTIONS ======
function updateCartCount() {
    fetch('/cart/count/')
        .then(res => res.json())
        .then(data => {
            const cartCount = document.getElementById('cartCount');
            if (data.count > 0) {
                cartCount.textContent = data.count;
                cartCount.style.display = 'inline-block';
            } else {
                cartCount.style.display = 'none';
            }
        })
        .catch(err => console.log('Cart count error:', err));
}

// ====== SEARCH SUGGESTIONS ======
function setupSearchSuggestions() {
    const searchInput = document.getElementById('searchInput');
    const suggestionsDiv = document.getElementById('searchSuggestions');
    
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function(e) {
        const query = this.value.trim();
        
        if (query.length < 2) {
            suggestionsDiv.style.display = 'none';
            return;
        }
        
        fetch(`/search-suggestions/?q=${query}`)
            .then(res => res.json())
            .then(suggestions => {
                if (suggestions.length > 0) {
                    suggestionsDiv.innerHTML = '';
                    
                    suggestions.forEach(product => {
                        const link = document.createElement('a');
                        link.href = `/product/${product.slug}/`;
                        link.className = 'dropdown-item';
                        link.textContent = product.name;
                        suggestionsDiv.appendChild(link);
                    });
                    
                    suggestionsDiv.style.display = 'block';
                } else {
                    suggestionsDiv.innerHTML = '<div class="dropdown-item">No products found</div>';
                    suggestionsDiv.style.display = 'block';
                }
            })
            .catch(err => console.log('Search error:', err));
    });
    
    // Close on blur
    searchInput.addEventListener('blur', function() {
        setTimeout(() => {
            suggestionsDiv.style.display = 'none';
        }, 200);
    });
}

// ====== TOOLTIPS ======
function setupTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ====== NOTIFICATION ======
function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertAdjacentElement('beforebegin', alertDiv);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
}

// ====== QUANTITY CONTROLS ======
function setupQuantityControls(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const decreaseBtn = container.querySelector('[data-action="decrease"]');
    const increaseBtn = container.querySelector('[data-action="increase"]');
    const input = container.querySelector('input[name="quantity"]');
    
    if (!decreaseBtn || !increaseBtn || !input) return;
    
    const maxQty = parseInt(input.getAttribute('max')) || 100;
    
    decreaseBtn.addEventListener('click', () => {
        if (input.value > 1) {
            input.value = parseInt(input.value) - 1;
            input.dispatchEvent(new Event('change'));
        }
    });
    
    increaseBtn.addEventListener('click', () => {
        if (input.value < maxQty) {
            input.value = parseInt(input.value) + 1;
            input.dispatchEvent(new Event('change'));
        }
    });
}

// ====== DELETE CONFIRMATION ======
function confirmDelete(message = 'Are you sure?', callback) {
    Swal.fire({
        title: 'Confirm Delete',
        text: message,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Yes, delete it!'
    }).then(result => {
        if (result.isConfirmed) {
            callback();
        }
    });
}

// ====== FORM VALIDATION ======
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]{10,}$/;
    return re.test(phone.replace(/\s/g, ''));
}

// ====== PRODUCT FILTERS ======
function applyFilters() {
    const category = document.getElementById('categoryFilter')?.value;
    const sort = document.getElementById('sortFilter')?.value;
    const search = document.getElementById('searchFilter')?.value;
    
    let url = '/products/?';
    
    if (category) url += `category=${category}&`;
    if (sort) url += `sort=${sort}&`;
    if (search) url += `search=${search}&`;
    
    window.location.href = url;
}

// ====== PRICE FORMATTER ======
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

// ====== SORT PRODUCTS ======
function sortProducts(sortBy) {
    const url = new URL(window.location);
    url.searchParams.set('sort', sortBy);
    window.location.href = url.toString();
}

// ====== IMAGE PREVIEW ======
function previewImage(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    
    if (!input || !preview) return;
    
    input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                preview.src = event.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
}

// ====== COPY TO CLIPBOARD ======
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy', 'error');
    });
}

// ====== DEBOUNCE FUNCTION ======
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// ====== LAZY LOADING IMAGES ======
function setupLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
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
}

// ====== PARALLAX EFFECT ======
function setupParallax() {
    window.addEventListener('scroll', function() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.parallax || 0.5;
            const yPos = window.pageYOffset * speed;
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// ====== ADMIN FUNCTIONS ======
function deleteProduct(productId) {
    confirmDelete('This will permanently delete the product.', function() {
        fetch(`/admin-panel/products/delete/${productId}/`, {
            method: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')}
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showNotification('Product deleted successfully', 'success');
                setTimeout(() => location.reload(), 1000);
            }
        });
    });
}

function deleteCategory(categoryId) {
    confirmDelete('This will permanently delete the category.', function() {
        fetch(`/admin-panel/categories/delete/${categoryId}/`, {
            method: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')}
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showNotification('Category deleted successfully', 'success');
                setTimeout(() => location.reload(), 1000);
            }
        });
    });
}

function deleteCoupon(couponId) {
    confirmDelete('This will permanently delete the coupon.', function() {
        fetch(`/admin-panel/coupons/delete/${couponId}/`, {
            method: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')}
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showNotification('Coupon deleted successfully', 'success');
                setTimeout(() => location.reload(), 1000);
            }
        });
    });
}

// ====== SMOOTH SCROLL ======
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

// ====== LOADING STATE ======
function setLoading(elementId, isLoading) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    if (isLoading) {
        element.disabled = true;
        element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    } else {
        element.disabled = false;
        element.innerHTML = element.dataset.originalText || 'Submit';
    }
}

// ====== NUMBER FORMATTING ======
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// ====== DATE FORMATTING ======
function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

console.log('EliteShop - Script loaded successfully');
