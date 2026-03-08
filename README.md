# Rosanna & Andrew Wedding Website
## Complete Setup & Deployment Guide

---

## 📁 File Structure

```
wedding/
├── index.html          ← Main invitation (beautiful animated page)
├── rsvp.html           ← Guest RSVP form
├── admin.html          ← Admin panel (guest management + WhatsApp)
├── supabase-schema.sql ← Database setup (run once)
├── photos/             ← Add your PNG photos here
│   ├── photo1.png      ← Gallery large portrait
│   ├── photo2.png      ← Gallery photo
│   ├── photo3.png      ← Gallery tall portrait
│   ├── photo4.png      ← Gallery photo
│   └── story.png       ← Our Story section photo
└── README.md           ← This file
```

---

## 🗃️ Step 1 — Supabase Setup

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Click **New Project** → fill in details → wait ~2 minutes
3. Go to **SQL Editor** (left sidebar)
4. Paste the contents of `supabase-schema.sql` and click **Run**
5. Go to **Settings → API** and copy:
   - `Project URL` → `https://hyalpsznjfuhpamzruyg.supabase.co` ✅ already set
   - `anon public` key → `sb_publishable_EsTDh8GbuyYRkVCq7jAtSg_9JUhJCTw` ✅ already set

---

## ⚙️ Step 2 — Configure the Files

Replace `YOUR_SUPABASE_URL` and `YOUR_ANON_KEY` in **both**:
- `rsvp.html` (near the bottom in the `<script>` tag)
- `admin.html` (near the bottom in the `<script>` tag)

Also in `admin.html`, update:
```js
const ADMIN_PASSWORD = 'wedding2026';     // Change to something secret!
const WEDDING_URL = 'https://your-site.vercel.app'; // Your live URL
```

---

## 🖼️ Step 3 — Add Your Photos

In `index.html`, find the photo placeholder comments and replace with actual `<img>` tags:

```html
<!-- Find this: -->
<!-- REPLACE: <img src="photos/photo1.png" alt="Rosanna & Andrew"> -->
<div class="photo-placeholder-icon">✦</div>
...

<!-- Replace with: -->
<img src="photos/photo1.png" alt="Rosanna & Andrew" />
```

Place your beautiful PNG files with decorative borders in the `/photos/` folder.

---

## 🚀 Step 4 — Deploy to Vercel

### Option A: Via GitHub (recommended)
1. Create a GitHub account if needed
2. Create a new repository (e.g. `rosanna-andrew-wedding`)
3. Push all your files:
   ```bash
   git init
   git add .
   git commit -m "Wedding website launch"
   git remote add origin https://github.com/YOUR_USERNAME/rosanna-andrew-wedding.git
   git push -u origin main
   ```
4. Go to [vercel.com](https://vercel.com) → **New Project** → Import from GitHub
5. Select your repo → click **Deploy**
6. Done! You'll get a URL like `rosanna-andrew.vercel.app`

### Option B: Vercel CLI
```bash
npm i -g vercel
cd wedding/
vercel
```

---

## 🌐 Step 5 — Custom Domain (Optional)
1. In Vercel dashboard → your project → **Settings → Domains**
2. Add your domain (e.g. `rosanna-andrew2026.com`)
3. Update DNS records as shown by Vercel

---

## 📱 Admin Panel

Access at: `your-site.vercel.app/admin.html`

**Features:**
- 📊 Live stats — Attending / Declined / Maybe / Not Opened
- 🔍 Filter & search all guests
- ➕ Manually add guests
- 🗑️ Remove guests
- 💬 WhatsApp bulk messaging with personalized templates
- 📋 Variable insertion (`{{first_name}}`, `{{wedding_date}}`, etc.)

---

## 💬 WhatsApp Integration

The admin panel generates WhatsApp deep links (`wa.me`) for each guest.
- Click **WhatsApp** button next to a guest → opens WhatsApp with pre-filled message
- Use **Send via WhatsApp** to open messages for all filtered guests (one by one)
- Customize your template with variables that auto-fill guest names, dates, links

---

## ✅ What's Included

| Feature | Status |
|---------|--------|
| Animated invitation page | ✅ |
| Live countdown timer | ✅ |
| Photo gallery placeholders | ✅ |
| Our Story section | ✅ |
| Wedding details section | ✅ |
| RSVP form with Supabase | ✅ |
| Plus one management | ✅ |
| Meal & dietary preferences | ✅ |
| Song request field | ✅ |
| Message for couple | ✅ |
| Admin guest management | ✅ |
| WhatsApp messaging | ✅ |
| Guest status tracking | ✅ |
| Mobile responsive | ✅ |

---

## 🎨 Color Palette

| Name | Hex |
|------|-----|
| Black | `#0d0d0d` |
| Ivory | `#f5f0e8` |
| Champagne | `#d4b896` |
| Blush | `#e8c4b8` |
| Forest Green | `#3a5c3f` |
| Gold | `#c9a84c` |
| Cream | `#faf7f2` |

---

## 🔐 Security Notes for Production

- Move the admin panel to a private route or add Supabase Auth
- Use Supabase Row Level Security policies properly (already set up in schema)
- Change the admin password from the default
- Consider adding rate limiting on RSVP submissions

---

*Built with love for Rosanna Vanessa Depaz & Andrew Denton Haylock ✦*
*Saturday, the Fourth of July · Two Thousand Twenty-Six · Belize*
