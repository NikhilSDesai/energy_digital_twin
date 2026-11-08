# Vercel Deployment Guide

## Quick Deploy (First Time)

### Step 1: Login to Vercel

```bash
vercel login
```

This will:
- Open your browser
- Ask you to login with GitHub (recommended)
- Authenticate the CLI

### Step 2: Deploy

```bash
cd /Users/nikhildesai/Documents/03_Personal/energy_dt
vercel
```

You'll be asked:
1. **Set up and deploy?** → Yes
2. **Which scope?** → Your personal account
3. **Link to existing project?** → No
4. **Project name?** → uk-energy-digital-twin (or press Enter)
5. **Directory?** → ./ (press Enter)
6. **Override settings?** → No

**Deployment will start!** ⚡

### Step 3: Add Mapbox Token (Environment Variable)

After first deployment:

```bash
vercel env add MAPBOX_TOKEN
```

When prompted:
1. **Value:** Your Mapbox token (starts with pk.eyJ...)
2. **Environment:** Production (and Preview if you want)

Then redeploy:
```bash
vercel --prod
```

### Step 4: Get Your Live URL

After deployment completes, you'll see:
```
✅ Production: https://uk-energy-digital-twin.vercel.app
```

---

## Update config.js for Production

We need to update the app to use environment variables in production. I'll handle this next.

---

## Future Deployments

Every time you push to GitHub:
```bash
git push
```

Then deploy:
```bash
vercel --prod
```

Or set up auto-deploy (I'll configure this).

---

## Custom Domain (Optional)

After deploying, add a custom domain:

1. Go to https://vercel.com/dashboard
2. Click your project
3. Settings → Domains
4. Add your domain (e.g., energygrid.uk)
5. Update DNS as instructed

**Cost:** Domain registration only (~£10/year), Vercel hosting is FREE

---

## Troubleshooting

**"Command not found: vercel"**
```bash
npm install -g vercel
```

**"Not authorized"**
```bash
vercel logout
vercel login
```

**Map not loading**
- Check Mapbox token is set: `vercel env ls`
- Check browser console for errors

**404 on routes**
- Vercel should use vercel.json config automatically

---

## What Gets Deployed

✅ Frontend (HTML/JS/CSS)
✅ GSP boundaries GeoJSON
✅ Config files
❌ Python scripts (not needed)
❌ Raw data CSVs (too large, use GeoJSON instead)
❌ venv directory

Total deployed size: ~5 MB
