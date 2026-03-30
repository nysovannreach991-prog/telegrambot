# 🚀 Quick Deploy to Hugging Face Spaces (5 Minutes!)

## Step-by-Step Guide

### 1️⃣ Create Hugging Face Account
- Go to: https://huggingface.co
- Click "Sign Up"
- Create free account

### 2️⃣ Create New Space
- Click your profile picture (top right)
- Click "New Space"
- Fill in:
  - **Space name**: `telegram-tts-bot` (or any name)
  - **License**: MIT
  - **Space SDK**: Select "Docker"
- Click "Create Space"

### 3️⃣ Upload Your Bot Files

In your new Space:

1. Click "Files" tab
2. Click "Add file" → "Upload files"
3. Upload these files from your project:
   - ✅ `bot.py`
   - ✅ `requirements.txt`
   - ✅ `Dockerfile`
4. Click "Commit changes to main"

### 4️⃣ Add Bot Token (Secret)

1. Click "Settings" tab
2. Scroll to "Repository secrets"
3. Click "New secret"
4. Add:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `8192406513:AAH98aCl4CnoAfBEuVmEhTq-9B9n_8puMP8`
5. Click "Save"

### 5️⃣ Wait for Deployment

- Go back to "App" tab
- Wait 2-5 minutes for build
- You'll see "Running" status when ready
- Your bot is now live 24/7! 🎉

### 6️⃣ Test Your Bot

1. Open Telegram
2. Find your bot
3. Send `/start`
4. It should respond!

---

## 📁 Files to Upload

Make sure you upload these 3 files:

```
✅ bot.py              (main bot code)
✅ requirements.txt    (dependencies)
✅ Dockerfile          (deployment config)
```

**DO NOT upload:**
- ❌ `.env` (contains secrets)
- ❌ `facebook_cookies.txt` (private)
- ❌ `.gitignore`

---

## ⚙️ Optional: Add Facebook Cookies

If you want Facebook video downloads:

1. Run locally first:
   ```bash
   python get_facebook_cookies.py
   ```

2. Upload `facebook_cookies.txt` to your Space

3. Add another secret:
   - **Name**: `FACEBOOK_COOKIES`
   - **Value**: `/app/facebook_cookies.txt`

---

## 🔧 Troubleshooting

### "Bot doesn't respond"
- Check "Logs" tab in your Space
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Wait 2-3 minutes after deployment

### "Build failed"
- Make sure all 3 files are uploaded
- Check logs for error details
- Verify `requirements.txt` format

### "Bot keeps restarting"
- Check logs for errors
- May be rate limited (wait a few minutes)
- Verify bot token is correct

---

## 📊 Your Bot Features

Once deployed, your bot can:

- ✅ Convert text to speech (10+ languages)
- ✅ Process SRT subtitle files
- ✅ Download TikTok videos
- ✅ Download Facebook videos (with cookies)
- ✅ Download YouTube videos
- ✅ Run 24/7 on Hugging Face

---

## 🎯 Next Steps

1. **Deploy to Hugging Face** (follow steps above)
2. **Test all features** in Telegram
3. **Share with friends!**

**Create your Space now:** https://huggingface.co/spaces/create

Good luck! 🚀
