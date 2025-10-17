// NutriHarvest Main JavaScript

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    try {
        initializeNavigation();
        initializeProductFeatures();
        initializeFormValidation();
        initializeNotifications();
        initializeScrollAnimations();
        initializeSystemNotifications();
        initializeNotificationBell();
    } catch (error) {
        console.error('Error initializing app:', error);
    }
}

// Debounce function for performance optimization
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Navigation functionality
function initializeNavigation() {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.navbar-toggler');
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            const navbarCollapse = document.querySelector('.navbar-collapse');
            navbarCollapse.classList.toggle('show');
        });
    }
    
    // Active nav link highlighting
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Smooth scrolling for anchor links
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

// Product-related functionality
function initializeProductFeatures() {
    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const quantity = this.dataset.quantity || 1;
            addToCart(productId, quantity);
        });
    });
    
    // Product image zoom
    const productImages = document.querySelectorAll('.product-image');
    productImages.forEach(image => {
        image.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        image.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Product quantity controls
    initializeQuantityControls();
    
    // Product search and filters
    initializeProductFilters();
}

// Cart functionality
function addToCart(productId, quantity = 1) {
    if (!isAuthenticated()) {
        showNotification('Please login to add items to cart', 'warning');
        window.location.href = '/login/';
        return;
    }
    
    const csrfToken = getCSRFToken();
    
    fetch('/api/orders/add-to-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: parseInt(quantity)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            updateCartCount(data.cart_count);
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred while adding to cart', 'error');
    });
}

function updateCart(cartItemId, quantity) {
    const csrfToken = getCSRFToken();
    
    fetch('/api/orders/update-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            cart_item_id: cartItemId,
            quantity: parseInt(quantity)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            if (quantity <= 0) {
                document.querySelector(`[data-cart-item="${cartItemId}"]`).remove();
            }
            updateCartTotals();
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred while updating cart', 'error');
    });
}

function removeFromCart(cartItemId) {
    const csrfToken = getCSRFToken();
    
    fetch('/api/orders/remove-from-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            cart_item_id: cartItemId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            document.querySelector(`[data-cart-item="${cartItemId}"]`).remove();
            updateCartTotals();
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred while removing item', 'error');
    });
}

// Quantity controls for product pages and cart
function initializeQuantityControls() {
    document.querySelectorAll('.quantity-control').forEach(control => {
        const minusBtn = control.querySelector('.quantity-minus');
        const plusBtn = control.querySelector('.quantity-plus');
        const input = control.querySelector('.quantity-input');
        
        if (minusBtn && plusBtn && input) {
            minusBtn.addEventListener('click', function() {
                const currentValue = parseInt(input.value);
                if (currentValue > 1) {
                    input.value = currentValue - 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
            
            plusBtn.addEventListener('click', function() {
                const currentValue = parseInt(input.value);
                const maxValue = parseInt(input.getAttribute('max')) || 999;
                if (currentValue < maxValue) {
                    input.value = currentValue + 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
            
            // Handle direct input changes
            input.addEventListener('change', function() {
                const cartItemId = this.dataset.cartItemId;
                if (cartItemId) {
                    updateCart(cartItemId, this.value);
                }
            });
        }
    });
}

// Product search and filtering
function initializeProductFilters() {
    const searchInput = document.querySelector('#product-search');
    const categoryFilter = document.querySelector('#category-filter');
    const priceFilter = document.querySelector('#price-filter');
    const sortSelect = document.querySelector('#sort-select');
    
    // Search functionality with debounce
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filterProducts();
            }, 300);
        });
    }
    
    // Filter change handlers
    [categoryFilter, priceFilter, sortSelect].forEach(element => {
        if (element) {
            element.addEventListener('change', filterProducts);
        }
    });
}

function filterProducts() {
    const searchTerm = document.querySelector('#product-search')?.value || '';
    const category = document.querySelector('#category-filter')?.value || '';
    const priceRange = document.querySelector('#price-filter')?.value || '';
    const sortBy = document.querySelector('#sort-select')?.value || '';
    
    const params = new URLSearchParams();
    if (searchTerm) params.append('search', searchTerm);
    if (category) params.append('category', category);
    if (priceRange) params.append('price_range', priceRange);
    if (sortBy) params.append('sort', sortBy);
    
    window.location.href = `/shop/?${params.toString()}`;
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Real-time validation for specific fields
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', validateEmail);
    });
    
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('blur', validatePassword);
    });
}

