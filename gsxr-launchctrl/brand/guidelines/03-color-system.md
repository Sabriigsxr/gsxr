# Color System — GSXR LAUNCHCTRL

## 3.1 Primary Colors

| Name          | Hex       | RGB         | Usage                  |
|--------------|-----------|-------------|------------------------|
| Obsidian Black | `#080B10` | 8, 11, 16   | Primary background     |
| Carbon Black   | `#111722` | 17, 23, 34  | Secondary background   |
| Racing Blue    | `#087BFF` | 8, 123, 255 | Links, primary buttons |
| Electric Cyan  | `#21C8FF` | 33, 200, 255| Highlights, accents     |

## 3.2 Text Colors

| Name        | Hex       | Usage                       |
|------------|-----------|-----------------------------|
| Clean White | `#F5F7FA` | Primary text, headings      |
| Metallic Silver | `#C7D0DC` | Secondary text, labels   |

## 3.3 Accent Colors

| Name           | Hex       | RGB          | Usage                             |
|----------------|-----------|--------------|-----------------------------------|
| Redline Red    | `#FF3048` | 255, 48, 72  | Accent, warnings, redline marker  |

## 3.4 Gradient Usage

### Primary Gradient (Hero backgrounds, buttons)
```
linear-gradient(135deg, #087BFF 0%, #21C8FF 100%)
```

### Accent Gradient (status, highlights)
```
linear-gradient(90deg, #087BFF 0%, #21C8FF 50%, #FF3048 100%)
```

## 3.5 Accessibility

| Combination                       | Contrast Ratio | WCAG Status |
|-----------------------------------|----------------|-------------|
| Clean White on Obsidian Black      | 19.2           | AAA         |
| Metallic Silver on Obsidian Black  | 11.8           | AAA         |
| Racing Blue on Obsidian Black      | 8.7            | AAA         |
| Redline Red on Obsidian Black      | 5.4            | AA          |
| Racing Blue on Carbon Black        | 2.1            | **FAIL**    |
