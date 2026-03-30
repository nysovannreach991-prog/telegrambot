#!/usr/bin/env python3
"""
Telegram Bot with Edge TTS Integration
Converts text messages to speech using Microsoft Edge TTS
"""

import os
import asyncio
import tempfile
import re
import yt_dlp
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
import edge_tts
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FACEBOOK_COOKIES = os.getenv("FACEBOOK_COOKIES")

# Default TTS settings
DEFAULT_VOICE = "en-US-AriaNeural"  # Default voice
DEFAULT_RATE = "+0%"  # Default speech rate
DEFAULT_VOLUME = "+0%"  # Default volume
DEFAULT_PITCH = "+0Hz"  # Default pitch

# SRT processing settings
MAX_SRT_SUBTITLES = 50  # Maximum number of subtitles to process
SRT_DELAY_BETWEEN = 0.5  # Delay between subtitle processing (seconds)

# Video download settings
MAX_VIDEO_DURATION = 600  # Maximum video duration in seconds (10 minutes)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB (Telegram limit for bots)


# Available voices with gender info
AVAILABLE_VOICES = {
    "en": {"voice": "en-US-AriaNeural", "gender": "Female", "label": "🇺🇸 English (F)"},
    "en-uk": {"voice": "en-GB-SoniaNeural", "gender": "Female", "label": "🇬🇧 English UK (F)"},
    "en-uk-m": {"voice": "en-GB-RyanNeural", "gender": "Male", "label": "🇬🇧 English UK (M)"},
    "kh": {"voice": "km-KH-SreymomNeural", "gender": "Female", "label": "🇰🇭 Khmer (F)"},
    "kh-m": {"voice": "km-KH-PisethNeural", "gender": "Male", "label": "🇰🇭 Khmer (M)"},
    "th": {"voice": "th-TH-PremwadeeNeural", "gender": "Female", "label": "🇹🇭 Thai (F)"},
    "th-m": {"voice": "th-TH-NiwatNeural", "gender": "Male", "label": "🇹🇭 Thai (M)"},
    "zh": {"voice": "zh-CN-XiaoxiaoNeural", "gender": "Female", "label": "🇨🇳 Chinese (F)"},
    "zh-m": {"voice": "zh-CN-YunxiNeural", "gender": "Male", "label": "🇨🇳 Chinese (M)"},
    "ja": {"voice": "ja-JP-NanamiNeural", "gender": "Female", "label": "🇯🇵 Japanese (F)"},
    "ja-m": {"voice": "ja-JP-KeitaNeural", "gender": "Male", "label": "🇯🇵 Japanese (M)"},
    "ko": {"voice": "ko-KR-SunHiNeural", "gender": "Female", "label": "🇰🇷 Korean (F)"},
    "ko-m": {"voice": "ko-KR-InJoonNeural", "gender": "Male", "label": "🇰🇷 Korean (M)"},
    "fr": {"voice": "fr-FR-DeniseNeural", "gender": "Female", "label": "🇫🇷 French (F)"},
    "fr-m": {"voice": "fr-FR-HenriNeural", "gender": "Male", "label": "🇫🇷 French (M)"},
    "de": {"voice": "de-DE-AmalaNeural", "gender": "Female", "label": "🇩🇪 German (F)"},
    "de-m": {"voice": "de-DE-ConradNeural", "gender": "Male", "label": "🇩🇪 German (M)"},
    "es": {"voice": "es-ES-ElviraNeural", "gender": "Female", "label": "🇪🇸 Spanish (F)"},
    "es-m": {"voice": "es-ES-AlvaroNeural", "gender": "Male", "label": "🇪🇸 Spanish (M)"},
}


