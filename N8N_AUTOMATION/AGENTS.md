# Fusion Starter

A production-ready frontend-only React application featuring React Router 6 SPA mode, TypeScript, Vitest, Zod and modern tooling.

## Tech Stack

- **PNPM**: Prefer pnpm
- **Frontend**: React 18 + React Router 6 (spa) + TypeScript + Vite + TailwindCSS 3
- **Testing**: Vitest
- **UI**: Radix UI + TailwindCSS 3 + Lucide React icons

## Project Structure (Inside frontend/ folder)

```
.
├── pages/                # Route components (Index.tsx = home)
├── components/ui/        # Pre-built UI component library
├── App.tsx               # App entry point and with SPA routing setup
├── global.css            # TailwindCSS 3 theming and global styles
├── shared/               # Shared types and utilities
├── package.json          # Project dependencies
├── vite.config.ts        # Vite configuration
└── tsconfig.json         # TypeScript configuration
```

## Key Features

## SPA Routing System

The routing system is powered by React Router 6:

- `pages/Index.tsx` represents the home page.
- Routes are defined in `App.tsx` using the `react-router-dom` import
- Route files are located in the `pages/` directory

### Styling System

- **Primary**: TailwindCSS 3 utility classes
- **Theme and design tokens**: Configure in `global.css`
- **UI components**: Pre-built library in `components/ui/`
- **Utility**: `cn()` function combines `clsx` + `tailwind-merge` for conditional classes

### Shared Types

Import consistent types:

```typescript
import { DemoResponse } from "@shared/api";
```

Path aliases:

- `@shared/*` - Shared folder (`./shared/*`)
- `@/*` - Root folder (`./*`)

## Development Commands

```bash
pnpm dev        # Start dev server
pnpm build      # Production build
pnpm typecheck  # TypeScript validation
pnpm test       # Run Vitest tests
```

## Adding Features

### Add new colors to the theme

Open `global.css` and `tailwind.config.ts` and add new tailwind colors.

### New Page Route

1. Create component in `pages/MyPage.tsx`
2. Add route in `App.tsx`:

```typescript
<Route path="/my-page" element={<MyPage />} />
```

## Production Deployment

- **Standard**: `pnpm build`
- **Cloud Deployment**: Use either Netlify or Vercel via their MCP integrations for easy deployment. Both providers work well with this starter template.

## Architecture Notes

- TypeScript throughout
- Hot reload for rapid development
- Production-ready with multiple deployment options
- Comprehensive UI component library included
