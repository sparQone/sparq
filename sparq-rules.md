# SparQ Development Rules

## JavaScript Usage Policy

### Core Principle
Minimize JavaScript usage by leveraging HTMX, Bootstrap, and CSS features whenever possible. JavaScript should be the last resort, not the first choice.

### Preferred Technologies
1. **HTMX** - For dynamic interactions and server communication
2. **Bootstrap** - For UI components and responsive design
3. **CSS** - For animations, transitions, and styling

### When to Use Each Technology

#### Use HTMX for:
- Form submissions
- Dynamic content loading
- Server-side validation
- Real-time updates
- Modal dialogs
- Tabs and pagination
- Infinite scroll
- Search-as-you-type
- Any server interaction

Example:
```html
<!-- Instead of JavaScript fetch -->
<button hx-post="/api/save" 
        hx-target="#result"
        hx-swap="outerHTML">
    Save
</button>
```

#### Use Bootstrap for:
- Dropdowns
- Tooltips
- Popovers
- Collapse/Expand
- Modal dialogs
- Tabs
- Accordions
- Form validation

Example:
```html
<!-- Instead of custom JavaScript -->
<div class="collapse" id="collapseExample">
    Content
</div>
<button data-bs-toggle="collapse" 
        data-bs-target="#collapseExample">
    Toggle
</button>
```

#### Use CSS for:
- Animations
- Transitions
- Hover effects
- Show/hide elements
- Simple state changes
- Responsive design

Example:
```css
/* Instead of JavaScript animation */
.card {
    transition: transform 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
}
```

### When JavaScript is Appropriate
Only use JavaScript when:
1. Direct DOM manipulation is absolutely necessary
2. Complex client-side calculations are needed
3. Working with third-party libraries that require JavaScript
4. Implementing complex animations that can't be done with CSS
5. Handling offline functionality
6. Working with WebSocket connections
7. Accessing browser APIs (geolocation, file system, etc.)

### JavaScript Guidelines
When JavaScript must be used:
1. Keep it minimal and focused
2. Use vanilla JavaScript over jQuery
3. Avoid large client-side frameworks
4. Document why JavaScript was necessary
5. Consider if the functionality could be simplified to use HTMX/Bootstrap instead

Example of acceptable JavaScript:
```javascript
// Complex calculation that must happen client-side
function calculateTotalWithTax(items) {
    return items.reduce((total, item) => {
        return total + (item.price * (1 + item.taxRate));
    }, 0);
}
```

### Code Review Checklist
When reviewing code, ask:
- [ ] Could this JavaScript be replaced with HTMX?
- [ ] Is there a Bootstrap component that provides this functionality?
- [ ] Could this animation/transition be done with CSS?
- [ ] Is the JavaScript absolutely necessary?
- [ ] Is the JavaScript minimal and focused?

### Benefits of This Approach
1. Reduced complexity
2. Better maintainability
3. Improved performance
4. Smaller bundle sizes
5. Better accessibility
6. Simpler testing
7. More reliable functionality
8. Progressive enhancement 