# 🎨 ClinicCloud Design System - Quick Reference Card

## Color Palette

### Primary Colors
```
Primary Blue:        #0f4c81  (Main brand color)
Primary Light Blue:  #38b6ff  (Interactive elements)
Primary Dark:        #0a2a4a  (Dark accents)
```

### Secondary Colors
```
Cyan:     #06b6d4  (Secondary actions)
Green:    #10b981  (Success, checkmarks)
Amber:    #f59e0b  (Warnings, cautions)
Red:      #ef4444  (Danger, errors)
```

### Grays (Neutral)
```
50:  #f9fafb   (Almost white)
100: #f3f4f6   (Light gray)
200: #e5e7eb   (Borders)
300: #d1d5db   (Disabled)
400: #9ca3af   (Secondary text)
500: #6b7280   (Body text)
600: #4b5563   (Dark gray)
700: #374151   (Very dark)
800: #1f2937   (Almost black)
900: #111827   (Black)
```

---

## Typography

### Sizes
```
H1: 2.25rem (36px)  - Page titles
H2: 1.875rem (30px) - Section headers
H3: 1.5rem (24px)   - Subsections
H4: 1.25rem (20px)  - Card titles
Base: 1rem (16px)   - Body text
Small: 0.875rem (14px) - Labels
```

### Weights
```
400: Regular text
500: Medium emphasis
600: Labels, semi-bold
700: Bold, headings
```

### Font Family
```
Primary: 'Segoe UI', 'Roboto', '-apple-system', 'BlinkMacSystemFont'
Mono:    'Fira Code', 'Courier New', monospace
```

---

## Spacing Scale (8px Base Unit)

```
--space-xs:   0.25rem (4px)
--space-sm:   0.5rem  (8px)
--space-md:   1rem    (16px) ← Default
--space-lg:   1.5rem  (24px)
--space-xl:   2rem    (32px)
--space-2xl:  3rem    (48px)
```

---

## Border Radius

```
--radius-sm:   0.375rem (6px)
--radius-md:   0.5rem   (8px)
--radius-lg:   0.75rem  (12px)
--radius-xl:   1rem     (16px)
--radius-2xl:  1.5rem   (24px)
```

---

## Shadows (Box-Shadow)

```
--shadow-sm:   0 1px 2px rgba(0,0,0,0.05)
--shadow-md:   0 4px 6px -1px rgba(0,0,0,0.1)       ← Standard cards
--shadow-lg:   0 10px 15px -3px rgba(0,0,0,0.1)     ← Elevated cards
--shadow-xl:   0 20px 25px -5px rgba(0,0,0,0.1)     ← Modals
--shadow-2xl:  0 25px 50px -12px rgba(0,0,0,0.25)   ← Maximum
```

---

## Transitions

```
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1)
--transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1) ← Default
--transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1)
```

---

## CSS Classes Reference

### Buttons
```html
<button class="primary">Primary Action</button>
<button class="secondary">Secondary</button>
<button class="danger">Delete</button>
```

### Cards
```html
<div class="card">
  <div class="card-header"><h3>Title</h3></div>
  <div class="card-body">Content</div>
  <div class="card-footer">Actions</div>
</div>
```

### Forms
```html
<div class="form-group">
  <label>Field Label</label>
  <input type="text">
  <p class="form-help-text">Help text</p>
</div>
```

### Badges
```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-danger">Danger</span>
```

### Status Badges
```html
<span class="status-badge status-active">Active</span>
<span class="status-badge status-pending">Pending</span>
<span class="status-badge status-completed">Completed</span>
<span class="status-badge status-cancelled">Cancelled</span>
<span class="status-badge status-inactive">Inactive</span>
```

### Lists
```html
<ul>
  <li>Item with arrow indicator</li>
  <li>Animated on hover</li>
</ul>
```

### Tables
```html
<table>
  <thead><!-- Gradient header --></thead>
  <tbody><!-- Hover effect --></tbody>
</table>
```

### Utility Classes
```css
.text-center       - Center align text
.text-right        - Right align text
.text-muted        - Gray text
.text-danger       - Red text
.text-success      - Green text
.text-warning      - Amber text
.text-info         - Blue text

.mt-1, .mt-2, .mt-3, .mt-4  - Margin top
.mb-1, .mb-2, .mb-3, .mb-4  - Margin bottom
.px-2, .py-2                - Padding
```

---

## Page Layout Classes

### List Pages
```html
<div class="list-page">
  <div class="list-header">
    <h2>Title</h2>
    <div class="list-actions">
      <div class="search-bar">...</div>
      <button>Action</button>
    </div>
  </div>
  <div class="filter-bar">...</div>
  <table>...</table>
</div>
```

### Form Pages
```html
<div class="form-page">
  <form class="form-section">
    <h3>Section</h3>
    <div class="form-group">...</div>
    <div class="form-actions">...</div>
  </form>
</div>
```

