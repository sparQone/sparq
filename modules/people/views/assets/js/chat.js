document.addEventListener('DOMContentLoaded', function() {
    // Initialize WebSocket connection
    const socket = io.connect(window.location.origin);
    let currentChannel = document.getElementById('current-channel').textContent;
    let showPinnedOnly = false;
    let channelToDelete = null;
    
    // Get current user ID from meta tag
    const userIdMeta = document.querySelector('meta[name="user-id"]');
    const currentUserId = userIdMeta ? parseInt(userIdMeta.content) : null;
    
    console.log('Current user ID:', currentUserId);
    console.log('Initial channel:', currentChannel);
    
    // Initialize delete channel modal
    const deleteChannelModal = new bootstrap.Modal(document.getElementById('deleteChannelModal'));
    const confirmDeleteChannelBtn = document.getElementById('confirmDeleteChannelBtn');
    
    // Function to show delete channel confirmation
    window.confirmDeleteChannel = function(channelName) {
        channelToDelete = channelName;
        deleteChannelModal.show();
    }
    
    // Handle channel deletion
    if (confirmDeleteChannelBtn) {
        confirmDeleteChannelBtn.addEventListener('click', function() {
            if (!channelToDelete) return;
            
            fetch(`/people/chat/channels/${channelToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(json => { throw new Error(json.error) });
                }
                return response.json();
            })
            .then(() => {
                // Remove channel from UI
                const channelElement = document.querySelector(`.channel[data-channel="${channelToDelete}"]`);
                if (channelElement) {
                    channelElement.remove();
                }
                
                // If we're in the deleted channel, switch to general
                if (currentChannel === channelToDelete) {
                    switchChannel('general');
                }
                
                // Close modal
                deleteChannelModal.hide();
                channelToDelete = null;
            })
            .catch(error => {
                alert('Error deleting channel: ' + error.message);
            });
        });
    }
    
    // Function to edit channel (placeholder for now)
    window.editChannel = function(channelName) {
        // TODO: Implement channel editing
        console.log('Edit channel:', channelName);
    }
    
    // Load initial messages
    loadChannelMessages(currentChannel);
    
    // Function to scroll chat to bottom
    function scrollToBottom() {
        const chatMessages = document.querySelector('.chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    // Function to update pin count
    function updatePinCount() {
        const pinCount = document.getElementById('pinCount');
        const pinnedMessages = document.querySelectorAll('.message.pinned');
        if (pinnedMessages.length > 0) {
            pinCount.textContent = pinnedMessages.length;
            pinCount.style.display = 'inline';
        } else {
            pinCount.style.display = 'none';
        }
    }

    // Function to toggle pin filter
    function togglePinFilter() {
        const pinFilter = document.getElementById('pinFilter');
        showPinnedOnly = !showPinnedOnly;
        pinFilter.classList.toggle('active', showPinnedOnly);
        
        document.querySelectorAll('.message').forEach(message => {
            if (showPinnedOnly) {
                message.style.display = message.classList.contains('pinned') ? 'flex' : 'none';
            } else {
                message.style.display = 'flex';
            }
        });
    }

    // Initialize pin filter button
    const pinFilter = document.getElementById('pinFilter');
    if (pinFilter) {
        pinFilter.addEventListener('click', togglePinFilter);
    }
    
    // Function to update unread badge
    function updateUnreadBadge(channelName, increment = true) {
        console.log('Updating badge for channel:', channelName, 'increment:', increment);
        const channelElement = document.querySelector(`.channel[data-channel="${channelName}"]`);
        if (!channelElement) {
            console.log('Channel element not found:', channelName);
            return;
        }

        let badge = channelElement.querySelector('.unread-badge');
        console.log('Existing badge:', badge);
        
        if (increment) {
            if (badge) {
                // Increment existing badge
                const count = parseInt(badge.textContent) + 1;
                badge.textContent = count;
                console.log('Incremented badge to:', count);
            } else {
                // Create new badge
                badge = document.createElement('span');
                badge.className = 'unread-badge';
                badge.textContent = '1';
                channelElement.appendChild(badge);
                console.log('Created new badge');
            }
        } else {
            // Remove badge when switching to channel
            if (badge) {
                badge.remove();
                console.log('Removed badge');
            }
        }
    }
    
    // Join default channel
    socket.emit('join', { channel: currentChannel });
    console.log('Joined channel:', currentChannel);
    
    // Channel switching
    window.switchChannel = function(channelName) {
        console.log('Switching to channel:', channelName);
        // Leave current channel
        socket.emit('leave', { channel: currentChannel });
        
        // Update UI
        document.querySelectorAll('.channel').forEach(ch => {
            ch.classList.remove('active');
            if (ch.dataset.channel === channelName) {
                ch.classList.add('active');
                // Update channel description if available
                if (ch.dataset.description) {
                    document.getElementById('channel-description').textContent = ch.dataset.description;
                }
            }
        });
        
        // Remove unread badge from new channel
        updateUnreadBadge(channelName, false);
        
        // Reset pin filter when switching channels
        showPinnedOnly = false;
        const pinFilter = document.getElementById('pinFilter');
        if (pinFilter) {
            pinFilter.classList.remove('active');
        }
        
        // Update current channel
        currentChannel = channelName;
        document.getElementById('current-channel').textContent = channelName;
        document.querySelector('.message-form textarea').placeholder = `Message in #${channelName}`;
        
        // Join new channel
        socket.emit('join', { channel: channelName });
        console.log('Joined new channel:', channelName);
        
        // Load channel messages
        loadChannelMessages(channelName);
    };

    // Function to load more messages
    window.loadMoreMessages = function(channelName, button) {
        const oldestId = button.dataset.oldestId;
        const url = `/people/chat/channels/${channelName}/messages?before_id=${oldestId}&limit=10`;
        
        // Show loading state
        button.disabled = true;
        const originalContent = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Loading...';
        
        // Get current scroll position and height before loading
        const chatMessages = document.querySelector('.chat-messages');
        const oldScrollHeight = chatMessages.scrollHeight;
        const oldScrollTop = chatMessages.scrollTop;
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(html => {
                // Remove the existing load more button
                button.closest('.load-more-container').remove();
                
                // Insert the new messages at the top
                chatMessages.insertAdjacentHTML('afterbegin', html);
                
                // Calculate and set new scroll position to maintain relative position
                const newScrollHeight = chatMessages.scrollHeight;
                chatMessages.scrollTop = newScrollHeight - oldScrollHeight + oldScrollTop;
                
                // Initialize new message actions
                initializeMessageActions();
                
                // Reinitialize tooltips for new messages
                const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
                tooltipTriggerList.map(function (tooltipTriggerEl) {
                    return new bootstrap.Tooltip(tooltipTriggerEl);
                });
            })
            .catch(error => {
                console.error('Error loading more messages:', error);
                button.disabled = false;
                button.innerHTML = originalContent;
                alert('Error loading more messages. Please try again.');
            });
    };

    // Function to load channel messages
    function loadChannelMessages(channelName) {
        const chatMessages = document.querySelector('.chat-messages');
        if (!chatMessages) return;

        const url = `/people/chat/channels/${channelName}/messages?limit=10`;
        
        // Show loading indicator
        chatMessages.innerHTML = '<div class="loading-indicator text-center p-4"><i class="fas fa-spinner fa-spin"></i> Loading messages...</div>';
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(html => {
                chatMessages.innerHTML = html;
                initializeMessageActions();
                updatePinCount();
                if (showPinnedOnly) {
                    document.querySelectorAll('.message').forEach(message => {
                        message.style.display = message.classList.contains('pinned') ? 'flex' : 'none';
                    });
                }
                scrollToBottom();
                
                // Reinitialize tooltips
                const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
                tooltipTriggerList.map(function (tooltipTriggerEl) {
                    return new bootstrap.Tooltip(tooltipTriggerEl);
                });
            })
            .catch(error => {
                console.error('Error loading messages:', error);
                chatMessages.innerHTML = '<div class="text-center p-4 text-danger">Error loading messages. Please try again.</div>';
            });
    }
    
    // New Channel Modal
    document.addEventListener('htmx:afterRequest', function(evt) {
        if (evt.detail.target.id === 'newChannelForm') {
            // Get the modal element
            const channelModal = document.getElementById('newChannelModal');
            // Retrieve the Bootstrap modal instance
            const modalInstance = bootstrap.Modal.getInstance(channelModal);
            
            if (modalInstance) {
                // Hide the modal
                modalInstance.hide();
                
                // Listen for the modal hidden event before disposing
                channelModal.addEventListener('hidden.bs.modal', function () {
                    modalInstance.dispose();
                }, { once: true });
            }
            
            // Optionally, reset the form fields
            evt.detail.target.reset();
        }
    });
    
    
    
    // Quick Message Form
    const quickMessageForm = document.getElementById('quickMessageForm');
    if (quickMessageForm) {
        quickMessageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            formData.append('channel', currentChannel);
            
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
                this.reset();
                scrollToBottom();
            })
            .catch(error => {
                alert('Error sending message: ' + error.message);
            });
        });
    }
    
    // WebSocket event handling
    socket.on('chat_changed', function(data) {
        //console.log('Received chat_changed event:', data);
        if (data.channel === currentChannel) {
            const chatMessages = document.querySelector('.chat-messages');
            if (chatMessages) {
                loadChannelMessages(currentChannel);
            }
        }
    });
    
    // Handle new messages for unread badges
    socket.on('message_created', function(data) {
        //console.log('Received message_created event:', data);
        // Only update badge if:
        // 1. We're not the author
        // 2. We're not currently viewing that channel
        if (data.author_id !== currentUserId && data.channel !== currentChannel) {
            console.log('Updating unread badge for channel:', data.channel);
            updateUnreadBadge(data.channel, true);
        } else if (data.channel === currentChannel) {
            scrollToBottom();
        }
    });
    
    socket.on('channel_created', function(data) {
        console.log('Channel created:', data.name);
    });
    
    socket.on('status', function(data) {
        // You can show join/leave messages if desired
        console.log(data.msg);
    });
    
    // Search functionality
    const searchInput = document.getElementById('chatSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            document.querySelectorAll('.message').forEach(message => {
                const content = message.querySelector('.message-content').textContent.toLowerCase();
                message.style.display = content.includes(searchTerm) ? 'flex' : 'none';
            });
        });
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize delete modal and message actions
    let deleteModal;
    let messageToDelete = null;

    function initializeMessageActions() {
        // Initialize delete modal
        const deleteModalElement = document.getElementById('deleteModal');
        if (deleteModalElement) {
            deleteModal = new bootstrap.Modal(deleteModalElement);
            
            // Handle confirm delete button click
            const confirmBtn = document.getElementById('confirmDeleteBtn');
            if (confirmBtn) {
                confirmBtn.addEventListener('click', function() {
                    if (!messageToDelete) return;

                    fetch(`/people/chat/${messageToDelete}`, {
                        method: 'DELETE'
                    })
                    .then(response => {
                        if (!response.ok) {
                            return response.json().then(json => { throw new Error(json.error) });
                        }
                        deleteModal.hide();
                        messageToDelete = null;
                        loadChannelMessages(currentChannel);  // Refresh messages after delete
                    })
                    .catch(error => {
                        alert('Error deleting message: ' + error.message);
                        deleteModal.hide();
                    });
                });
            }
        }

        // Handle all message actions using event delegation
        const chatMessages = document.querySelector('.chat-messages');
        if (chatMessages) {
            chatMessages.addEventListener('click', function(e) {
                const button = e.target.closest('.action-btn');
                if (!button) return;

                const action = button.dataset.action;
                const messageId = button.dataset.messageId;

                switch (action) {
                    case 'reply':
                        alert('Reply feature not implemented yet');
                        break;
                    case 'like':
                        alert('Like feature not implemented yet');
                        break;
                    case 'pin':
                        if (messageId) {
                            fetch(`/people/chat/${messageId}/pin`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            })
                            .then(response => {
                                if (!response.ok) {
                                    return response.json().then(json => { throw new Error(json.error) });
                                }
                                return response.json();
                            })
                            .then(() => {
                                loadChannelMessages(currentChannel);
                            })
                            .catch(error => {
                                alert('Error toggling pin: ' + error.message);
                            });
                        }
                        break;
                    case 'delete':
                        if (messageId && deleteModal) {
                            messageToDelete = messageId;
                            deleteModal.show();
                        }
                        break;
                }
            });
        }
    }

    // Initialize on page load
    initializeMessageActions();

    // Re-initialize after HTMX content swaps
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        if (evt.detail.target.classList.contains('chat-messages')) {
            initializeMessageActions();
            scrollToBottom();
        }
    });
}); 