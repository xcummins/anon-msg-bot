# Anon Message Bot

A Telegram bot that enables users to send anonymous messages to others via referral links. Users who share their referral link can receive messages and reply to them anonymously. Additionally, the bot includes an admin panel for sending global messages to all users.

## Features

- **Anonymous Messaging**: Send messages to users who have shared their referral link without revealing your identity.
- **Referral Links**: Each user receives a unique referral link to share with others for anonymous messaging.
- **Admin Panel**: Admins can send global messages (e.g., ads) to all users.
- **SQLite Database**: User data and messages are stored in an SQLite database.

## Installation

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/anon-msg-bot.git
   cd anon-msg-bot
   chmod +x start.sh
   ./start.sh