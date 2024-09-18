
# Telegram Bot with OpenAI Assistant

This project implements a Telegram bot that leverages OpenAI's Assistant APIs. The bot is designed to handle requests interactively with a rate limiting to enhance user interaction.

## Getting Started

These instructions will guide you through setting up the project on your local machine for development and testing purposes.

### Prerequisites

You need Python 3.8+ installed on your machine. You will also need `pip` to install the required packages.

### Installation

Follow these steps to get your development environment running:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/akhatsuleimenov/tg-bot_openai-assistant.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd tg-bot_openai-assistant
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Environment Variables:**
   Create a `.env` file in the root directory and populate it with your Telegram bot token and OpenAI API key:
   ```plaintext
   TG_BOT_TOKEN='your_telegram_bot_token_here'
   OPENAI_API_KEY='your_openai_api_key_here'
   ```

### Running the Bot

Execute the following command to start the bot:

```bash
python main.py
```

This will activate the bot, and you can start interacting with it using predefined commands or by sending messages directly.

## Features

- **Intelligent Conversation**: Utilizes OpenAI's GPT-4.0 mini to generate context-aware responses.
- **Rate Limiting**: Prevents abuse by limiting the number of requests a user can make per unit time.
- **Session Management**(Soon): Handles messages that are too long and splits them into manageable parts, maintaining the context across multiple messages.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- OpenAI for providing the GPT-4 API.
- The developers and contributors of the `aiogram` library.
