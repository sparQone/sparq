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
    
    // Initialize unread indicators
    initializeUnreadIndicators();
    
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
                // Check if there's content to parse
                if (response.status === 204) {
                    return {}; // Return empty object for 204 No Content
                }
                return response.json().catch(() => ({})); // Handle empty responses
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
    
    // Function to edit channel
    window.editChannel = function(channelName, description) {
        // Populate the edit form
        const originalNameInput = document.getElementById('originalChannelName');
        const nameInput = document.getElementById('editChannelName');
        const descriptionInput = document.getElementById('editChannelDescription');
        
        // Set values
        originalNameInput.value = channelName;
        nameInput.value = channelName;
        descriptionInput.value = description || '';
        
        // Show the modal
        const editModal = new bootstrap.Modal(document.getElementById('editChannelModal'));
        editModal.show();
    }
    
    // Handle edit form submission
    const editChannelForm = document.getElementById('editChannelForm');
    if (editChannelForm) {
        editChannelForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const originalName = formData.get('original_channel_name');
            
            // Submit without client-side validation
            fetch('/people/chat/channels/edit', {
                method: 'PUT',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(json => { throw new Error(json.error) });
                }
                return response.json();
            })
            .then(response => {
                // Get the channel element
                const channelElement = document.querySelector(`.channel[data-channel="${originalName}"]`);
                
                if (channelElement) {
                    // Update channel attributes
                    channelElement.dataset.channel = response.name;
                    channelElement.dataset.description = response.description || '';
                    channelElement.setAttribute('onclick', `switchChannel('${response.name}')`);
                    
                    // Update channel name in the UI
                    const nameElement = channelElement.querySelector('.text-truncate');
                    if (nameElement) {
                        nameElement.innerHTML = `<span class="channel-prefix">#</span> ${response.name}`;
                    }
                    
                    // Update dropdown menu actions
                    const dropdownItems = channelElement.querySelectorAll('.dropdown-item');
                    dropdownItems.forEach(item => {
                        if (item.innerHTML.includes('fa-edit')) {
                            item.setAttribute('data-channel-name', response.name);
                            item.setAttribute('data-channel-description', response.description || '');
                            item.setAttribute('onclick', `event.stopPropagation(); editChannel(this.getAttribute('data-channel-name'), this.getAttribute('data-channel-description'));`);
                        } else if (item.innerHTML.includes('fa-trash')) {
                            item.setAttribute('onclick', `event.stopPropagation(); confirmDeleteChannel('${response.name}');`);
                        }
                    });
                    
                    // If this is the current channel, update the header
                    if (currentChannel === originalName) {
                        document.getElementById('current-channel').textContent = response.name;
                        document.getElementById('channel-description').textContent = response.description || '';
                        currentChannel = response.name;
                        
                        // Update pin filter URL
                        const pinFilter = document.querySelector('.pin-filter');
                        if (pinFilter) {
                            pinFilter.setAttribute('hx-get', `/people/chat/channels/${response.name}/messages`);
                        }
                        
                        // Update search endpoint
                        const searchInput = document.getElementById('chatSearch');
                        if (searchInput) {
                            searchInput.setAttribute('hx-post', `/people/chat/channels/${response.name}/search`);
                        }
                    }
                }
                
                // Close the modal
                const editModal = bootstrap.Modal.getInstance(document.getElementById('editChannelModal'));
                if (editModal) {
                    editModal.hide();
                }
            })
            .catch(error => {
                alert('Error updating channel: ' + error.message);
            });
        });
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
    function updatePinCount(count) {
        const pinCount = document.getElementById('pinCount');
        const pinCountHidden = document.getElementById('pinCountHidden');
        
        if (pinCount) {
            pinCount.textContent = count;
            pinCount.style.display = count > 0 ? 'inline' : 'none';
        }
        
        if (pinCountHidden) {
            pinCountHidden.value = count;
        }
    }

    // Listen for pin count updates
    document.addEventListener('updatePinCount', function(evt) {
        updatePinCount(evt.detail.count);
    });

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
    
    // Function to update unread indicator
    function updateUnreadIndicator(channelName, hasUnread = true) {
        console.log(`Updating unread indicator for channel ${channelName}: ${hasUnread}`);
        const channelNameElement = document.getElementById(`channel-name-${channelName}`);
        if (!channelNameElement) {
            console.error(`Channel element not found for ${channelName}`);
            return;
        }

        if (hasUnread) {
            console.log(`Marking channel ${channelName} as unread`);
            channelNameElement.classList.add('fw-bold');
            channelNameElement.style.opacity = '1';
        } else {
            console.log(`Marking channel ${channelName} as read`);
            channelNameElement.classList.remove('fw-bold');
            channelNameElement.style.opacity = '0.75';
        }
    }
    
    // Initialize unread indicators
    function initializeUnreadIndicators() {
        console.log('Initializing unread indicators...');
        // Fetch unread status for all channels
        fetch('/people/chat/channels/unread')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Received unread status:', data);
                // Update unread indicators based on server response
                for (const channelName in data) {
                    console.log(`Channel ${channelName} unread status: ${data[channelName]}`);
                    updateUnreadIndicator(channelName, data[channelName]);
                }
            })
            .catch(error => {
                console.error('Error fetching unread status:', error);
            });
    }
    
    // Join default channel
    socket.emit('join', { channel: currentChannel });
    console.log('Joined channel:', currentChannel);
    
    // Channel switching
    window.switchChannel = function(channelName) {
        console.log(`Switching to channel: ${channelName}`);
        
        // Update current channel display
        document.getElementById('current-channel').textContent = channelName;
        currentChannel = channelName;
        
        // Update channel description
        const channelElement = document.querySelector(`.channel[data-channel="${channelName}"]`);
        if (channelElement) {
            const description = channelElement.getAttribute('data-description');
            document.getElementById('channel-description').textContent = description;
            
            // Update active state
            document.querySelectorAll('.channel').forEach(el => el.classList.remove('active'));
            channelElement.classList.add('active');
            
            // Remove unread indicator from new channel
            updateUnreadIndicator(channelName, false);
            
            // Mark channel as read on the server
            console.log(`Marking channel ${channelName} as read on the server`);
            fetch(`/people/chat/channels/${channelName}/mark_read`, {
                method: 'POST'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(`Successfully marked channel ${channelName} as read:`, data);
            })
            .catch(error => {
                console.error(`Error marking channel ${channelName} as read:`, error);
            });
        }
        
        // Preserve search input value
        const searchValue = document.getElementById('chatSearch').value;
        
        // Update pin filter URL
        const pinFilter = document.querySelector('.pin-filter');
        if (pinFilter) {
            pinFilter.setAttribute('hx-get', `/people/chat/channels/${channelName}/messages`);
            pinFilter.classList.remove('text-primary');
        }
        
        // Load messages for the new channel
        htmx.ajax('GET', `/people/chat/channels/${channelName}/messages`, {target: '.chat-messages'})
            .then(() => {
                // Restore search input value after channel switch
                document.getElementById('chatSearch').value = searchValue;
                
                // Update search endpoint
                const searchInput = document.getElementById('chatSearch');
                if (searchInput) {
                    searchInput.setAttribute('hx-post', `/people/chat/channels/${channelName}/search`);
                }
                
                // Join the new channel via WebSocket
                socket.emit('join', {channel: channelName});
            });
    };

    // Function to load more messages
    window.loadMoreMessages = function(channelName, button) {
        const oldestId = button.dataset.oldestId;
        const url = `/people/chat/channels/${channelName}/messages?before_id=${oldestId}`;
        
        fetch(url)
            .then(response => response.text())
            .then(html => {
                // Remove the old "Load More" button
                button.closest('.load-more-container').remove();
                
                // Insert the new content at the top
                const chatMessages = document.querySelector('.chat-messages');
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = html;
                
                // Get all the new messages
                const newMessages = Array.from(tempDiv.children);
                
                // Insert each new message at the top, maintaining order
                newMessages.reverse().forEach(message => {
                    if (!message.classList || !message.classList.contains('load-more-container')) {
                        chatMessages.insertBefore(message, chatMessages.firstChild);
                    }
                });
                
                // If there's a new "Load More" button, move it to the top
                const newLoadMoreBtn = tempDiv.querySelector('.load-more-container');
                if (newLoadMoreBtn) {
                    chatMessages.insertBefore(newLoadMoreBtn, chatMessages.firstChild);
                }
                
                // Initialize tooltips for new messages
                const tooltips = chatMessages.querySelectorAll('[data-bs-toggle="tooltip"]');
                tooltips.forEach(el => new bootstrap.Tooltip(el));
                
                // Reinitialize HTMX for the new content
                htmx.process(chatMessages);
            })
            .catch(error => {
                console.error('Error loading more messages:', error);
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
                
                // Process any HTMX attributes in the new content
                htmx.process(chatMessages);
                
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
            if (evt.detail.successful) {
                try {
                    const response = JSON.parse(evt.detail.xhr.response);
                    
                    // Create new channel element
                    const channelList = document.querySelector('.channel-list');
                    const newChannel = document.createElement('div');
                    newChannel.className = 'channel d-flex align-items-center justify-content-between p-2 mx-2 rounded-1 cursor-pointer text-white';
                    newChannel.dataset.channel = response.name;
                    newChannel.dataset.description = response.description || '';
                    newChannel.setAttribute('onclick', `switchChannel('${response.name}')`);
                    
                    newChannel.innerHTML = `
                        <div class="d-flex align-items-center flex-grow-1 min-w-0">
                            <div class="text-truncate opacity-75" id="channel-name-${response.name}">
                                <span class="channel-prefix">#</span> ${response.name}
                            </div>
                        </div>
                        <div class="dropdown channel-actions opacity-0" onclick="event.stopPropagation();">
                            <button class="btn btn-link btn-sm text-white p-0 opacity-75" 
                                    data-bs-toggle="dropdown"
                                    aria-expanded="false"
                                    title="Channel options">
                                <i class="fas fa-ellipsis-v"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li>
                                    <a class="dropdown-item" href="#" 
                                       data-channel-name="${response.name}"
                                       data-channel-description="${response.description || ''}"
                                       onclick="event.stopPropagation(); editChannel(this.getAttribute('data-channel-name'), this.getAttribute('data-channel-description'));">
                                        <i class="fas fa-edit me-2"></i> Edit channel
                                    </a>
                                </li>
                                <li>
                                    <a class="dropdown-item text-danger" href="#" 
                                       onclick="event.stopPropagation(); confirmDeleteChannel('${response.name}');">
                                        <i class="fas fa-trash me-2"></i> Delete channel
                                    </a>
                                </li>
                            </ul>
                        </div>
                    `;
                    
                    channelList.appendChild(newChannel);
                    
                    // Switch to the new channel
                    switchChannel(response.name);
                } catch (e) {
                    console.error('Error parsing channel creation response:', e);
                }
            }
            
            // Get the modal element
            const channelModal = document.getElementById('newChannelModal');
            // Retrieve the Bootstrap modal instance
            const modalInstance = bootstrap.Modal.getInstance(channelModal);
            
            if (modalInstance) {
                // Hide the modal
                modalInstance.hide();
            }
            
            // Reset the form fields
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
            
            fetch('/people/chat/messages', {
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
        if (data.channel === currentChannel && data.type !== 'pin') {
            const chatMessages = document.querySelector('.chat-messages');
            if (chatMessages) {
                loadChannelMessages(currentChannel);
            }
        }
    });
    
    // Handle new messages for unread badges
    socket.on('message_created', function(data) {
        console.log('Message created event received:', data);
        
        if (data.author_id !== currentUserId && data.channel !== currentChannel) {
            console.log(`New message in channel ${data.channel} from user ${data.author_id}, updating unread indicator`);
            updateUnreadIndicator(data.channel, true);
        } else if (data.channel === currentChannel) {
            console.log(`New message in current channel ${data.channel}, scrolling to bottom`);
            scrollToBottom();
        } else {
            console.log(`New message from current user in channel ${data.channel}, no action needed`);
        }
    });
    
    socket.on('channel_created', function(data) {
        console.log('Channel created:', data.name);
    });
    
    socket.on('status', function(data) {
        console.log(data.msg);
    });
    
    // Search functionality
    const searchInput = document.getElementById('chatSearch');
    if (searchInput) {
        // Don't clear search when switching channels
        // document.addEventListener('htmx:afterSwap', function(evt) {
        //     if (evt.detail.target.classList.contains('chat-messages')) {
        //         searchInput.value = '';
        //     }
        // });
        
        // Update search endpoint when input changes
        searchInput.addEventListener('htmx:configRequest', function(evt) {
            // Always use the current channel for search
            evt.detail.path = `/people/chat/channels/${currentChannel}/search`;
            console.log('Search request configured for channel:', currentChannel);
        });
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Re-initialize after HTMX content swaps
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        if (evt.detail.target.classList.contains('chat-messages')) {
            scrollToBottom();
            
            // Reinitialize tooltips
            const tooltips = evt.detail.target.querySelectorAll('[data-bs-toggle="tooltip"]');
            tooltips.forEach(el => new bootstrap.Tooltip(el));

            updatePinCount();
        }
    });
}); 