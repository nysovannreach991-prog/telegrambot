# Telegram Bot with Edge TTS

A Telegram bot that converts text messages to speech using Microsoft Edge's Text-to-Speech (TTS) service.

## Features

- 🎤 Convert text to natural-sounding speech
- 🌍 Support for multiple languages (English, Khmer, Thai, Chinese, Japanese, Korean, French, German, Spanish)
- 🔧 Customizable voice settings
- 📱 Easy to use - just send a text message

## Supported Languages

| Code | Language | Voice |
|------|----------|-------|
| `en` | English (US) | Aria |
| `en-uk` | English (UK) | Sonia |
| `kh` | Khmer | Piseth |
| `th` | Thai | Premwadee |
| `zh` | Chinese | Xiaoxiao |
| `ja` | Japanese | Nanami |
| `ko` | Korean | SunHi |
| `fr` | French | Denise |
| `de` | German | Amala |
| `es` | Spanish | Elvira |

## Setup Instructions

### 1. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided by BotFather

### 2. Clone or Download This Project

Make sure you have Python 3.8+ installed on your system.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Bot

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Edit the `.env` file and add your bot token:

```
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
```

### 5. Run the Bot

```bash
python bot.py
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see welcome message |
| `/help` | Show help message with all commands |
| `/voice` | List available voices |
| `/voice <lang>` | Change voice (e.g., `/voice kh` for Khmer) |
| `/settings` | Show current TTS settings |

## Usage

1. Start a chat with your bot on Telegram
2. Send any text message
3. The bot will respond with a voice message reading your text

### Examples

- Send: "Hello, how are you?"
- Bot responds with: English voice message

- Send: `/voice kh`
- Bot changes to: Khmer voice

- Send: "សួស្តី" (after setting Khmer voice)
- Bot responds with: Khmer voice message

## Project Structure

```
Telegram Bot for AI Translation/
├── bot.py              # Main bot script
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment file
├── .env               # Your configuration (create this)
└── README.md          # This file
```

## Troubleshooting

### Bot doesn't respond
- Make sure the bot is running (`python bot.py`)
- Check if the bot token is correct in `.env`
- Ensure you have installed all dependencies

### Voice generation fails
- Check your internet connection (Edge TTS requires online access)
- Try a different voice/language
- Make sure the text is not too long

### Khmer voice doesn't sound right
- Make sure you've set the Khmer voice using `/voice kh`
- Khmer text should be properly encoded in Unicode

## Requirements

- Python 3.8+
- Telegram Bot Token
- Internet connection (for Edge TTS API)

## Dependencies

- `python-telegram-bot` - Telegram Bot API wrapper
- `edge-tts` - Microsoft Edge TTS integration
- `python-dotenv` - Environment variable management

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues, please check:
1. The bot is running
2. Your bot token is correct
3. All dependencies are installed
4. You have an active internet connection

---

Made with ❤️ using Edge TTS
