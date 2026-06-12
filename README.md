# 🌍 The Borrower's Forum Platform

**Open-source sovereign debt intelligence platform helping debt-stressed countries make informed restructuring decisions.**

[![Live Status](https://img.shields.io/badge/Status-🟢%20LIVE-success)](https://www.borrowersforum.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Live at: [borrowersforum.org](https://www.borrowersforum.org)**

---

## The Problem

Official creditors have coordinated through the Paris Club since 1956, while debtor nations face a fragmented landscape of bilateral, private, and multilateral lenders with no shared intelligence of their own. This platform helps close that gap, giving debtor nations data-driven analysis and historical precedent matching to inform restructuring decisions.

Aligned with the agenda of the UN Expert Group on Debt. Conceptualized through the COP30 Simulation Programme at the British University in Egypt.

---

## What It Does

- **AI Strategy Tools** — debt-strategy briefs and an advisory chat, powered by the Anthropic Claude API
- **Debt Impact Calculator** — converts debt service payments into development equivalents (healthcare workers, schools, climate adaptation)
- **Precedents Database** — 23 historical restructuring cases (2017-2023) with weighted similarity matching
- **Live World Bank Data** — real-time economic indicators for 190+ countries
- **Secure API** — API key authentication, rate limiting, and full OpenAPI documentation

---

## Repository Structure

This is a monorepo containing two applications:

| Folder | What it is | Stack |
|--------|-----------|-------|
| **[`backend/`](backend/)** | REST API (26 endpoints, 38 tests) | FastAPI, Python, SQLAlchemy, Supabase PostgreSQL |
| **[`frontend/`](frontend/)** | Web application | Next.js, React, TypeScript, Tailwind |

See **[`backend/README.md`](backend/README.md)** and **[`frontend/README.md`](frontend/README.md)** for setup, architecture, and full documentation.

---

## Live Deployment

| Component | URL |
|-----------|-----|
| **Web app** | [borrowersforum.org](https://www.borrowersforum.org) |
| **API** | [borrowers-forum.onrender.com](https://borrowers-forum.onrender.com) |
| **API docs** | [borrowers-forum.onrender.com/api/docs](https://borrowers-forum.onrender.com/api/docs) |

---

## License

MIT License. Copyright (c) 2025-2026 Anne Wanjiru Ngarachu / SAGE Platform LLC. See [LICENSE](LICENSE) for details.

---

## Contact

**Developer**: Anne Wanjiru Ngarachu
**Portfolio**: [annengarachu.com](https://annengarachu.com)
**LinkedIn**: [anne-wanjiru-ngarachu](https://www.linkedin.com/in/anne-wanjiru-ngarachu/)
**GitHub**: [@AnneNgarachu](https://github.com/AnneNgarachu)
