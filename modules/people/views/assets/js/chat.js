document.addEventListener('DOMContentLoaded', function() {
    // Initialize WebSocket connection with namespace
    const socket = io.connect(window.location.origin);
    
    // Modal handling
    const chatModal = document.getElementById('newChatModal');
    if (chatModal) {
        chatModal.addEventListener('shown.bs.modal', function() {
            document.querySelector('#content').focus();
        });
        
        chatModal.addEventListener('hidden.bs.modal', function() {
            const form = chatModal.querySelector('form');
            if (form) form.reset();
            document.querySelector('[data-bs-target="#newChatModal"]').focus();
        });
    }
    
    // Search functionality
    const searchInput = document.getElementById('chatSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            applyChatFilters();
        });
    }
    
    // Filter buttons
    const filterButtons = document.querySelectorAll('.filter-buttons button');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            applyChatFilters();
        });
    });
    
    // Filter function
    window.applyChatFilters = function() {
        const searchTerm = searchInput.value.toLowerCase();
        const activeFilter = document.querySelector('.filter-buttons button.active').dataset.filter;
        
        document.querySelectorAll('.chat-card').forEach(card => {
            const content = card.querySelector('.chat-content').textContent.toLowerCase();
            const type = card.dataset.type;
            
            const matchesSearch = content.includes(searchTerm);
            const matchesFilter = activeFilter === 'all' || type === activeFilter;
            
            card.style.display = matchesSearch && matchesFilter ? 'block' : 'none';
        });
    };
    
    // Handle quick message form submission
    const quickMessageForm = document.getElementById('quickMessageForm');
    if (quickMessageForm) {
        quickMessageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/people/chat/create', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => { throw new Error(text) });
                }
                return response.text();
            })
            .then(() => {
                // Clear the form
                this.reset();
            })
            .catch(error => {
                // Show error message
                alert('Error sending message: ' + error.message);
            });
        });
    }
    
    // WebSocket event handling
    socket.on('chat_changed', function() {
        // Refresh the chat list using HTMX
        htmx.trigger('.chat-messages', 'chat-refresh');
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    const newChatForm = document.getElementById('newChatForm');
    
    newChatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        fetch(this.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) });
            }
            return response.text();
        })
        .then(() => {
            // Success - close modal and clear form
            bootstrap.Modal.getInstance(document.getElementById('newChatModal')).hide();
            this.reset();
        })
        .catch(error => {
            // Show error message
            alert('Error creating message: ' + error.message);
        });
    });
}); 