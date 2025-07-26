# btc_notifier.py

import requests
import time
from plyer import notification

# --- CONFIGURATION ---
# Set the price (in INR) at which you want to be notified.
# Example: Notify me when Bitcoin is over ₹6,000,000
TARGET_PRICE = 6000000

def get_btc_price():
    """Fetches the current price of Bitcoin in INR from the CoinGecko API."""
    try:
        # API URL for Bitcoin price in INR
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=inr"
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
        
        # Extract the price from the JSON response
        data = response.json()
        price = float(data['bitcoin']['inr'])
        return price
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except (KeyError, ValueError):
        print("Error: Could not parse price data.")
        return None

def send_notification(title, message):
    """Sends a desktop notification."""
    notification.notify(
        title=title,
        message=message,
        app_name='BTC Notifier',
        timeout=10  # Notification will stay for 10 seconds
    )
    print("Notification sent!")

if __name__ == "__main__":
    print("🚀 Bitcoin Price Notifier Started...")
    print(f"Will notify when price exceeds: ₹{TARGET_PRICE:,.2f}")

    while True:
        current_price = get_btc_price()

        if current_price is not None:
            print(f"Checked at {time.strftime('%H:%M:%S')}: Current Price = ₹{current_price:,.2f}")

            # Check if the current price is above our target
            if current_price > TARGET_PRICE:
                notification_title = "🎉 Bitcoin Price Alert! 🎉"
                notification_message = (
                    f"Bitcoin has hit ₹{current_price:,.2f}!\n"
                    f"Your target was ₹{TARGET_PRICE:,.2f}."
                )
                send_notification(notification_title, notification_message)
                print("Target reached. Exiting script.")
                break  # Exit the loop after sending notification

        # Wait for 10 minutes (600 seconds) before checking again
        print("Checking again in 10 minutes...")
        time.sleep(600)
