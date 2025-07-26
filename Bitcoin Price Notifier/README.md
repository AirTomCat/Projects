# Bitcoin Price Notifier 🚀

This Python script monitors the live price of Bitcoin and sends a desktop notification when its value surpasses a user-defined target. It uses the free **CoinGecko API** to fetch real-time price data in Indian Rupees (INR) and the **`plyer`** library to deliver cross-platform notifications.

---

## Features

-   **Live Price Tracking:** Fetches the current price of Bitcoin.
-   **Desktop Notifications:** Sends a native desktop alert that works on Windows, macOS, and Linux.
-   **Customizable Target:** Easily set the price threshold at which you want to be notified.
-   **Periodic Checks:** Runs in the background and checks the price every 10 minutes by default.
-   **Lightweight:** A simple script that runs directly from your terminal.

---

## Requirements

-   Python 3.x
-   `requests` library
-   `plyer` library

---

## Installation & Setup

1.  **Get the Code:**
    Download the `btc_notifier.py` script to a folder on your computer.

2.  **Install Dependencies:**
    Open your terminal or command prompt and run the following command to install the necessary libraries:
    ```bash
    pip install requests plyer
    ```

---

## How to Use

1.  **Set Your Target Price:**
    Open the `btc_notifier.py` file in any text editor. Find this line near the top and change the value to your desired target price in INR:
    ```python
    TARGET_PRICE = 6000000
    ```

2.  **Run the Script:**
    Navigate to the script's directory in your terminal and execute the following command:
    ```bash
    python btc_notifier.py
    ```

3.  **Wait for Notifications:**
    The script will start running. You can minimize the terminal window. It will print the current price every 10 minutes. Once the live price of Bitcoin exceeds your target, a desktop notification will appear automatically, and the script will stop.