### Record/Detail Pages
```html
<div class="record-header">...</div>
<div class="record-sections">
  <div class="record-section">
    <div class="record-field">...</div>
  </div>
</div>
<div class="record-actions">...</div>
```

### Profile Pages
```html
<div class="profile-header">
  <div class="profile-avatar">👤</div>
  <h2 class="profile-name">Name</h2>
</div>
<div class="profile-tabs">...</div>
<div class="profile-content">
  <div class="profile-info-card">...</div>
</div>
```

---

## Responsive Breakpoints

```
Mobile:   < 768px      (Single column, simplified)
Tablet:   768px-1023px (2-3 columns)
Desktop:  ≥ 1024px     (Full layout)
```

---

## Color Usage by Feature

```
Patients:        Blue     (#0f4c81 → #38b6ff)
Appointments:    Cyan     (#06b6d4 → #14b8a6)
Labs:            Green    (#10b981 → #34d399)
Billing:         Amber    (#f59e0b → #fbbf24)
AI/Analytics:    Purple   (#8b5cf6 → #a78bfa)
Admin:           Red      (#ef4444 → #f87171)
```

---

## Animation Keyframes

```css
@keyframes fadeIn       /* Fade in from transparent */
@keyframes slideInUp    /* Slide up from below */
@keyframes slideInLeft  /* Slide in from left */
@keyframes slideInRight /* Slide in from right */
@keyframes pulse        /* Pulse opacity (loading) */
@keyframes shimmer      /* Shimmer effect (skeleton) */
```

---

## Common Patterns

### Gradient Button
```html
<button style="
  background: linear-gradient(135deg, #0f4c81 0%, #38b6ff 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 700;
">Button</button>
```

### Gradient Card
```html
<div style="
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
">Content</div>
```

### Hover Lift
```css
.card {
  transition: all var(--transition-base);
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
```

### Responsive Grid
```html
<div style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
">
  <!-- Cards auto-layout -->
</div>
```

---

## Accessibility Checklist

```
☐ Color contrast ≥ 4.5:1
☐ Focus indicators visible
☐ Heading hierarchy correct
☐ Form labels present
☐ Semantic HTML used
☐ Keyboard navigation works
☐ Alt text on images
☐ 44px minimum touch targets
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `main.css` | Core system & variables |
| `navbar_worldclass.css` | Navigation styling |
| `worldclass.css` | Animations & utilities |
| `app-pages.css` | Application pages |
| `landing.html` | Landing page |
| `dashboard.html` | Dashboard |

---

## Documentation Files

| File | Content |
|------|---------|
| `DESIGN_SYSTEM.md` | Complete reference |
| `IMPLEMENTATION_GUIDE.md` | Code examples |
| `DESIGN_CHECKLIST.md` | Implementation tracking |
| `DESIGN_UPGRADE_SUMMARY.md` | What changed |
| `DESIGN_UPGRADE_README.md` | Executive summary |

---

## Browser Support

✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+
✅ Mobile Safari
✅ Chrome Mobile

---

## Quick Implementation Tips

1. **Use CSS Variables**: Never hardcode colors
   ```css
   color: var(--primary);
   background: var(--neutral-100);
   ```

2. **Apply Component Classes**:
   ```html
   <div class="card">...</div>
   <button class="primary">...</button>
   ```

3. **Use Spacing Variables**:
   ```css
   padding: var(--space-lg);
   gap: var(--space-md);
   ```

4. **Responsive Grids**:
   ```css
   grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
   ```

5. **Smooth Transitions**:
   ```css
   transition: all var(--transition-base);
   ```

---

## Common Tasks

### Change Primary Color
Edit `:root` variables in `main.css`

### Make Page Mobile-Responsive
Use grid with `auto-fit, minmax(280px, 1fr)`

### Add Hover Effect
Use `transition` + `:hover` with `transform` or `box-shadow`

### Create Status Badge
Use `<span class="status-badge status-{type}">`

### Build Form
Use `.form-page` → `.form-section` → `.form-group`

### Style Table
Table automatically gets gradient header + hover effects

---

## Pro Tips ⚡

💡 **Gradients**: Use `linear-gradient(135deg, color1, color2)`
💡 **Shadows**: Use `var(--shadow-lg)` for instant depth
💡 **Animations**: Use `transform` + `opacity` for performance
💡 **Mobile**: Test at 375px, 768px, 1024px
💡 **Accessibility**: Always provide focus states

---

## Need Help?

📖 **Design Questions** → Read `DESIGN_SYSTEM.md`
💻 **Implementation** → Read `IMPLEMENTATION_GUIDE.md`
✅ **Track Progress** → Use `DESIGN_CHECKLIST.md`
📊 **What Changed** → See `DESIGN_UPGRADE_SUMMARY.md`

---

**Print this card and keep it handy! 📌**

*Version 1.0 | ClinicCloud Design System | 2026*