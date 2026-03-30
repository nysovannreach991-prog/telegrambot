# 📘 How to Download Private Facebook Videos

## Problem
The Facebook video you want to download is **private** and requires Facebook login.

## Solution: Extract Facebook Cookies

### Step 1: Log into Facebook
1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to https://www.facebook.com
3. Log in to your Facebook account
4. Keep the browser open

### Step 2: Extract Cookies
Run this command in your terminal:

```bash
cd "/Users/reach/Desktop/Telegram Bot for AI Translation"
python get_facebook_cookies.py
```

The script will:
- Find Facebook cookies from your browser
- Save them to `facebook_cookies.txt`
- Update your `.env` file automatically

### Step 3: Restart the Bot
```bash
# Stop the current bot (press Ctrl+C)
python bot.py
```

### Step 4: Try Again
Send the Facebook video link to your bot again!

---

## ⚠️ Important Notes

1. **Cookies Expire**: Facebook cookies expire after a few days/weeks. Re-run the script if downloads stop working.

2. **Security**: The cookies file contains your Facebook session. Don't share it with anyone!

3. **Only for Private Videos**: You don't need cookies for:
   - ✅ Public Facebook videos
   - ✅ Public Facebook pages
   - ✅ YouTube videos
   - ✅ TikTok videos

4. **Browser Requirement**: You must be logged into Facebook in your browser when running the script.

---

## Troubleshooting

### "Could not find Facebook cookies"
- Make sure you're logged into Facebook in your browser
- Try a different browser (Chrome, Firefox, Edge)
- Refresh Facebook and try again

### "Downloads still don't work"
- Cookies may have expired
- Re-run `python get_facebook_cookies.py`
- Restart the bot

### Manual Setup
If the script doesn't update `.env` automatically:

1. Open `.env` file
2. Add this line:
   ```
   FACEBOOK_COOKIES=/full/path/to/facebook_cookies.txt
   ```
3. Save and restart the bot

---

## Alternative: Use Public Videos

If you don't want to use cookies, only download **public** Facebook videos:
- Videos from public pages
- Videos with public privacy settings
- fb.watch links (if public)
