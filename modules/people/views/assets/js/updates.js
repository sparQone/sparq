// Updates.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });

    // Handle not implemented features
    document.addEventListener('click', function(e) {
        if (e.target.closest('.not-implemented')) {
            // Create the toast element first
            const toastElement = document.createElement('div');
            toastElement.className = 'toast align-items-center text-white bg-secondary';
            toastElement.role = 'alert';
            toastElement.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas fa-tools"></i> This feature is not implemented yet
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            `;
            
            // Append the element first
            document.body.appendChild(toastElement);
            
            // Then create the Toast instance with auto-hide
            const toast = new bootstrap.Toast(toastElement, {
                delay: 1500  // Auto-hide after 1.5 seconds
            });
            toast.show();
            
            // Remove element after it's hidden
            toastElement.addEventListener('hidden.bs.toast', () => {
                toastElement.remove();
            });
            
            e.preventDefault();
            return false;
        }
    });

    // Filter updates
    const filterButtons = document.querySelectorAll('.filter-buttons .btn');

    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Update active state
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Apply filter
            applyCurrentFilter();
        });
    });

    // Function to apply current filter
    function applyCurrentFilter() {
        const activeFilter = document.querySelector('.filter-buttons .btn.active').dataset.filter;
        const updates = document.querySelectorAll('.update-card');
        
        updates.forEach(update => {
            const updateType = update.dataset.type;
            if (activeFilter === 'all' || updateType === activeFilter) {
                update.style.display = '';
            } else {
                update.style.display = 'none';
            }
        });
    }

    // Apply filter before content is shown
    document.body.addEventListener('htmx:beforeSwap', function(evt) {
        const fragment = new DOMParser().parseFromString(evt.detail.serverResponse, 'text/html');
        const updates = fragment.querySelectorAll('.update-card');
        const activeFilter = document.querySelector('.filter-buttons .btn.active').dataset.filter;
        
        updates.forEach(update => {
            const updateType = update.dataset.type;
            if (activeFilter === 'all' || updateType === activeFilter) {
                update.style.display = '';
            } else {
                update.style.display = 'none';
            }
        });
        
        evt.detail.serverResponse = fragment.body.innerHTML;
    });

    // Search updates
    const searchInput = document.getElementById('updateSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const updates = document.querySelectorAll('.update-card');
            const activeFilter = document.querySelector('.filter-buttons .btn.active').dataset.filter;

            updates.forEach(update => {
                const content = update.querySelector('.update-content').textContent.toLowerCase();
                const author = update.querySelector('.author-name').textContent.toLowerCase();
                const matchesSearch = content.includes(searchTerm) || author.includes(searchTerm);
                const matchesFilter = activeFilter === 'all' || update.dataset.type === activeFilter;

                update.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
            });
        });
    }
}); 