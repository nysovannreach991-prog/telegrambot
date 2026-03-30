# 🚀 Deploy Your Bot for FREE (24/7)

## Option 1: Hugging Face Spaces (EASIEST - Recommended!)

**✅ Completely Free | ✅ No Credit Card | ✅ Runs 24/7**

### Steps:

1. **Create Account**
   - Go to https://huggingface.co
   - Sign up for free

2. **Create New Space**
   - Click your profile → "New Space"
   - Name: `telegram-bot`
   - License: MIT
   - Click "Create Space"

3. **Upload Files**
   - Click "Files" → "Add file" → "Upload files"
   - Upload: `bot.py`, `requirements.txt`, `Dockerfile`
   - Commit changes

4. **Add Secrets (Environment Variables)**
   - Go to Settings → "Repository secrets"
   - Add secret: `TELEGRAM_BOT_TOKEN` = your bot token
   - Add secret: `FACEBOOK_COOKIES` = /app/facebook_cookies.txt (optional)

5. **Deploy**
   - Go back to your Space
   - It will automatically deploy!
   - Wait 2-3 minutes
   - Your bot is running 24/7! 🎉

---

## Option 2: Railway (Easy - Free Tier)

**✅ Easy Setup | ⚠️ Free credits monthly | ✅ No Credit Card**

### Steps:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Connect your bot repository
5. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`
6. Deploy!

---

## Option 3: Render (Easy - Free Tier)

**✅ Easy Setup | ✅ Free | ⚠️ Web services sleep (not good for bots)**

> ⚠️ Not recommended for Telegram bots as they need to run continuously

---

## Option 4: Fly.io (Good Alternative)

**✅ Free tier | ✅ Runs 24/7 | ⚠️ Requires Credit Card**

### Steps:

1. Install Fly.io CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Login:
   ```bash
   fly auth login
   ```

3. Initialize:
   ```bash
   fly launch --name telegram-bot
   ```

4. Set secrets:
   ```bash
   fly secrets set TELEGRAM_BOT_TOKEN=your_token_here
   ```

5. Deploy:
   ```bash
   fly deploy
   ```

---

## 📋 Before Deploying

1. **Update `.env` for production:**
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token
   FACEBOOK_COOKIES=/app/facebook_cookies.txt
   ```

2. **Create `.gitignore`:**
   ```
   .env
   __pycache__/
   *.pyc
   facebook_cookies.txt
   ```

3. **Test locally first:**
   ```bash
   python bot.py
   ```

---

## 🔧 Troubleshooting

### Bot doesn't start on Hugging Face
- Check logs in your Space dashboard
- Make sure `TELEGRAM_BOT_TOKEN` is set in secrets
- Verify `requirements.txt` has all dependencies

### Facebook downloads don't work
- Upload `facebook_cookies.txt` to your Space
- Set `FACEBOOK_COOKIES=/app/facebook_cookies.txt` in secrets

### Bot keeps restarting
- Check error logs
- May be rate limited by Telegram
- Wait a few minutes and try again

---

## 🎯 My Recommendation

**Use Hugging Face Spaces** because:
- ✅ 100% Free forever
- ✅ No credit card needed
- ✅ Runs 24/7
- ✅ Easy to upload files
- ✅ Built-in secrets management
- ✅ Good for small-medium bots

**Deploy now:** https://huggingface.co/spaces

---

## 📞 Need Help?

1. Check bot logs on your hosting platform
2. Verify environment variables are set correctly
3. Make sure all files are uploaded
4. Test with `/start` command after deployment

Good luck! 🚀