async def generate_speech(text: str, voice: str = DEFAULT_VOICE) -> str:
    """
    Generate speech audio from text using Edge TTS

    Args:
        text: Text to convert to speech
        voice: Voice to use for TTS

    Returns:
        Path to the generated audio file
    """
    # Create a temporary file for the audio
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.close()

    print(f"🎤 Generating speech: text='{text[:50]}...', voice='{voice}'")

    try:
        # Initialize Edge TTS
        communicate = edge_tts.Communicate(text, voice)

        # Generate and save the audio
        await communicate.save(temp_file.name)
        
        # Check if file was created
        file_size = os.path.getsize(temp_file.name)
        print(f"✅ Audio file created, size: {file_size} bytes")
        
        if file_size == 0:
            os.unlink(temp_file.name)
            raise Exception("Empty audio file generated")

        return temp_file.name
    except Exception as e:
        # Clean up on error
        try:
            os.unlink(temp_file.name)
        except:
            pass
        raise e


def parse_srt_file(file_path: str) -> list:
    """
    Parse SRT subtitle file and extract text with timestamps
    
    Args:
        file_path: Path to the SRT file
        
    Returns:
        List of dictionaries with index, start_time, end_time, and text
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # SRT pattern: index, timestamp, text
    srt_pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\n*$)'
    matches = re.findall(srt_pattern, content, re.DOTALL)
    
    subtitles = []
    for match in matches:
        index, start_time, end_time, text = match
        # Clean up text (remove HTML tags, special characters)
        clean_text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        clean_text = clean_text.replace('\n', ' ').strip()
        
        if clean_text:
            subtitles.append({
                'index': int(index),
                'start_time': start_time,
                'end_time': end_time,
                'text': clean_text
            })
    
    return subtitles[:MAX_SRT_SUBTITLES]  # Limit number of subtitles


async def process_srt_file(file_path: str, voice: str) -> list:
    """
    Process SRT file and generate audio for each subtitle
    
    Args:
        file_path: Path to the SRT file
        voice: Voice to use for TTS
        
    Returns:
        List of audio file paths
    """
    subtitles = parse_srt_file(file_path)
    audio_files = []
    
    print(f"📝 Processing {len(subtitles)} subtitles...")
    
    for sub in subtitles:
        try:
            audio_file = await generate_speech(sub['text'], voice)
            audio_files.append({
                'text': sub['text'],
                'audio_file': audio_file,
                'start_time': sub['start_time'],
                'end_time': sub['end_time']
            })
            await asyncio.sleep(SRT_DELAY_BETWEEN)  # Avoid rate limiting
        except Exception as e:
            print(f"❌ Error processing subtitle {sub['index']}: {e}")
    
    return audio_files


def is_video_url(text: str) -> bool:
    """Check if text is a video URL from supported platforms."""
    video_patterns = [
        r'(https?://)?(www\.)?(tiktok\.com|vm\.tiktok\.com|vt\.tiktok\.com)/\S+',
        r'(https?://)?(www\.)?(facebook\.com|fb\.watch)/\S+',
        r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/\S+',
        r'(https?://)?(m\.)?(facebook\.com)/\S+',
    ]
    
    for pattern in video_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


async def download_video(url: str) -> dict:
    """
    Download video from TikTok, Facebook, or YouTube
    
    Args:
        url: Video URL
        
    Returns:
        Dictionary with video info and file path
    """
    temp_dir = tempfile.mkdtemp()
    
    # Different format options for different platforms
    if 'tiktok.com' in url:
        # TikTok: more flexible format selection
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    elif 'facebook.com' in url or 'fb.watch' in url:
        # Facebook - with optional cookies for private videos
        ydl_opts = {
            'format': 'best[height<=480]/best',
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }
        # Add cookies if available
        if FACEBOOK_COOKIES:
            ydl_opts['cookiefile'] = FACEBOOK_COOKIES
    else:
        # YouTube and others
        ydl_opts = {
            'format': 'best[height<=720]/best',
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }
    
    loop = asyncio.get_event_loop()
    
    def _download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return info, filename
    
    info, filename = await loop.run_in_executor(None, _download)
    
    # Check file size
    file_size = os.path.getsize(filename)
    if file_size > MAX_FILE_SIZE:
        os.unlink(filename)
        raise Exception(f"File too large: {file_size / (1024*1024):.1f} MB (max: {MAX_FILE_SIZE / (1024*1024):.0f} MB)")
    
    # Check duration
    duration = info.get('duration', 0)
    if duration and duration > MAX_VIDEO_DURATION:
        os.unlink(filename)
        raise Exception(f"Video too long: {duration//60}m {duration%60}s (max: {MAX_VIDEO_DURATION//60} minutes)")
    
    return {
        'title': info.get('title', 'Unknown'),
        'duration': duration or 0,
        'filename': filename,
        'thumbnail': info.get('thumbnail'),
        'uploader': info.get('uploader', 'Unknown'),
        'platform': info.get('extractor', 'unknown')
    }


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"Hello {user.first_name}! 👋\n\n"
        "I'm a Telegram Bot with multiple capabilities.\n\n"
        "🎤 *Text to Speech:*\n"
        "• Send any text and I'll convert it to speech\n"
        "• Use /voice to select voice (Male/Female)\n\n"
        "📁 *SRT Subtitles:*\n"
        "• Send .srt files to generate voice for each subtitle\n\n"
        "📥 *Video Download:*\n"
        "• Send TikTok, Facebook, or YouTube links\n"
        "• I'll download and send the video back\n\n"
        "Use /help for more details!"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "*🤖 Bot Commands:*\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/voice - Select voice with inline menu\n"
        "/settings - Show current TTS settings\n\n"
        "*📁 Supported Files:*\n"
        "• Send *.srt* subtitle files to generate voice\n"
        "• Bot will process up to 50 subtitles per file\n\n"
        "*📥 Video Download:*\n"
        "• Send *TikTok* links (tiktok.com, vm.tiktok.com)\n"
        "• Send *Facebook* links (facebook.com, fb.watch)\n"
        "• Send *YouTube* links (youtube.com, youtu.be)\n"
        "• Max duration: 10 minutes\n"
        "• Max file size: 50 MB\n\n"
        "*💡 Tips:*\n"
        "• Send text for speech conversion\n"
        "• Use /voice to switch Male/Female voices\n"
        "• Supported TTS: 🇰🇭 Khmer, 🇺🇸 English, 🇹🇭 Thai, 🇨🇳 Chinese, 🇯🇵 Japanese, 🇰🇷 Korean, 🇫🇷 French, 🇩🇪 German, 🇪🇸 Spanish"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def voice_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show voice selection menu."""
    # Create inline keyboard with language options
    keyboard = []
    
    # Group voices by language
    languages = {}
    for key, info in AVAILABLE_VOICES.items():
        lang = key.split('-')[0] if '-m' not in key else key.replace('-m', '')
        if lang not in languages:
            languages[lang] = []
        languages[lang].append((key, info))
    
    # Create buttons for each language
    for lang, voices in languages.items():
        row = []
        for key, info in voices:
            flag = info['label'].split()[0]
            gender = '👩' if info['gender'] == 'Female' else '👨'
            row.append(InlineKeyboardButton(f"{flag} {gender}", callback_data=f"voice_{key}"))
        keyboard.append(row)
    
    # Add a close button
    keyboard.append([InlineKeyboardButton("❌ Close", callback_data="close")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    current_voice = context.user_data.get("voice", DEFAULT_VOICE)
    current_label = next((info['label'] for info in AVAILABLE_VOICES.values() if info['voice'] == current_voice), "Unknown")
    
    await update.message.reply_text(
        f"🎤 *Select Voice:*\n\nCurrent: *{current_label}*\n\n"
        f"Tap a button to change voice:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def voice_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle voice selection from inline keyboard."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "close":
        await query.message.delete()
        return
    
    if data.startswith("voice_"):
        voice_key = data.replace("voice_", "")
        if voice_key in AVAILABLE_VOICES:
            voice_info = AVAILABLE_VOICES[voice_key]
            context.user_data["voice"] = voice_info["voice"]
            
            gender_emoji = "👩" if voice_info["gender"] == "Female" else "👨"
            await query.message.edit_text(
                f"✅ Voice changed to: *{voice_info['label']}* {gender_emoji}\n\n"
                f"Voice ID: `{voice_info['voice']}`",
                parse_mode="Markdown"
            )


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current TTS settings."""
    current_voice = context.user_data.get("voice", DEFAULT_VOICE)
    settings_text = (
        "*⚙️ Current TTS Settings:*\n\n"
        f"🎤 Voice: `{current_voice}`\n"
        f"📊 Rate: `{DEFAULT_RATE}`\n"
        f"🔊 Volume: `{DEFAULT_VOLUME}`\n"
        f"🎵 Pitch: `{DEFAULT_PITCH}`"
    )
    await update.message.reply_text(settings_text, parse_mode="Markdown")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages and convert them to speech or download videos."""
    text = update.message.text

    print(f"📩 Received text: '{text}'")

    if not text:
        return

    # Check if it's a video URL
    if is_video_url(text):
        await handle_video_url(update, context, text)
        return

    # Show typing action
    await update.message.chat.send_action(action="record_voice")

    # Get the user's preferred voice
    voice = context.user_data.get("voice", DEFAULT_VOICE)
    
    print(f"🎤 Using voice: {voice}")

    try:
        # Generate speech
        print(f"🎵 Generating speech...")
        audio_file = await generate_speech(text, voice)

        # Send the audio file as a voice message
        print(f"📤 Sending voice message...")
        with open(audio_file, "rb") as audio:
            await update.message.reply_voice(voice=audio)

        # Clean up the temporary file
        os.unlink(audio_file)
        print(f"✅ Voice message sent successfully!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        await update.message.reply_text(f"❌ Error generating speech: {str(e)}")


async def handle_video_url(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str) -> None:
    """Handle video URL and download the video."""
    print(f"🎬 Downloading video from: {url}")
    
    # Send processing message
    status_msg = await update.message.reply_text(
        "📥 Downloading video...\n"
        "⏳ Please wait..."
    )
    
    try:
        # Download the video
        video_info = await download_video(url)
        
        # Escape special characters for Markdown
        title = video_info['title'].replace('_', ' ').replace('*', ' ').replace('[', '(').replace(']', ')')
        uploader = video_info['uploader'].replace('_', ' ').replace('*', ' ')
        duration = video_info['duration']
        duration_text = f"{duration//60}m {duration%60}s" if duration else "Unknown"
        
        await status_msg.edit_text(
            f"🎬 *Video Found*\n\n"
            f"📝 Title: {title}\n"
            f"👤 Uploader: {uploader}\n"
            f"⏱️ Duration: {duration_text}\n\n"
            f"📤 Sending video...",
            parse_mode="Markdown"
        )
        
        # Send the video
        with open(video_info['filename'], "rb") as video:
            await update.message.reply_video(
                video=video,
                caption=f"🎬 {title[:100]}\n👤 {uploader[:50]}",
                supports_streaming=True
            )
        
        # Clean up
        os.unlink(video_info['filename'])
        await status_msg.delete()
        
        print(f"✅ Video sent successfully!")
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error downloading video: {error_msg}")
        
        # Check for specific error types
        if "registered users" in error_msg or "login" in error_msg.lower():
            await update.message.reply_text(
                "❌ *Facebook Video Error*\n\n"
                "This video requires Facebook login to download.\n"
                "Only public videos can be downloaded.\n\n"
                "💡 Try:\n"
                "• Public Facebook pages\n"
                "• Public Facebook videos\n"
                "• fb.watch links (public videos)",
                parse_mode="Markdown"
            )
        elif "Private" in error_msg:
            await update.message.reply_text(
                "❌ *Private Video*\n\n"
                "This video is private and cannot be downloaded.\n"
                "Only public videos are supported.",
                parse_mode="Markdown"
            )
        elif "TikTok" in error_msg and "not available" in error_msg:
            await update.message.reply_text(
                "❌ *TikTok Error*\n\n"
                "This video might be:\n"
                "• Private\n"
                "• Deleted\n"
                "• Region restricted\n\n"
                "Try a different TikTok video.",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                f"❌ *Download Error*\n\n"
                f"{error_msg[:200]}",
                parse_mode="Markdown"
            )
        
        try:
            await status_msg.delete()
        except:
            pass


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle document messages (SRT files)."""
    document = update.message.document
    
    # Check if it's an SRT file
    if not document.file_name.lower().endswith('.srt'):
        return
    
    print(f"📁 Received SRT file: {document.file_name}")
    
    # Get the user's preferred voice
    voice = context.user_data.get("voice", DEFAULT_VOICE)
    
    # Send processing message
    status_msg = await update.message.reply_text(
        "🔄 Processing SRT file...\n"
        "This may take a while depending on the number of subtitles.\n\n"
        "⏳ Please wait..."
    )
    
    try:
        # Download the file
        file = await context.bot.get_file(document.file_id)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.srt')
        await file.download_to_drive(temp_file.name)
        
        print(f"📥 File downloaded: {temp_file.name}")
        
        # Parse and process SRT
        subtitles = parse_srt_file(temp_file.name)
        print(f"📝 Found {len(subtitles)} subtitles")
        
        if not subtitles:
            await status_msg.edit_text("❌ No subtitles found in the file.")
            os.unlink(temp_file.name)
            return
        
        await status_msg.edit_text(
            f"📊 Found *{len(subtitles)}* subtitles\n"
            f"🎤 Voice: `{voice}`\n\n"
            f"⏳ Generating audio...",
            parse_mode="Markdown"
        )
        
        # Process each subtitle
        audio_files = []
        for i, sub in enumerate(subtitles, 1):
            try:
                print(f"🎵 Processing {i}/{len(subtitles)}: {sub['text'][:30]}...")
                audio_file = await generate_speech(sub['text'], voice)
                audio_files.append({
                    'text': sub['text'],
                    'audio_file': audio_file,
                    'start_time': sub['start_time']
                })
                
                # Update progress
                if i % 10 == 0 or i == len(subtitles):
                    await status_msg.edit_text(
                        f"📊 Progress: *{i}/{len(subtitles)}*\n"
                        f"⏳ Processing...",
                        parse_mode="Markdown"
                    )
                
                await asyncio.sleep(SRT_DELAY_BETWEEN)
            except Exception as e:
                print(f"❌ Error processing subtitle {i}: {e}")
        
        # Send all audio files
        await status_msg.edit_text(
            f"✅ Generated *{len(audio_files)}* audio files!\n"
            f"📤 Sending now...",
            parse_mode="Markdown"
        )
        
        # Send audio files in batches
        for i, audio_data in enumerate(audio_files, 1):
            try:
                with open(audio_data['audio_file'], "rb") as audio:
                    caption = f"{i}. {audio_data['text'][:100]}"
                    await update.message.reply_voice(
                        voice=audio,
                        caption=caption[:100]
                    )
                os.unlink(audio_data['audio_file'])
            except Exception as e:
                print(f"❌ Error sending audio {i}: {e}")
        
        await status_msg.edit_text(
            f"✅ *Complete!*\n"
            f"📊 Processed: *{len(audio_files)}/{len(subtitles)}* subtitles\n"
            f"🎤 Voice: `{voice}`",
            parse_mode="Markdown"
        )
        
        # Clean up
        os.unlink(temp_file.name)
        
    except Exception as e:
        print(f"❌ Error processing SRT: {str(e)}")
        await status_msg.edit_text(f"❌ Error processing SRT file: {str(e)}")
        try:
            os.unlink(temp_file.name)
        except:
            pass


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle voice messages (transcription not implemented in this basic version)."""
    await update.message.reply_text(
        "🎤 I received your voice message! \n\n"
        "Currently, I can only convert *text to speech*, not speech to text.\n"
        "Please send me a text message instead!",
        parse_mode="Markdown",
    )


def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in environment variables!")
        print("Please create a .env file with your bot token.")
        return

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("voice", voice_command))
    application.add_handler(CommandHandler("settings", settings_command))
    
    # Add callback handler for inline keyboard
    application.add_handler(CallbackQueryHandler(voice_selection_callback))

    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Start the bot
    print("🤖 Bot is starting...")
    print("📡 Press Ctrl+C to stop the bot")
    print("📁 SRT file processing enabled!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
