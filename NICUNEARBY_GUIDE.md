# NicuNearby - Complete Guide

**Last Updated:** October 21, 2025
**Live URL:** https://neonearby.vercel.app/
**Repository:** https://github.com/ruthmarieartistry/nicu-nearby

---

## What Is NicuNearby?

NicuNearby is a NICU (Neonatal Intensive Care Unit) hospital finder that helps users locate nearby NICU facilities based on their location. It provides real-time distance calculations, hospital details, and contact information.

**Key Features:**
- Search by ZIP code or city/state
- Adjustable search radius (20-100 miles)
- Pre-loaded database of 1,473 NICUs across the United States
- Real-time distance calculation using Google Maps API
- Hospital details: NICU level, beds, phone, website, ratings
- Mobile-responsive design

---

## Technology Stack

### Frontend Framework
- **Next.js 14.2** - React framework with server-side rendering
- **React 18.2** - JavaScript library for building UI
- **Tailwind CSS 3.4** - Utility-first CSS framework

### Language
- **JavaScript (ES6+)** - No TypeScript, pure JavaScript

### Hosting Platform
- **Vercel** - Free hosting optimized for Next.js
- **Deployment:** Automatic on every push to `main` branch
- **Build Command:** `next build`
- **Framework:** Next.js (auto-detected)

### External APIs
- **Google Maps Geocoding API** - Converts user location to coordinates
- **Google Maps Distance Matrix API** - Calculates driving distances
- **API Key:** Stored in Vercel environment variable `GoogleMaps`

### Database
- **Static JSON file** - 1,473 NICUs pre-loaded in `data/nicu-database.json`
- **No live database** - All data is embedded in the application
- **Updated manually** - Requires code deployment to update NICU data

---

## Project Structure

```
nicu-finder/
├── public/                          # Static assets
│   ├── nicunearby-logo.png         # Main logo (60KB)
│   └── alcea-logo.png              # ALCEA branding logo (120KB)
│
├── pages/                           # Next.js pages (routes)
│   ├── index.js                    # Main search page (336 lines)
│   ├── api/                        # API routes (serverless functions)
│   │   ├── search-nicus.js         # Search endpoint (200+ lines)
│   │   └── metrics.js              # Analytics endpoint
│   ├── _app.js                     # Next.js app wrapper
│   ├── _error.js                   # Error page
│   └── 404.js                      # Not found page
│
├── data/                            # NICU database
│   └── nicu-database.json          # 1,473 NICUs (556KB)
│
├── styles/                          # CSS files
│   └── globals.css                 # Global styles + Tailwind imports
│
├── package.json                     # Dependencies and scripts
├── next.config.js                  # Next.js configuration
├── tailwind.config.js              # Tailwind CSS settings
└── postcss.config.js               # PostCSS configuration
```

---

## Local Development Setup

### Prerequisites
- **Node.js 18+** installed
- **npm** (comes with Node.js)
- **Google Maps API Key** (for search functionality)
- Code editor (VS Code recommended)

### Steps to Run Locally

1. **Navigate to project folder:**
   ```bash
   cd /Users/ruthellis/nicu-finder
   ```

2. **Install dependencies** (only needed once or when package.json changes):
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   # Create .env.local file
   echo "GoogleMaps=YOUR_GOOGLE_MAPS_API_KEY" > .env.local
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

5. **Open in browser:**
   - Server runs at `http://localhost:3000`
   - Changes to code auto-reload in browser

6. **Stop development server:**
   - Press `Ctrl+C` in terminal

---

## Making Updates

### Editing Content

#### Update Logo
1. Replace `/Users/ruthellis/nicu-finder/public/nicunearby-logo.png`
2. Keep same filename OR update reference in `pages/index.js` line 79:
   ```javascript
   React.createElement('img', { src: '/nicunearby-logo.png', alt: 'NICU Nearby', ... })
   ```

#### Update ALCEA Logo
1. Replace `/Users/ruthellis/nicu-finder/public/alcea-logo.png`
2. Reference is in `pages/index.js` line 52

#### Update Copyright Text
Edit `pages/index.js` line 53 and 331:
```javascript
React.createElement('p', { ... }, '© RME 2025')
```

#### Update Search Radius Options
Edit `pages/index.js` lines 131-134:
```javascript
React.createElement('option', { value: '20' }, '20 miles'),
React.createElement('option', { value: '40' }, '40 miles'),
// Add or modify options
```

### Editing Styles

**Global styles:** `styles/globals.css`

**Tailwind classes:** Inline in `pages/index.js`

