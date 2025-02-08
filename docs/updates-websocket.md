# Real-Time Updates Implementation in People Module: From Polling to WebSockets

## Overview

Today I implemented a new real-time updates system in the People module. The People module was initially designed to display company updates. Admittedly, company update posts are not like real-time notifications, so using a simple polling mechanism gets the job done but is not the best solution. To achieve a more elegant and efficient solution, I transitioned to a hybrid system that leverages WebSockets in combination with our own custom Server-Side Events (SSE) mechanism. This way if the updates section is turned into a more general Slack type of system with channels for both announcements (static posts) and general discussions (real-time posts), the code is already in place.

## Initial Implementation Using Polling

At first, the updates feed was implemented using HTMX to periodically poll the server (1 sec). The HTML element responsible for displaying the updates was set up to trigger a refresh on page load and at regular intervals. For example:

```html
<div class="updates-feed"
hx-get="{{ url_for('people_bp.get_updates') }}"
hx-trigger="load, updates-refresh from:body"
hx-swap="innerHTML"
hx-target="this">
</div>
```

While this approach ensured that users eventually saw new updates, the solution was far from optimal.

## Drawbacks of Polling

- **Inelegant design:** The polling mechanism is not a good design and overpopulates the logs with requests.

- **Scalability:** The polling mechanism is not scalable and will not work for a large number of users. (Not an issue for the People module, but a good point to keep in mind for the future if a module needs to support a large number of users.)

- **Inefficient Resource Usage:** Polling generated repeated HTTP requests even when no updates were available, increasing network overhead.


## Transition to WebSocket & Custom SSE System

To overcome these limitations, I adopted a more reactive design using WebSockets. The key innovation was a custom SSE system, which integrates with the WebSocket infrastructure to provide real-time notifications with minimal overhead.

### How the Custom SSE System Works

1. **Logging New Updates:**  
   Whenever a new update is created (for example, when a user posts an update via the "New Update" modal), the update is logged into the database. This ensures persistence and provides a clear audit trail of events.

2. **Notifying Clients via WebSockets:**  
   Immediately after committing the new update to the database, the backend emits an `updates_changed` event over a persistent WebSocket channel. This is achieved by a call similar to:

   ```python
   current_app.socketio.emit('updates_changed', {'update_id': update.id})
   ```

   This event serves as a real-time notification to all connected clients that a new update is available.

3. **Client-Side Handling Using HTMX:**  
   On the client side, JavaScript listens for the `updates_changed` event via a Socket.IO connection. Once the event is received, a minimal HTMX-based AJAX call is triggered to refresh the relevant portion of the page (i.e., the updates feed). For instance:

   ```javascript
   socket.on('updates_changed', (data) => {
       const updatesFeed = document.querySelector('.updates-feed');
       htmx.ajax('GET', '{{ url_for("people_bp.get_updates") }}', {
           target: updatesFeed,
           swap: 'innerHTML'
       });
   });
   ```

   This streamlined interaction ensures that only the necessary part of the page is updated, improving both performance and user experience.

## Benefits of the New Architecture

- **Reduced Network Overhead:**  
  Unlike polling, which continuously sends requests irrespective of changes, the WebSocket-driven approach only triggers an update when a new event is available.

- **Immediate User Feedback:**  
  Real-time notifications mean that users receive new updates almost instantly, significantly enhancing the interactivity of the application.

- **Simplified Client Logic:**  
  Leveraging HTMX for partial page updates minimizes the amount of custom JavaScript required on the client side. The system cleanly separates the responsibilities of update notification (via WebSockets) and UI refresh (via HTMX).

- **Scalability and Efficiency:**  
  This hybrid approach is easier to scale since the server is not burdened with constant polling requests. Instead, it only sends messages when necessary.

## Conclusion

The evolution from a polling-based updates feed to a modern, WebSocket-driven real-time system is a good step forward. By integrating a custom SSE system with WebSockets, I not only log each update to the database but also broadcast an `updates_changed` event to all connected clients. These clients then leverage HTMX to refresh the updates stream seamlessly. This design delivers a clever, lean, and highly responsive solution to real-time updates in the People module.

This also lays the groundwork for any future module or page that needs to display real-time updates.
