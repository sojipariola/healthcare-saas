# ClinicCloud Design System & Style Guide

## Overview
This document defines the world-class design system used throughout ClinicCloud, ensuring consistency, professionalism, and excellent user experience across all web pages.

## Color Palette

### Primary Colors
- **Primary**: `#0f4c81` - Deep healthcare blue (used for main actions and headers)
- **Primary Light**: `#38b6ff` - Bright accent blue (used for highlights and interactive elements)
- **Primary Dark**: `#0a2a4a` - Dark navy (used for text and emphasis)

### Secondary Colors
- **Secondary**: `#06b6d4` - Cyan (used for secondary actions)
- **Success**: `#10b981` - Green (used for positive feedback)
- **Warning**: `#f59e0b` - Amber (used for cautionary messages)
- **Danger**: `#ef4444` - Red (used for critical actions)

### Neutral Colors
- **Neutral 50**: `#f9fafb` - Almost white (backgrounds)
- **Neutral 100**: `#f3f4f6` - Light gray (secondary backgrounds)
- **Neutral 200**: `#e5e7eb` - Medium gray (borders)
- **Neutral 300**: `#d1d5db` - Medium-dark gray
- **Neutral 400**: `#9ca3af` - Gray (secondary text)
- **Neutral 500**: `#6b7280` - Dark gray (body text)
- **Neutral 600**: `#4b5563` - Darker gray
- **Neutral 700**: `#374151` - Very dark gray
- **Neutral 800**: `#1f2937` - Almost black
- **Neutral 900**: `#111827` - Black

## Typography

### Font Family
- **Sans Serif**: 'Segoe UI', 'Roboto', '-apple-system', 'BlinkMacSystemFont', sans-serif
- **Monospace**: 'Fira Code', 'Courier New', monospace

### Font Sizes & Hierarchy
- **H1**: 2.25rem (36px) - Page titles, hero sections
- **H2**: 1.875rem (30px) - Section headers
- **H3**: 1.5rem (24px) - Subsection headers
- **H4**: 1.25rem (20px) - Card titles
- **Body**: 1rem (16px) - Regular text
- **Small**: 0.875rem (14px) - Captions, labels

### Font Weights
- **700 (Bold)**: Headings, emphasis, buttons
- **600 (Semibold)**: Labels, form fields, important text
- **500 (Medium)**: Navigation, secondary text
- **400 (Regular)**: Body text, descriptions

## Spacing System

| Variable | Value | Usage |
|----------|-------|-------|
| `--space-xs` | 0.25rem | Minimal spacing |
| `--space-sm` | 0.5rem | Between inline elements |
| `--space-md` | 1rem | Default paragraph spacing |
| `--space-lg` | 1.5rem | Section spacing |
| `--space-xl` | 2rem | Major section spacing |
| `--space-2xl` | 3rem | Page-level spacing |

## Border Radius

| Variable | Value | Usage |
|----------|-------|-------|
| `--radius-sm` | 0.375rem | Small buttons, inputs |
| `--radius-md` | 0.5rem | Standard form elements |
| `--radius-lg` | 0.75rem | Cards, modals |
| `--radius-xl` | 1rem | Large components |
| `--radius-2xl` | 1.5rem | Hero sections, containers |

## Shadows

| Variable | Value | Usage |
|----------|-------|-------|
| `--shadow-sm` | 0 1px 2px rgba(0,0,0,0.05) | Subtle depth |
| `--shadow-md` | 0 4px 6px -1px rgba(0,0,0,0.1) | Standard cards |
| `--shadow-lg` | 0 10px 15px -3px rgba(0,0,0,0.1) | Elevated cards |
| `--shadow-xl` | 0 20px 25px -5px rgba(0,0,0,0.1) | Modals, dropdown |
| `--shadow-2xl` | 0 25px 50px -12px rgba(0,0,0,0.25) | Maximum depth |

## Transitions

| Variable | Value | Usage |
|----------|-------|-------|
| `--transition-fast` | 150ms cubic-bezier(0.4, 0, 0.2, 1) | Quick interactions |
| `--transition-base` | 200ms cubic-bezier(0.4, 0, 0.2, 1) | Standard interactions |
| `--transition-slow` | 300ms cubic-bezier(0.4, 0, 0.2, 1) | Significant changes |

## Component Styles

### Buttons

#### Primary Button
```css
background: linear-gradient(135deg, #0f4c81 0%, #38b6ff 100%);
color: #fff;
padding: 0.75rem 1.5rem;
border-radius: 6px;
font-weight: 700;
box-shadow: 0 4px 12px rgba(15, 76, 129, 0.15);
```

