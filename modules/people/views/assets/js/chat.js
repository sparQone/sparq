document.addEventListener('DOMContentLoaded', function() {
    // Initialize WebSocket connection
    const socket = io.connect(window.location.origin);
    let currentChannel = document.getElementById('current-channel').textContent;
    
    // Function to scroll chat to bottom
    function scrollToBottom() {
        const chatMessages = document.querySelector('.chat-messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Join default channel
    socket.emit('join', { channel: currentChannel });
    
    // Channel switching
    window.switchChannel = function(channelName) {
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
        
        // Update current channel
        currentChannel = channelName;
        document.getElementById('current-channel').textContent = channelName;
        document.querySelector('.message-form textarea').placeholder = `Message in #${channelName}`;
        
        // Join new channel
        socket.emit('join', { channel: channelName });
        
        // Load channel messages
        loadChannelMessages(channelName);
    };

    // Function to load channel messages
    function loadChannelMessages(channelName) {
        const chatMessages = document.querySelector('.chat-messages');
        const url = `/people/chat/channels/${channelName}/messages`;
        htmx.ajax('GET', url, { 
            target: chatMessages,
            swap: 'innerHTML',
            afterSwap: function(evt) {
                scrollToBottom();
                // Update description from response if available
                const description = evt.detail.xhr.getResponseHeader('X-Channel-Description');
                if (description) {
                    document.getElementById('channel-description').textContent = decodeURIComponent(description);
                }
            }
        });
    }
    
    // New Channel Modal
    const channelModal = document.getElementById('newChannelModal');
    if (channelModal) {
        const form = channelModal.querySelector('form');
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Close modal and clear form
                bootstrap.Modal.getInstance(channelModal).hide();
                this.reset();
                
                // Switch to new channel
                switchChannel(data.name);
            })
            .catch(error => {
                alert('Error creating channel: ' + error);
            });
        });
    }
    
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
                // Clear the form
                this.reset();
            })
            .catch(error => {
                alert('Error sending message: ' + error.message);
            });
        });
    }
    
    // WebSocket event handling
    socket.on('chat_changed', function(data) {
        if (data.channel === currentChannel) {
            loadChannelMessages(currentChannel);
        }
    });
    
    socket.on('channel_created', function(data) {
        const channelList = document.querySelector('.channel-list');
        const newChannel = document.createElement('div');
        newChannel.className = 'channel';
        newChannel.dataset.channel = data.name;
        newChannel.onclick = () => switchChannel(data.name);
        newChannel.innerHTML = `<span class="channel-prefix">#</span> ${data.name}`;
        channelList.appendChild(newChannel);
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

    // Initial scroll to bottom
    scrollToBottom();

    // Add event listener for when messages are loaded
    document.querySelector('.chat-messages').addEventListener('htmx:afterSwap', function() {
        scrollToBottom();
    });
}); 