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

    // Search updates
    const searchInput = document.getElementById('updateSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            applyFilters();
        });
    }

    // Combined function to apply both search and type filters
    function applyFilters() {
        const searchText = document.getElementById('updateSearch').value.toLowerCase();
        const activeFilter = document.querySelector('.filter-buttons .btn.active').dataset.filter;
        
        document.querySelectorAll('.update-card').forEach(card => {
            const content = card.querySelector('.update-content').textContent.toLowerCase();
            const type = card.querySelector('.update-type').dataset.type; // Make sure this matches the data-type attribute
            
            const matchesSearch = content.includes(searchText);
            const matchesFilter = activeFilter === 'all' || type === activeFilter;
            
            card.style.display = matchesSearch && matchesFilter ? 'block' : 'none';
        });
    }

    // Apply filters before content is shown
    document.body.addEventListener('htmx:beforeSwap', function(evt) {
        const fragment = new DOMParser().parseFromString(evt.detail.serverResponse, 'text/html');
        const updates = fragment.querySelectorAll('.update-card');
        
        // Get current filter and search values
        const activeFilter = document.querySelector('.filter-buttons .btn.active').dataset.filter;
        const searchTerm = searchInput.value.toLowerCase();
        
        updates.forEach(update => {
            const content = update.querySelector('.update-content').textContent.toLowerCase();
            const author = update.querySelector('.author-name').textContent.toLowerCase();
            const updateType = update.dataset.type;
            
            const matchesSearch = content.includes(searchTerm) || author.includes(searchTerm);
            const matchesFilter = activeFilter === 'all' || updateType === activeFilter;

            update.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
        });
        
        evt.detail.serverResponse = fragment.body.innerHTML;
    });

    // Filter button click handler
    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            applyFilters();
        });
    });
}); 