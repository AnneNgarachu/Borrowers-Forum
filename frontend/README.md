# 🌍 Borrower's Forum — Web Frontend

The web application for the **Borrower's Forum Platform**, an open-source debt intelligence tool helping debt-stressed countries make informed restructuring decisions.

[![Next.js](https://img.shields.io/badge/Next.js-16-black.svg)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)](https://www.typescriptlang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Live at:** [borrowersforum.org](https://www.borrowersforum.org)

---

## ✨ Overview

This is the public-facing interface for the platform. It presents the debt calculator, precedent search, country data, and supporting resources in a clean, accessible UI. Visitors use the site anonymously, with no account or login required.

### Pages
- **/** — Home, platform overview and entry point
- **/about** — the information asymmetry problem and the platform's purpose
- **/calculator** — converts debt service payments into development-cost equivalents (doctors, schools, climate adaptation)
- **/precedents** — searchable database of historical debt restructuring cases
- **/countries** — country profiles with economic and climate indicators
- **/api-docs** — reference for the underlying API
- **/resources** — supporting material and links
- **/legal** — disclaimer, terms of use, data-source attribution, and privacy notice

---

## 🔐 How It Talks to the API

The frontend never exposes the API key to the browser. Data calls to the backend run through **Next.js Server Actions** (`lib/api-actions.ts`, marked `"use server"`), which execute on Vercel's server and attach a server-side API key before reaching the backend.

- `API_KEY` is read server-side only (`process.env.API_KEY`) and is never shipped to the client
- The backend base URL is read from `NEXT_PUBLIC_API_URL`, with a fallback to the production API URL
- Visitors use the full site anonymously, with no key of their own

If the backend is unreachable or returns an error, the calculator falls back to stored estimate values so the interface stays usable.

---

## 🛠️ Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 16.0.10 | React framework (App Router) |
| **React** | 19.2.0 | UI library |
| **TypeScript** | ^5 | Type safety |
| **Tailwind CSS** | ^4.1.9 | Styling |
| **shadcn/ui** | - | Components (via `components.json` + Radix primitives) |
| **Vercel** | Cloud | Hosting |

---

## 🚀 Local Development

#### Prerequisites
- Node.js (a current LTS release is recommended; no version is pinned in the repo)
- npm, pnpm, or yarn

#### Setup

```bash
# From the repo root
cd frontend

# Install dependencies
npm install

# Set up environment variables
# Create .env.local with:
# NEXT_PUBLIC_API_URL=https://borrowers-forum.onrender.com
# API_KEY=your_server_side_api_key

# Run the dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

> **Note:** `API_KEY` is a server-side secret and must NOT be prefixed with `NEXT_PUBLIC_`, which would expose it to the browser. Only `NEXT_PUBLIC_API_URL` (the base URL, not a secret) is exposed to the client.

---

## 📁 Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── about/
│   ├── api-docs/
│   ├── calculator/
│   ├── countries/
│   ├── precedents/
│   ├── resources/
│   └── legal/
├── components/             # UI components (incl. shadcn/ui in components/ui)
├── hooks/
├── lib/
│   └── api-actions.ts      # Server Actions (API proxy with server-side key)
├── public/
├── styles/
├── components.json         # shadcn configuration
├── next.config.mjs
└── package.json
```

---

## 📝 License

This project is licensed under the MIT License. Copyright (c) 2025-2026 Anne Wanjiru Ngarachu / SAGE Platform LLC. See the [LICENSE](../LICENSE) file at the repository root for details.

---

## 📞 Contact

**Developer**: Anne Wanjiru Ngarachu
**Portfolio**: [annengarachu.com](https://annengarachu.com)
**LinkedIn**: [anne-wanjiru-ngarachu](https://www.linkedin.com/in/anne-wanjiru-ngarachu/)
**GitHub**: [@AnneNgarachu](https://github.com/AnneNgarachu)

The backend API and its documentation live in [`../backend`](../backend).
