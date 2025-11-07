# NicuNearby
## User & Technical Manual

---

**Product:** NicuNearby - NICU Hospital Distance Finder
**Version:** 2.0
**Last Updated:** October 21, 2025
**Live Application:** https://neonearby.vercel.app/
**GitHub Repository:** https://github.com/ruthmarieartistry/nicu-nearby

**Developed for:** Alcea Surrogacy
**Developer:** Ruth Ellis
**Copyright:** © 2025 Ruth Marie Ellis

---

## Table of Contents

1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Project Architecture](#project-architecture)
4. [Getting Started](#getting-started)
5. [Making Updates](#making-updates)
6. [Deployment Guide](#deployment-guide)
7. [NICU Database](#nicu-database)
8. [Search System](#search-system)
9. [Configuration](#configuration)
10. [Troubleshooting](#troubleshooting)
11. [Maintenance Tasks](#maintenance-tasks)
12. [Reference](#reference)

---

## Overview

### What Is NicuNearby?

NicuNearby is a specialized hospital search tool that helps users locate nearby NICU (Neonatal Intensive Care Unit) facilities based on their location. The application provides real-time distance calculations, detailed hospital information, and contact details for 1,473 NICU facilities across the United States.

### Key Features

- **ZIP Code or City/State Search** - Flexible location input
- **Adjustable Search Radius** - 20, 40, 60, or 100-mile options
- **Pre-loaded Database** - 1,473 NICUs with complete information
- **Real-Time Distance Calculation** - Accurate driving distances via Google Maps
- **Comprehensive Hospital Details** - NICU level, bed count, phone, website, ratings
- **Mobile-Responsive Design** - Works on phones, tablets, and desktops
- **Fast Results** - Instant search with no database delays

### Use Cases

- Finding nearby NICUs for intended parents
- Comparing NICU options by distance and level of care
- Emergency NICU location lookup
- Surrogacy planning and preparation
- Hospital research and comparison

---

## Technology Stack

### Frontend Framework

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 14.2.33 | React framework with server-side features |
| **React** | 18.2.0 | UI component library |
| **Tailwind CSS** | 3.4.18 | Utility-first CSS framework |
| **JavaScript** | ES6+ | Primary programming language |

### Hosting & Deployment

| Service | Purpose | Cost |
|---------|---------|------|
| **Vercel** | Next.js hosting platform | Free (100GB/month bandwidth) |
| **GitHub** | Version control & automatic deployment | Free |
| **Google Maps API** | Geocoding & distance calculation | $200/month free credit |

### Database

| Type | Location | Size |
|------|----------|------|
| **Static JSON** | `data/nicu-database.json` | 556KB (1,473 NICUs) |

### Why These Technologies?

- **Next.js** - Optimized for React, built-in API routes, excellent performance
- **Vercel** - Designed for Next.js, automatic deployments, global CDN
- **Tailwind CSS** - Rapid styling, consistent design, mobile-friendly
- **Static database** - No database server needed, fast, reliable
- **Google Maps API** - Industry standard for accurate geocoding and distances

---

## Project Architecture

### Directory Structure

```
nicu-finder/
│
├── public/                          # Static assets served directly
│   ├── nicunearby-logo.png         # Main application logo (60KB)
│   └── alcea-logo.png              # ALCEA branding logo (120KB)
│
├── pages/                           # Next.js pages (URL routes)
│   ├── index.js                    # Main search page (336 lines)
│   │                               # UI components built with React.createElement
│   │
│   ├── api/                        # API routes (serverless functions)
│   │   ├── search-nicus.js         # Main search endpoint (230 lines)
│   │   └── metrics.js              # Analytics endpoint
│   │
│   ├── _app.js                     # Next.js app wrapper
│   ├── _error.js                   # Custom error page
│   └── 404.js                      # Custom 404 page
│
├── data/                            # Application data
│   └── nicu-database.json          # NICU database (1,473 hospitals)
│
├── styles/                          # Stylesheets
│   └── globals.css                 # Global styles & Tailwind imports
│
├── package.json                     # Dependencies & npm scripts
├── next.config.js                  # Next.js configuration
├── tailwind.config.js              # Tailwind CSS configuration
├── postcss.config.js               # PostCSS configuration (for Tailwind)
└── vercel.json                     # Vercel deployment settings
```

### Key Files Explained

| File | Lines | Purpose |
|------|-------|---------|
| `pages/index.js` | 336 | Main search interface, all UI components |
| `pages/api/search-nicus.js` | 230+ | Search logic, geocoding, distance calc |
| `data/nicu-database.json` | 1,473 entries | Complete NICU database |
| `styles/globals.css` | ~10 | Global styles, Tailwind imports |
| `vercel.json` | ~5 | Vercel build configuration |

---

## Getting Started

### Prerequisites

Before working on NicuNearby, ensure you have:

- **Node.js** version 18 or higher
- **npm** (included with Node.js)
- **Git** for version control
- **Google Maps API key** for search functionality
- **Code editor** (VS Code recommended)
- **Terminal/Command Line** access

### Initial Setup

#### 1. Navigate to Project Directory

```bash
cd /Users/ruthellis/nicu-finder
```

#### 2. Install Dependencies

```bash
npm install
```

This downloads all required packages. Only needed once or when `package.json` changes.

#### 3. Create Environment File

Create file `.env.local` in project root:

```bash
echo "GoogleMaps=YOUR_GOOGLE_MAPS_API_KEY" > .env.local
```

Replace `YOUR_GOOGLE_MAPS_API_KEY` with your actual Google Maps API key.

#### 4. Start Development Server

```bash
npm run dev
```

The application will start at `http://localhost:3000`.

#### 5. View in Browser

Open browser and navigate to `http://localhost:3000`. Changes auto-reload.

#### 6. Stop Development Server

Press `Ctrl+C` in terminal.

### Project Commands

| Command | Purpose |
|---------|---------|
| `npm install` | Install dependencies |
| `npm run dev` | Start development server (port 3000) |
| `npm run build` | Build for production |
| `npm run start` | Start production server locally |

---

## Making Updates

### Updating Visual Content

#### Change Application Logo

**File:** `public/nicunearby-logo.png`

**Steps:**
1. Replace the file with your new logo (keep same filename)
2. **OR** use a different filename and update reference:
   - Open `pages/index.js`
   - Find line 79: `src: '/nicunearby-logo.png'`
   - Change to your new filename

**Recommended specs:**
- Format: PNG with transparency
- Size: ~60KB or less
- Dimensions: 300-500px wide

#### Change ALCEA Logo

**File:** `public/alcea-logo.png`
**Referenced in:** `pages/index.js` line 52

Same process as main logo.

#### Update Color Scheme

**File:** `pages/index.js`

**Current colors (lines 39-43):**
```javascript
const rubyRed = '#7d2431';
const darkGreen = '#217045';      // Main search button
const mustardYellow = '#e1b321';  // Method button
const goldBrown = '#a5630b';      // How To Use button
const darkTeal = '#005567';       // Labels, headings
```

**To change:**
1. Search for these variable names
2. Update hex color values
3. Save and test locally
4. Commit and push to deploy

#### Update Copyright Text

**Files:** `pages/index.js`
**Lines:** 53 and 331

Search for `© RME 2025` and update year or text.

### Updating Search Settings

#### Change Default Search Radius

**File:** `pages/index.js`
**Line:** 5

```javascript
const [radius, setRadius] = useState('60');
```

Change `'60'` to desired default: `'20'`, `'40'`, `'60'`, or `'100'`

#### Add New Radius Option

**File:** `pages/index.js`
**Lines:** 131-134

```javascript
React.createElement('option', { value: '20' }, '20 miles'),
React.createElement('option', { value: '40' }, '40 miles'),
React.createElement('option', { value: '60' }, '60 miles'),
React.createElement('option', { value: '100' }, '100 miles')
```

Add new line following the same pattern.

### Updating Content Modals

#### "How To Use" Modal

**File:** `pages/index.js`
**Lines:** 232-293

Contains step-by-step instructions for users.

#### "Method & Reliability" Modal

**File:** `pages/index.js`
**Lines:** 294-334

Contains methodology and data source information.

---

## Deployment Guide

### How Deployment Works

NicuNearby uses **automatic deployment** via GitHub and Vercel:

```
1. Make code changes locally
2. Test with npm run dev
3. Commit to git
4. Push to GitHub
5. Vercel detects push
6. Vercel builds project (npm run build)
7. Vercel deploys to https://neonearby.vercel.app/
```

**Deployment time:** 1-3 minutes after push

### Step-by-Step Deployment

#### 1. Make Changes

Edit files locally using your code editor.

#### 2. Test Locally

```bash
npm run dev
```

Open browser to `http://localhost:3000`, verify changes work.

#### 3. Commit Changes

```bash
git add .
git commit -m "Brief description of what you changed"
```

**Good commit messages:**
- "Update NicuNearby logo to new version"
- "Add Memorial Hospital to NICU database"
- "Change default search radius to 40 miles"

**Bad commit messages:**
- "changes"
- "updates"
- "fix"

#### 4. Push to GitHub

```bash
git push
```

#### 5. Verify Deployment

**Check GitHub:**
```bash
git log --oneline -1
```
Or visit: https://github.com/ruthmarieartistry/nicu-nearby/commits/main

**Check Vercel:**
- Go to https://vercel.com/dashboard
- Click **neonearby** project
- Click **Deployments** tab
- Watch for new deployment
- Green checkmark = successful
- Red X = failed (click for logs)

**Check Live Site:**
- Visit https://neonearby.vercel.app/
- Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Verify changes appear

### Manual Deployment

If automatic deployment fails:

1. Go to https://vercel.com/dashboard
2. Click **neonearby** project
3. Click **Deployments** tab
4. Click **•••** (three dots) on latest deployment
5. Select **Redeploy**
6. Optionally uncheck **Use existing Build Cache** if issues persist
7. Click **Redeploy** button

---

## NICU Database

### Database Overview

**File:** `data/nicu-database.json`
**Format:** JSON
**Size:** 556KB
**Total Hospitals:** 1,473
**Last Updated:** October 2025

### Database Structure

```json
{
  "total": 1473,
  "nicus": [
    {
      "name": "Hospital Name",
      "state": "California",
      "county": "Los Angeles",
      "nicuLevel": "Level III",
      "url": "https://nicudata.com/entry/...",
      "beds": 24,
      "lat": 34.0522,
      "lng": -118.2437,
      "formatted_address": "123 Main St, City, ST 12345, USA",
      "phone": "(555) 123-4567"
    }
  ]
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `name` | String | Hospital name |
| `state` | String | US state |
| `county` | String | County name |
| `nicuLevel` | String | NICU classification (Level I-IV) |
| `url` | String | Source URL from nicudata.com |
| `beds` | Number | NICU bed count (null if unknown) |
| `lat` | Number | Latitude coordinate |
| `lng` | Number | Longitude coordinate |
| `formatted_address` | String | Full address from Google Maps |
| `phone` | String | Hospital phone number |

### Adding a New NICU

**Step 1:** Get Hospital Information

Gather:
- Hospital name
- Full address
- Phone number
- NICU level (I, II, III, or IV)
- Bed count (if available)

**Step 2:** Get Coordinates

Use Google Maps:
1. Search for hospital address
2. Right-click on map marker
3. Click "What's here?"
4. Copy latitude and longitude numbers

**Step 3:** Edit Database File

Open `data/nicu-database.json`:

```json
{
  "total": 1474,  // Increment this number
  "nicus": [
    // ... existing entries ...
    {
      "name": "New Hospital Name",
      "state": "Texas",
      "county": "Harris",
      "nicuLevel": "Level III",
      "url": "https://hospital-website.com",
      "beds": 30,
      "lat": 29.7604,
      "lng": -95.3698,
      "formatted_address": "1234 Medical Dr, Houston, TX 77030, USA",
      "phone": "(713) 555-1234"
    }
  ]
}
```

**Step 4:** Test and Deploy

```bash
npm run dev
# Test search in that area
# Verify new hospital appears
git add data/nicu-database.json
git commit -m "Add [Hospital Name] to NICU database"
git push
```

### Updating Existing NICU

1. Open `data/nicu-database.json`
2. Search for hospital name (Ctrl+F or Cmd+F)
3. Update relevant fields
4. Save file
5. Test locally
6. Commit and push

### Removing a NICU

1. Open `data/nicu-database.json`
2. Find and delete the entire hospital entry (including curly braces)
3. Remove trailing comma if last entry
4. Decrement `total` field by 1
5. Test locally
6. Commit and push

---

## Search System

### How Search Works

```
┌──────────────────────────┐
│  User enters location    │
│  (e.g., "Boston, MA")    │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Frontend sends request  │
│  to /api/search-nicus    │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Google Geocoding API    │
│  "Boston, MA" →          │
│  (42.3601, -71.0589)     │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Load NICU database      │
│  (1,473 hospitals)       │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Calculate distances     │
│  using Haversine formula │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Filter by radius        │
│  (20/40/60/100 miles)    │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Sort by distance        │
│  (closest first)         │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Return results to       │
│  frontend for display    │
└──────────────────────────┘
```

### Search API Endpoint

**File:** `pages/api/search-nicus.js`

**URL:** `/api/search-nicus?location=LOCATION&radius=RADIUS`

**Parameters:**
- `location` - ZIP code or "City, State"
- `radius` - 20, 40, 60, or 100 (miles)

**Returns:**
```json
{
  "results": [
    {
      "name": "Hospital Name",
      "distance": "12.5 mi",
      "nicuLevel": "Level III",
      "beds": 24,
      "address": "123 Main St...",
      "phone": "(555) 123-4567",
      "website": "https://...",
      "placeId": "ChIJ..."
    }
  ]
}
```

### Distance Calculation

**Method:** Haversine Formula

**Purpose:** Calculate great-circle distance between two GPS coordinates

**Formula:** Implemented in `calculateDistance()` function

**Accuracy:** Within 0.5% for distances under 100 miles

**Why not Google Distance Matrix for all?**
- Cost: Haversine is free, Distance Matrix costs $5/1000 requests
- Speed: Haversine is instant, API calls take time
- Sufficiency: Users need approximate distances, not exact driving routes

---

## Configuration

### Environment Variables

**Stored in:** Vercel Dashboard (NOT in code)

| Variable | Purpose | Required |
|----------|---------|----------|
| `GoogleMaps` | Google Maps API key | **YES** |

**Current API Key:** `AIzaSyBVbzetOCtZbIvlp5mBdSD9_aaY64ulhiE`

### Setting Environment Variables

**For Local Development:**

Create `.env.local` file in project root:

```
GoogleMaps=AIzaSyBVbzetOCtZbIvlp5mBdSD9_aaY64ulhiE
```

**For Production (Vercel):**

1. Go to https://vercel.com/dashboard
2. Click **neonearby** project
3. Click **Settings** → **Environment Variables**
4. Click **Add New**
5. Enter:
   - **Name:** `GoogleMaps`
   - **Value:** Your API key
   - **Environments:** Check all three boxes
6. Click **Save**
7. **Redeploy** for changes to take effect

### Build Settings

**Vercel Configuration:**

| Setting | Value |
|---------|-------|
| Framework Preset | **Next.js** |
| Build Command | `next build` |
| Output Directory | `.next` |
| Install Command | `npm install` |
| Root Directory | (empty) |
| Node.js Version | 22.x |

**IMPORTANT:** Framework must be "Next.js", not "Express" or other.

---

## Troubleshooting

### Common Issues

#### "API key not configured" Error

**Symptoms:** Search fails with error message

**Causes:**
1. Missing environment variable
2. Incorrect API key
3. Environment variable not deployed

**Solutions:**

**Check Vercel environment variables:**
1. Vercel Dashboard → neonearby → Settings → Environment Variables
2. Verify `GoogleMaps` variable exists
3. Verify value is correct
4. If missing or wrong, add/update and redeploy

**Redeploy after adding variable:**
1. Deployments tab
2. Click **•••** on latest deployment
3. Select **Redeploy**

#### Search Returns 0 Results

**Possible causes:**
1. Location not found by Google
2. No NICUs within selected radius
3. Typo in location name

**Solutions:**

**Try ZIP code instead of city:**
```
Instead of: "Boston Massachusetts"
Try: "02101"
```

**Increase search radius:**
```
Try 100 miles instead of 20 miles
```

**Check Google Maps API quota:**
- Visit https://console.cloud.google.com/apis/
- Check daily quota remaining

#### Changes Not Appearing on Live Site

**Check push succeeded:**
```bash
git log --oneline -1
# Should show your latest commit
```

**Check Vercel deployment:**
1. Go to https://vercel.com/dashboard
2. Click neonearby → Deployments
3. Look for green checkmark (success) or red X (failed)
4. If failed, click deployment to see error logs

**Clear browser cache:**
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Or open in incognito window

#### Build Fails on Vercel

**Common errors:**

**Framework set incorrectly:**
```
Error: Build failed
```
**Solution:**
- Settings → Build & Development Settings
- Change Framework Preset to "Next.js"
- Redeploy

**Syntax error:**
```
Error: Unexpected token on line X
```
**Solution:**
- Check error log for line number
- Fix syntax error in code
- Test locally with `npm run dev`
- Push again

**Missing dependency:**
```
Error: Cannot find module 'package-name'
```
**Solution:**
```bash
npm install
git add package.json package-lock.json
git commit -m "Update dependencies"
git push
```

---

## Maintenance Tasks

### Regular Updates

#### Monthly: Check Database Accuracy

1. Spot-check 10-20 random hospitals
2. Verify phone numbers still work
3. Update any changed information
4. Remove hospitals that have closed
5. Add newly opened NICU facilities

#### Quarterly: Review Search Performance

1. Test searches in various locations
2. Check response times
3. Verify distance calculations accurate
4. Update any outdated hospital data
5. Review Google Maps API usage and costs

#### Annually: Update Dependencies

```bash
# Check for outdated packages
npm outdated

# Update all dependencies
npm update

# Test thoroughly
npm run dev

# If everything works, commit
git add package.json package-lock.json
git commit -m "Update dependencies to latest versions"
git push
```

### Google Maps API Management

**Monitor Usage:**
1. Go to https://console.cloud.google.com/
2. Select your project
3. Navigate to APIs & Services → Dashboard
4. Check Geocoding API and Distance Matrix API usage

**Free Tier Limits:**
- **$200/month free credit**
- Geocoding: ~40,000 free requests/month
- Distance Matrix: ~40,000 free requests/month

**If approaching limits:**
- Consider caching geocoded locations
- Optimize API calls
- Upgrade to paid plan if necessary

### Backup & Version Control

**Git provides automatic backups:**

**View change history:**
```bash
git log --oneline -20
```

**Restore previous version:**
```bash
git checkout COMMIT_HASH -- path/to/file
```

**Undo last commit:**
```bash
git reset --soft HEAD~1  # Keeps changes
# OR
git reset --hard HEAD~1  # Discards changes
```

**Vercel deployment history:**
- Each deployment preserved in Vercel Dashboard
- Can roll back to previous deployment if needed

---

## Reference

### Git Commands Quick Reference

```bash
# Check current status
git status

# View recent commits
git log --oneline -10

# Stage all changes
git add .

# Stage specific file
git add path/to/file

# Commit with message
git commit -m "Message"

# Push to GitHub
git push

# Pull latest changes
git pull

# View file history
git log --oneline -- path/to/file
```

### File Locations Quick Reference

| What | File Path |
|------|-----------|
| Main search page | `pages/index.js` |
| Search API | `pages/api/search-nicus.js` |
| Metrics API | `pages/api/metrics.js` |
| NICU database | `data/nicu-database.json` |
| Global styles | `styles/globals.css` |
| Main logo | `public/nicunearby-logo.png` |
| ALCEA logo | `public/alcea-logo.png` |
| Dependencies | `package.json` |
| Next.js config | `next.config.js` |
| Tailwind config | `tailwind.config.js` |
| Vercel config | `vercel.json` |

### Color Reference

| Color Name | Hex Code | Used For |
|------------|----------|----------|
| Ruby Red | `#7d2431` | Headers, badges |
| Dark Green | `#217045` | Main search button |
| Mustard Yellow | `#e1b321` | Method button |
| Gold Brown | `#a5630b` | How To Use button |
| Dark Teal | `#005567` | Labels, headings |

### API Endpoints Reference

| Endpoint | Method | Parameters | Returns |
|----------|--------|------------|---------|
| `/api/search-nicus` | GET | `location`, `radius` | Array of hospitals |
| `/api/metrics` | GET | None | Request count, timestamp |

### Database Statistics

| Metric | Value |
|--------|-------|
| Total NICUs | 1,473 |
| File Size | 556KB |
| Data Sources | nicudata.com, Google Maps |
| Coverage | All 50 US states |
| Last Updated | October 2025 |

### Support & Resources

| Resource | URL |
|----------|-----|
| Live Application | https://neonearby.vercel.app/ |
| GitHub Repository | https://github.com/ruthmarieartistry/nicu-nearby |
| Vercel Dashboard | https://vercel.com/dashboard |
| Google Cloud Console | https://console.cloud.google.com/ |
| Next.js Documentation | https://nextjs.org/docs |
| Tailwind Documentation | https://tailwindcss.com/docs |

---

**End of User Manual**

*For questions or support, contact Ruth Ellis*

---

**Document Version:** 1.0
**Last Updated:** October 21, 2025
**Next Review:** January 2026