**Hover State:**
- Transform: `translateY(-2px)`
- Shadow: `0 8px 20px rgba(15, 76, 129, 0.25)`

### Cards

```css
background: #fff;
border-radius: 12px;
padding: 2rem;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
border: 1px solid #e5e7eb;
```

**Hover State:**
- Box-shadow: `0 12px 24px rgba(0, 0, 0, 0.12)`
- Transform: `translateY(-4px)`

### Forms

#### Input Fields
```css
width: 100%;
padding: 0.75rem 1rem;
border: 1.5px solid #e5e7eb;
border-radius: 0.75rem;
background: #f9fbfd;
transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
```

**Focus State:**
- Border-color: `#38b6ff`
- Background: `#fff`
- Box-shadow: `0 0 0 3px rgba(56, 182, 255, 0.1)`

#### Labels
```css
font-weight: 600;
color: #0f4c81;
font-size: 0.95rem;
margin-bottom: 0.5rem;
```

### Tables

```css
border-collapse: collapse;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
border-radius: 8px;
overflow: hidden;
```

**Header:**
- Background: `linear-gradient(90deg, #0f4c81 0%, #38b6ff 100%)`
- Color: `#fff`
- Font-weight: `700`
- Text-transform: `uppercase`
- Font-size: `0.95rem`
- Letter-spacing: `0.5px`

**Row Hover:**
- Background: `#f9fafb`

## Animations

### Fade In
Used for page and component transitions
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

### Slide Up
Used for content appearing from below
```css
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Pulse
Used for loading states and attention
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
```

## Responsive Design

### Breakpoints
- **Desktop**: 1024px and above
- **Tablet**: 768px - 1023px
- **Mobile**: Below 768px

### Mobile-First Approach
All styles are designed mobile-first and enhanced for larger screens. Use `@media (min-width: ...)` for desktop enhancements.

## Accessibility Guidelines

1. **Color Contrast**: All text meets WCAG AA standards (4.5:1 ratio for normal text)
2. **Focus States**: All interactive elements have visible focus indicators
3. **Motion**: Respect `prefers-reduced-motion` media query
4. **Touch Targets**: Minimum 44px x 44px for interactive elements
5. **Semantic HTML**: Use proper heading hierarchy and semantic elements
6. **ARIA Labels**: Use when necessary for screen readers

## Best Practices

### CSS Usage
1. Use CSS variables for consistency
2. Leverage the design system tokens
3. Apply transitions smoothly (never without animation)
4. Use appropriate shadow depths for visual hierarchy
5. Maintain consistent spacing throughout

### Component Development
1. Build components mobile-first
2. Test all interactive states (hover, focus, active)
3. Ensure accessibility compliance
4. Use semantic HTML
5. Document component variations

### Typography
1. Never use font sizes below 0.875rem (14px)
2. Maintain line-height of 1.6 for body text
3. Use proper font weights from the hierarchy
4. Keep line length between 50-75 characters for readability

### Color Usage
1. Never rely on color alone to convey information
2. Use primary color for main CTAs
3. Use secondary colors for supporting actions
4. Use semantic colors (success, warning, danger) appropriately
5. Maintain sufficient contrast ratios

## Component Library

### Available Components
- Buttons (Primary, Secondary, Danger)
- Cards (with headers and footers)
- Forms (with validation styles)
- Tables (responsive)
- Badges (with color variants)
- Alerts (info, success, warning, danger)
- Navigation (navbar with dropdowns)
- Footer
- Hero sections
- Feature grids
- Testimonial cards
- Pricing cards

## Files Reference

- **Main Styles**: `/static/css/main.css` - Core design system and components
- **Navbar Styles**: `/static/css/navbar_worldclass.css` - Navigation bar styling
- **Enhancements**: `/static/css/worldclass.css` - Additional animations and utilities
- **Landing Page**: `/templates/landing.html` (embedded styles)
- **Base Template**: `/templates/base/base.html` - Main page template

## Implementation Tips

1. Always use CSS variables instead of hardcoding colors
2. Use transitions from the transition system
3. Apply shadows for depth and emphasis
4. Maintain consistent spacing using the spacing scale
5. Test components on multiple devices
6. Validate WCAG accessibility compliance
7. Use semantic HTML to support assistive technologies

---

**Last Updated**: January 2026
**Version**: 1.0 (World-Class Design System)