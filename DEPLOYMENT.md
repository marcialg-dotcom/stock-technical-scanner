# Deployment Guide - Stock Technical Scanner

This guide provides multiple options for deploying your Stock Technical Scanner dashboard permanently.

## Option 1: Streamlit Community Cloud (Recommended - FREE)

Streamlit Community Cloud is the easiest and free way to deploy Streamlit apps.

### Prerequisites
- GitHub account
- Streamlit Community Cloud account (free, sign up at https://streamlit.io/cloud)

### Step-by-Step Instructions

#### 1. Create a GitHub Repository

**Option A: Using GitHub Web Interface**
1. Go to https://github.com/new
2. Create a new repository named `stock-technical-scanner`
3. Make it public (required for free Streamlit Cloud)
4. Don't initialize with README (we already have files)

**Option B: Using Command Line**
```bash
cd stock_scanner
git init
git add .
git commit -m "Initial commit: Stock Technical Scanner"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/stock-technical-scanner.git
git push -u origin main
```

#### 2. Deploy to Streamlit Community Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub account (if not already connected)
4. Select your repository: `YOUR_USERNAME/stock-technical-scanner`
5. Set main file path: `app.py`
6. Click "Deploy!"

**Your app will be live at:**
`https://YOUR_USERNAME-stock-technical-scanner.streamlit.app`

### Advantages
- ✅ Completely FREE
- ✅ Automatic HTTPS
- ✅ Auto-deploys on git push
- ✅ No server management
- ✅ Built-in monitoring

### Limitations
- Apps sleep after inactivity (wake up on first visit)
- Resource limits (1 GB RAM, 1 CPU)
- Public repository required for free tier

---

## Option 2: Heroku (Free Tier Available)

### Prerequisites
- Heroku account (https://heroku.com)
- Heroku CLI installed

### Files Needed

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

### Deployment Steps

```bash
cd stock_scanner
heroku login
heroku create stock-technical-scanner
git init
git add .
git commit -m "Deploy to Heroku"
git push heroku main
heroku open
```

---

## Option 3: AWS EC2 (Full Control)

### Prerequisites
- AWS account
- Basic Linux knowledge

### Steps

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier eligible)
   - Open port 8501 in security group

2. **Connect and Install**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Python and dependencies
sudo apt update
sudo apt install python3-pip -y
pip3 install streamlit yfinance pandas

# Upload your code
git clone https://github.com/YOUR_USERNAME/stock-technical-scanner.git
cd stock-technical-scanner

# Run with nohup (keeps running after logout)
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

3. **Access**: `http://your-ec2-ip:8501`

### For Production (with domain)
- Use Nginx as reverse proxy
- Set up SSL with Let's Encrypt
- Use systemd for process management

---

## Option 4: DigitalOcean App Platform

### Prerequisites
- DigitalOcean account
- GitHub repository

### Steps

1. Go to https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Connect GitHub repository
4. Select `stock-technical-scanner`
5. DigitalOcean auto-detects Streamlit
6. Click "Next" → "Launch App"

**Cost**: ~$5/month for basic tier

---

## Option 5: Google Cloud Run (Serverless)

### Prerequisites
- Google Cloud account
- Docker installed locally

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Deploy

```bash
gcloud run deploy stock-scanner \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Recommended Approach for Your Use Case

### For Personal Use / Testing
**→ Streamlit Community Cloud** (FREE, easiest)

### For Small Team / Business
**→ DigitalOcean App Platform** ($5/month, reliable)

### For Enterprise / High Traffic
**→ AWS EC2 with Load Balancer** (scalable, full control)

---

## Post-Deployment Checklist

- [ ] Test all four scan types
- [ ] Verify CSV downloads work
- [ ] Check Yahoo Finance links
- [ ] Test with different markets (NASDAQ, NYSE, AMEX, All)
- [ ] Verify date picker functionality
- [ ] Test on mobile devices
- [ ] Set up monitoring/alerts (if using paid service)

---

## Updating Your Deployed App

### Streamlit Community Cloud
```bash
git add .
git commit -m "Update description"
git push origin main
# Auto-deploys within 1-2 minutes
```

### Other Platforms
Follow their respective deployment commands or use CI/CD pipelines.

---

## Troubleshooting

### App Won't Start
- Check logs in deployment platform
- Verify all files are committed to git
- Ensure requirements.txt is present

### Slow Performance
- Consider upgrading to paid tier
- Optimize ticker list size
- Add caching with `@st.cache_data`

### Memory Issues
- Reduce number of stocks scanned
- Process in smaller batches
- Use paid tier with more RAM

---

## Need Help?

- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Community: https://discuss.streamlit.io/
- GitHub Issues: Create issue in your repository

---

**Ready to deploy? Start with Streamlit Community Cloud for the easiest experience!**