**Colors (Tailwind):**
```javascript
const rubyRed = '#7d2431';
const darkGreen = '#217045';      // Main search button
const mustardYellow = '#e1b321';  // Method button
const goldBrown = '#a5630b';      // How To Use button
const darkTeal = '#005567';       // Labels, headings
```

To change colors: Search for these variables in `pages/index.js` and update hex values.

### Updating the NICU Database

**Database file:** `data/nicu-database.json`

**Structure:**
```json
{
  "total": 1473,
  "nicus": [
    {
      "name": "Hospital Name",
      "state": "California",
      "county": "Los Angeles",
      "nicuLevel": "Level III",
      "url": "https://...",
      "beds": 24,
      "lat": 34.0522,
      "lng": -118.2437,
      "formatted_address": "123 Main St, City, ST 12345, USA",
      "phone": "(555) 123-4567"
    }
  ]
}
```

**To add a NICU:**
1. Open `data/nicu-database.json`
2. Add new entry to `nicus` array
3. Update `total` count
4. Commit and push (redeploys automatically)

**To update existing NICU:**
1. Search for hospital name in `data/nicu-database.json`
2. Update fields
3. Commit and push

---

## Deploying Changes

### Automatic Deployment (Recommended)

1. **Make your changes** to files
2. **Test locally** with `npm run dev`
3. **Commit changes:**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```
4. **Push to GitHub:**
   ```bash
   git push
   ```
5. **Vercel automatically builds and deploys** (takes 1-2 minutes)
6. **Check live site:** https://neonearby.vercel.app/

### Manual Deployment

1. Go to https://vercel.com/dashboard
2. Click **neonearby** project
3. Click **Deployments** tab
4. Click three dots (•••) on latest deployment
5. Select **Redeploy**
6. Confirm

---

## Key Configuration Files

### `package.json`
Defines dependencies and scripts:
```json
{
  "scripts": {
    "dev": "next dev",           // Start local dev server
    "build": "next build",       // Build for production
    "start": "next start"        // Start production server
  }
}
```

### `next.config.js`
Next.js configuration (currently default settings)

### `tailwind.config.js`
Tailwind CSS configuration - defines which files to scan for classes

### `vercel.json`
Vercel deployment settings (created recently):
```json
{
  "buildCommand": "next build",
  "outputDirectory": ".next",
  "framework": "nextjs"
}
```

### `.gitignore`
Files NOT tracked in git:
- `node_modules/` - Dependencies
- `.next/` - Build output
- `.env.local` - Local environment variables (secrets)

---

## Environment Variables

Stored in **Vercel Dashboard** (not in code):

| Variable | Purpose | Required? |
|----------|---------|-----------|
| `GoogleMaps` | Google Maps API key for geocoding & distance | **YES** |

**To update:**
1. Go to Vercel Dashboard → neonearby project
2. Click **Settings** → **Environment Variables**
3. Edit or add `GoogleMaps` variable
4. Select all environments (Production, Preview, Development)
5. Click **Save**
6. **Redeploy** for changes to take effect

**Current API Key:** `AIzaSyBVbzetOCtZbIvlp5mBdSD9_aaY64ulhiE`

---

## How the Search Works

### Step-by-Step Process

1. **User enters location** (e.g., "New York, NY" or "10001")
2. **Frontend sends request** to `/api/search-nicus?location=...&radius=...`
3. **API geocodes location:**
   - Calls Google Maps Geocoding API
   - Converts location → lat/lng coordinates
4. **API loads NICU database** from `data/nicu-database.json`
5. **API calculates distances:**
   - Uses Haversine formula for quick distance estimates
   - Filters NICUs within radius
6. **API sorts results** by distance (closest first)
7. **API returns results** to frontend
8. **Frontend displays hospitals** with details

### Search API File
**File:** `pages/api/search-nicus.js`

**Key functions:**
- `calculateDistance()` - Haversine formula for distance
- `matchNicuData()` - Matches Google results to database
- Main handler - Processes search requests

### Why Google Maps API is Required
- **Geocoding:** Converts "Boston, MA" → (42.3601, -71.0589)
- **Distance Matrix:** Calculates accurate driving distances
- **Without API:** Search will fail with "API key not configured" error

---

## Vercel Deployment Settings

### Build & Development Settings
- **Framework Preset:** Next.js
- **Build Command:** `next build` (default)
- **Output Directory:** `.next` (default)
- **Install Command:** `npm install` (default)
- **Root Directory:** (empty - uses project root)

### Node.js Version
- **Version:** 22.x (set in Vercel dashboard)

### Important Notes
- **Do NOT set Framework to "Express"** (common mistake)
- **Ensure "Production Branch" is `main`**
- Build cache can be cleared if deployments fail: Redeploy → Uncheck "Use existing Build Cache"

---

## Troubleshooting

### "API key not configured" error
1. Check Vercel environment variables: Settings → Environment Variables
2. Verify `GoogleMaps` variable exists and is correct
3. Redeploy after adding/changing environment variables

### Search returns 0 results
- **Check location spelling:** Try ZIP code instead
- **Check API key quota:** https://console.cloud.google.com/apis/
- **Check browser console (F12)** for error messages

### Site not updating after push
1. Check GitHub: https://github.com/ruthmarieartistry/nicu-nearby/commits/main
2. Check Vercel: https://vercel.com/dashboard → neonearby → Deployments
3. Look for failed builds (red X)
4. Click deployment to see error logs

### Build fails on Vercel
Common causes:
- **Framework set to wrong preset** (should be Next.js, not Express)
- **Syntax error in code:** Check error log
- **Missing dependency:** Run `npm install` locally first

### Styling not updating
- **Clear Vercel build cache:** Redeploy without cache
- **Check Tailwind classes are correct:** Must be complete strings (not dynamic)
- **Check globals.css is imported** in `pages/_app.js`

---

## Important Files to Never Delete

- `pages/index.js` - Main search interface
- `pages/api/search-nicus.js` - Search API endpoint
- `data/nicu-database.json` - NICU database (1,473 hospitals!)
- `package.json` - Project configuration
- `next.config.js` - Next.js settings
- `styles/globals.css` - Global styles

---

## Common Tasks

### Add a new NICU to database

1. **Open** `data/nicu-database.json`
2. **Add new entry** to `nicus` array:
   ```json
   {
     "name": "New Hospital Name",
     "state": "State",
     "county": "County",
     "nicuLevel": "Level III",
     "url": "https://website.com",
     "beds": 20,
     "lat": 0.0000,
     "lng": 0.0000,
     "formatted_address": "123 St, City, ST ZIP, USA",
     "phone": "(555) 555-5555"
   }
   ```
3. **Update** `total` field (increment by 1)
4. **Get coordinates:** Use https://www.google.com/maps → Right-click → "What's here?"
5. **Commit and push**

### Change default search radius

Edit `pages/index.js` line 5:
```javascript
const [radius, setRadius] = useState('60'); // Change '60' to desired default
```

### Update "How To Use" or "Method" modals

Edit `pages/index.js`:
- **How To Use:** Lines 232-293
- **Method & Reliability:** Lines 294-334

### Change header colors

Edit `pages/index.js` color variables (lines 39-43):
```javascript
const rubyRed = '#7d2431';
const darkGreen = '#217045';
// etc.
```

---

## Getting Help

- **View errors:** Press F12 in browser → Console tab
- **Check build logs:** Vercel Dashboard → Deployments → Click deployment
- **GitHub:** https://github.com/ruthmarieartistry/nicu-nearby
- **Local testing:** Always run `npm run dev` before pushing

---

## Backup & Safety

- **All code is in GitHub:** Changes are tracked, can be reverted
- **NICU database is in git:** Safe, version-controlled
- **View history:** `git log --oneline`
- **Undo last commit:** `git revert HEAD`
- **Vercel keeps deployment history:** Can roll back in dashboard

---

## Database Statistics

- **Total NICUs:** 1,473
- **File size:** 556KB
- **Data sources:** Scraped from nicudata.com
- **Geocoded:** All hospitals have lat/lng coordinates
- **Last updated:** October 2025

---

## Quick Reference Commands

```bash
# Navigate to project
cd /Users/ruthellis/nicu-finder

# Install dependencies
npm install

# Run locally
npm run dev

# Build for production (test only - Vercel does this automatically)
npm run build

# Commit changes
git add .
git commit -m "Your message"
git push

# View recent commits
git log --oneline -10

# Check current status
git status
```

---

## API Rate Limits & Costs

### Google Maps API
- **Free tier:** $200/month credit
- **Geocoding:** $5 per 1,000 requests (after free tier)
- **Distance Matrix:** $5 per 1,000 requests (after free tier)
- **Monitor usage:** https://console.cloud.google.com/

### Vercel Hosting
- **Free tier:** 100GB bandwidth/month
- **Serverless functions:** 100GB-hours/month
- **Current usage:** Well within free tier
- **Monitor:** Vercel dashboard

---

## Side-by-Side Embed Code

To embed NicuNearby alongside Risk Ranger, use the code in:
`/Users/ruthellis/surrogacy-risk-assessment/EMBED_ZOHO_INLINE.html`

Background color: `#a5b6b9`
