from dotenv import load_dotenv
from telethon import TelegramClient, events
import requests
import os

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
source_channel = os.getenv('SOURCE_CHANNEL')
target_channel = os.getenv('TARGET_CHANNEL')
webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message_text = event.message.message  # Get the text from the message

    # Send to target Telegram channel
    await client.send_message(target_channel, message_text)

    # Send to Discord channel via webhook
    if message_text:  # check if the message is not empty
        data = {
            "content": message_text
        }
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
            print(f"Sent message to Discord: {message_text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending to Discord: {e}")

async def main():
    await client.start()
    print("Listening for messages...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