function validateEmail(event) {
    const input = event.target;
    const email = input.value;
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    
    if (!isValid && email.length > 0) {
        input.classList.add('is-invalid');
        showFieldError(input, 'Please enter a valid email address');
    } else {
        input.classList.remove('is-invalid');
        hideFieldError(input);
    }
}

function validatePassword(event) {
    const input = event.target;
    const password = input.value;
    
    if (password.length > 0 && password.length < 8) {
        input.classList.add('is-invalid');
        showFieldError(input, 'Password must be at least 8 characters long');
    } else {
        input.classList.remove('is-invalid');
        hideFieldError(input);
    }
}

function showFieldError(input, message) {
    let errorDiv = input.parentNode.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        input.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}

function hideFieldError(input) {
    const errorDiv = input.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Notifications system
function initializeNotifications() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 300);
        }, 5000);
    });
}

// System notifications
function initializeSystemNotifications() {
    // Fetch and display system notifications
    fetchSystemNotifications();
    
    // Check for new notifications every 5 minutes
    setInterval(fetchSystemNotifications, 5 * 60 * 1000);
}

function fetchSystemNotifications() {
    fetch('/api/notifications/system-notifications/')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.notifications.length > 0) {
                // Display each notification
                data.notifications.forEach(notification => {
                    showSystemNotification(notification);
                });
            }
        })
        .catch(error => {
            console.log('Failed to fetch system notifications:', error);
        });
}

function showSystemNotification(notification) {
    const container = document.getElementById('notification-popup-container');
    
    // Check if notification is already displayed
    if (document.getElementById(`system-notification-${notification.id}`)) {
        return;
    }
    
    const notificationElement = document.createElement('div');
    notificationElement.id = `system-notification-${notification.id}`;
    notificationElement.className = `alert alert-${getNotificationClass(notification.type)} alert-dismissible fade show mb-2`;
    notificationElement.style.minWidth = '300px';
    notificationElement.innerHTML = `
        <h6 class="alert-heading">${notification.title}</h6>
        <p class="mb-0">${notification.message}</p>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    container.appendChild(notificationElement);
    
    // Auto-hide after 10 seconds
    setTimeout(() => {
        if (notificationElement.parentNode) {
            notificationElement.style.opacity = '0';
            setTimeout(() => {
                if (notificationElement.parentNode) {
                    notificationElement.parentNode.removeChild(notificationElement);
                }
            }, 300);
        }
    }, 10000);
}

function getNotificationClass(type) {
    const typeMap = {
        'promotion': 'success',
        'new_arrival': 'info',
        'announcement': 'primary',
        'alert': 'warning'
    };
    return typeMap[type] || 'info';
}

// Notification bell functionality
function initializeNotificationBell() {
    const bell = document.getElementById('notificationBell');
    if (!bell) return;
    
    // Fetch user notifications
    fetchUserNotifications();
    
    // Update notification count periodically
    setInterval(fetchUserNotifications, 60 * 1000); // Every minute
}

function fetchUserNotifications() {
    // Only fetch if user is authenticated
    if (!isAuthenticated()) return;
    
    fetch('/api/notifications/user-notifications/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateNotificationBell(data.notifications);
            }
        })
        .catch(error => {
            console.log('Failed to fetch user notifications:', error);
        });
}

function updateNotificationBell(notifications) {
    const countElement = document.querySelector('.notification-count');
    const dropdownMenu = document.getElementById('notificationDropdown');
    const noNotificationsElement = document.getElementById('noNotifications');
    
    if (!countElement || !dropdownMenu) return;
    
    // Count unread notifications
    const unreadCount = notifications.filter(n => !n.is_read).length;
    
    // Update count badge
    countElement.textContent = unreadCount;
    countElement.style.display = unreadCount > 0 ? 'inline' : 'none';
    
    // Clear existing notifications in dropdown
    // Keep the header and divider
    const header = dropdownMenu.querySelector('.dropdown-header');
    const divider = dropdownMenu.querySelector('.dropdown-divider');
    
    // Remove all except header and divider
    while (dropdownMenu.children.length > 3) {
        dropdownMenu.removeChild(dropdownMenu.lastChild);
    }
    
    // Add notifications to dropdown
    if (notifications.length > 0) {
        noNotificationsElement.style.display = 'none';
        
        // Add up to 5 most recent notifications
        notifications.slice(0, 5).forEach(notification => {
            const notificationElement = document.createElement('li');
            notificationElement.innerHTML = `
                <a class="dropdown-item ${notification.is_read ? '' : 'bg-light'}" href="#">
                    <div class="d-flex justify-content-between">
                        <strong>${notification.title}</strong>
                        ${!notification.is_read ? '<span class="badge bg-danger badge-sm">New</span>' : ''}
                    </div>
                    <small class="text-muted">${notification.message.substring(0, 60)}${notification.message.length > 60 ? '...' : ''}</small>
                    <div class="small text-muted mt-1">${new Date(notification.created_at).toLocaleString()}</div>
                </a>
            `;
            dropdownMenu.appendChild(notificationElement);
        });
        
        // Add view all link
        if (notifications.length > 5) {
            const viewAllElement = document.createElement('li');
            viewAllElement.innerHTML = `
                <hr class="dropdown-divider">
                <a class="dropdown-item text-center" href="#">View all notifications</a>
            `;
            dropdownMenu.appendChild(viewAllElement);
        }
    } else {
        noNotificationsElement.style.display = 'block';
    }
}

function showNotification(message, type = 'info', duration = 5000) {
    const alertContainer = document.getElementById('alert-container') || document.body;
    
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type} alert-dismissible fade show`;
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertContainer.appendChild(alertElement);
    
    // Auto-hide after duration
    setTimeout(() => {
        alertElement.style.opacity = '0';
        setTimeout(() => {
            if (alertElement.parentNode) {
                alertElement.parentNode.removeChild(alertElement);
            }
        }, 300);
    }, duration);
}

