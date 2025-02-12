# From Company Updates to Real-Time Chat: Building a Lightweight Team Communication System

## Overview

Following my previous post about implementing [Real-Time Updates Implementation in People Module](/blog/updates-websocket/), I've evolved the system into a full-fledged chat platform. The goal was to create a familiar, Slack-like interface that maintains simplicity while providing essential team communication features. This transformation wasn't just about renaming - it involved rethinking how teams interact within our platform.

## Why the Evolution?

While the previous updates system worked well for company announcements, I believe that teams need more dynamic communication options. I noticed that updates could beused for various purposes:
- Company-wide announcements
- Team discussions
- Event planning
- General conversations

This variety of use cases naturally led to the idea of a dedicated channel-based chat system, similar to Slack but streamlined for smaller teams.

## Core Features

### Channel-Based Communication
Instead of using message types, we've implemented a proper channel system with a dedicated Channel model:

```python
@ModelRegistry.register
class Channel(db.Model):
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.now())
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_private = db.Column(db.Boolean, default=False)
```

The system automatically creates default channels:
- #general for day-to-day team conversations
- #announcements for important company updates
- #events for team activities and planning

Each channel has its own description, providing context for its purpose.

### Message Model Evolution

The chat model has been simplified while adding new features:

```python
@ModelRegistry.register
class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    pinned = db.Column(db.Boolean, default=False)
   
    author = db.relationship('User',
                           foreign_keys=[author_id],
                           backref=db.backref('authored_chats', lazy='dynamic'),
                           lazy='joined')
    liked_by = db.relationship('User',
                             secondary=chat_likes,
                             backref=db.backref('liked_messages', lazy='dynamic'),
                             lazy='dynamic')
```

Key features include:
- Channel association for organized conversations
- Message pinning for important information
- Like functionality for engagement
- Automatic URL detection and formatting

## Real-Time Architecture

The WebSocket implementation remains the foundation, but now includes channel-specific events:

```python
@blueprint.route("/chat/create", methods=["POST"])
@login_required
def create_chat():
    try:
        content = request.form.get("content")
        channel_name = request.form.get("channel", "general")
        pinned = bool(request.form.get("pin", False))

        channel = Channel.query.filter_by(name=channel_name).first()
        if not channel:
            return f"Channel {channel_name} not found", 404

        chat = Chat(
            content=content,
            author_id=current_user.id,
            channel_id=channel.id,
            pinned=pinned
        )
        db.session.add(chat)
        db.session.commit()

        # Emit WebSocket event with channel info
        current_app.socketio.emit("chat_changed", {
            "channel": channel_name
        }, room=channel_name)
        
        return ""
    except Exception as e:
        return str(e), 400
```

The system now emits channel-specific events, ensuring users only receive updates for channels they're actively viewing.

## Enhanced User Interface

The interface has been refined to provide a more intuitive chat experience:

```html
<div class="chat-layout">
    <!-- Channel Sidebar -->
    <div class="chat-sidebar">
        <div class="sidebar-header">
            <h3>{{ _('Channels') }}</h3>
            <button class="btn btn-sm btn-link" data-bs-toggle="modal" data-bs-target="#newChannelModal">
                <i class="fas fa-plus"></i>
            </button>
        </div>
        <div class="channel-list">
            {% for channel in channels %}
            <div class="channel {% if channel.name == default_channel.name %}active{% endif %}" 
                 data-channel="{{ channel.name }}"
                 data-description="{{ channel.description }}"
                 onclick="switchChannel('{{ channel.name }}')">
                <span class="channel-prefix">#</span> {{ channel.name }}
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Main Chat Area -->
    <div class="chat-main">
        <div class="chat-header">
            <div class="chat-header-info">
                <h2><span class="channel-prefix">#</span><span id="current-channel">{{ default_channel.name }}</span></h2>
                <p class="channel-description" id="channel-description">{{ default_channel.description }}</p>
            </div>
        </div>
        <!-- Messages rendered here -->
    </div>
</div>
```

Key UI improvements include:
- Channel descriptions for better context
- Clickable URLs that open in new tabs
- Clean, three-column layout
- Message formatting toolbar
- Real-time channel switching

## Smart URL Handling

We've added intelligent URL detection and formatting:

```python
@property
def formatted_content(self):
    """Format message content with clickable links"""
    url_pattern = r'(https?://[^\s<>"]+|www\.[^\s<>"]+)'
    
    def replace_url(match):
        url = match.group(0)
        display_url = url[:50] + '...' if len(url) > 50 else url
        full_url = url if url.startswith(('http://', 'https://')) else f'https://{url}'
        return f'<a href="{full_url}" target="_blank" rel="noopener noreferrer" class="chat-link">{display_url}</a>'
    
    content = re.sub(url_pattern, replace_url, self.content)
    content = content.replace('\n', '<br>')
    
    return Markup(content)
```

This feature automatically:
- Detects URLs in messages
- Truncates long URLs for display
- Opens links in new tabs
- Adds proper security attributes

## Keeping It Simple (for now)

While building this system, I have not yet implemented the following features. ALl of these are easy to add in the future.
- Threaded replies 
- Direct messages 
- File uploads 
- Emoji reactions 
- Message styling (bold, italic, underline, etc.)
- Channel moderation tools
- Message editing
- Message deletion
- Message pinning
- Message unpinning
- Message liking
- Message unliking

## Future Considerations

While the current implementation serves our needs well, I've designed it with future extensibility in mind:
- Private channels infrastructure is in place
- The message model can be extended for additional features
- The WebSocket architecture can handle increased real-time events
- Channel descriptions provide room for enhanced metadata

## Conclusion

The evolution from a simple updates system to a channel-based chat platform demonstrates how well-structured code can adapt to changing needs. By maintaining the WebSocket foundation while adding proper channel support and enhanced features like URL formatting, we've created a familiar yet lightweight communication tool that serves our team's needs without the complexity of full-featured chat platforms.

The key was finding the right balance between functionality and simplicity, resulting in a system that feels natural to use while requiring minimal training or adjustment from team members.
