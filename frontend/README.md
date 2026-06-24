# AIKosh Dataset Quality Toolkit — Frontend Next.js 14 App Router

This directory contains the user-facing web application of the AIKosh Dataset Quality Evaluation Toolkit. The frontend is built on Next.js 14 (App Router) using TypeScript, Tailwind CSS, shadcn/ui, Zustand, and TanStack Query.

---

## 1. Features

1. **Authentication & Session State:**
   - Secure register/login/logout flow.
   - HttpOnly session cookies for credentials management.
   - Global auth state via Zustand store (`stores/auth.ts`).

2. **Intake Form Wizard (`app/(app)/upload/page.tsx`):**
   - 8-step questionnaire wizard reflecting the reverse-engineered MIDAS 2.0 quality domains.
   - Conditional rendering based on dataset parameters (e.g. metadata criteria, synthetic inputs, ethics flags).
   - Direct-to-S3 pre-signed upload flow for datasets and accessory files.

3. **Dashboard & API Keys Panel (`app/(app)/dashboard/page.tsx`):**
   - Historical assessments list with polling.
   - Developer API keys generator, listing, and revocation controls.

4. **Assessment Details & Radar/Gauge Graphs (`app/(app)/dashboard/[id]/page.tsx`):**
   - Real-time status polling for queued/processing runs.
   - Diagnostic panel displaying pipeline tracebacks for failed runs.
   - Visual quality dashboards for completed assessments:
     - 15-domain Radar Chart (via Recharts).
     - CQI and PRS Gauge indicators.
     - Release eligibility categorization badge.
     - Detailed remediation gaps breakdown.

5. **Admin Moderation Panel (`app/(app)/admin/page.tsx`):**
   - Moderation console to suspend or reactivate user accounts.

---

## 2. Directory Structure

```
frontend/
├── app/                  # Next.js 14 App Router routes
│   ├── (auth)/           # Authentication layout and login/register pages
│   ├── (app)/            # Protected layout pages (upload, dashboard, admin)
│   ├── layout.tsx        # Root layout, Inter font setup, QueryClient provider
│   └── page.tsx          # Landing / Entry point
├── components/           # Reusable UI widgets and custom Recharts charts
├── hooks/                # TanStack query hooks (useAuth, useAssessment)
├── lib/                  
│   ├── api/client.ts     # Cookie-aware API HTTP client
│   └── types/index.ts    # TypeScript interfaces mirroring Pydantic schemas
├── stores/               # Zustand auth session store
└── tailwind.config.ts    # Tailwind styling tokens mapping CSS variables
```

---

## 3. Development Setup

Start the dev container via Docker Compose from the root directory:
```bash
docker-compose up --build
```
The frontend dev server will be accessible at [http://localhost:3000](http://localhost:3000) with hot-reloading enabled.

To compile the production standalone bundle manually:
```bash
npm run build
```