// Scroll animations
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    document.querySelectorAll('.product-card, .feature-card, .testimonial-card, .dashboard-card').forEach(el => {
        observer.observe(el);
    });
}

// Utility functions
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
}

function isAuthenticated() {
    // Check if user is authenticated (you can customize this based on your implementation)
    return document.body.classList.contains('authenticated') ||
           document.querySelector('.user-menu') !== null;
}

function updateCartCount(count) {
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(element => {
        element.textContent = count;
        if (count > 0) {
            element.style.display = 'inline';
        }
    });
}

function updateCartTotals() {
    // Recalculate cart totals (implement based on your cart page structure)
    const cartItems = document.querySelectorAll('.cart-item');
    let total = 0;
    
    cartItems.forEach(item => {
        const price = parseFloat(item.dataset.price || '0');
        const quantity = parseInt(item.querySelector('.quantity-input')?.value || '0');
        total += price * quantity;
    });
    
    const totalElements = document.querySelectorAll('.cart-total');
    totalElements.forEach(element => {
        element.textContent = `$${total.toFixed(2)}`;
    });
}

// Newsletter subscription
function subscribeNewsletter(email) {
    const csrfToken = getCSRFToken();
    
    fetch('/api/cms/newsletter/subscribe/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            document.querySelector('#newsletter-email').value = '';
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred during subscription', 'error');
    });
}

// Initialize newsletter form if present
document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.querySelector('#newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.querySelector('#newsletter-email').value;
            if (email) {
                subscribeNewsletter(email);
            }
        });
    }
});

// Admin panel functionality
function initializeAdminFeatures() {
    // Bulk actions
    const bulkActionSelect = document.querySelector('#bulk-action');
    const bulkApplyBtn = document.querySelector('#bulk-apply');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    
    if (bulkApplyBtn && bulkActionSelect && itemCheckboxes.length > 0) {
        bulkApplyBtn.addEventListener('click', function() {
            const selectedAction = bulkActionSelect.value;
            const selectedItems = Array.from(itemCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.value);
            
            if (selectedAction && selectedItems.length > 0) {
                if (confirm(`Are you sure you want to ${selectedAction} ${selectedItems.length} item(s)?`)) {
                    // Implement bulk action
                    performBulkAction(selectedAction, selectedItems);
                }
            } else {
                showNotification('Please select items and an action', 'warning');
            }
        });
    }
    
    // Select all checkbox
    const selectAllCheckbox = document.querySelector('#select-all');
    if (selectAllCheckbox && itemCheckboxes.length > 0) {
        selectAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(cb => {
                cb.checked = this.checked;
            });
        });
    }
}

function performBulkAction(action, items) {
    // Implement bulk action logic based on the current page
    console.log(`Performing ${action} on items:`, items);
    // This would need to be implemented based on specific requirements
}

// Initialize admin features if on admin pages
if (document.body.classList.contains('admin-page')) {
    document.addEventListener('DOMContentLoaded', initializeAdminFeatures);
}