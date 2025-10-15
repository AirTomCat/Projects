<div align="center">

⏳ Age Unraveled ⏳

A tiny Python script to see your age in a whole new light!

Created by AirTomCat

</div>

Ever wondered exactly how many months or even days you've been navigating planet Earth? Age Unraveled is a fun, simple command-line tool that takes your age in years and breaks it down into the total months and days you've lived.

It's a perfect little script for anyone curious about time, and it even accounts for those pesky leap years!

✨ Features

    ✅ Multi-dimensional View: Calculates your age in total months and total days.

    🧠 Leap Year Savvy: Intelligently handles leap years to ensure the day count is accurate.

    🚀 Zero Dependencies: Runs with standard Python libraries. No pip install needed!

    💬 Interactive & Simple: A friendly command-line prompt guides you through.

🚀 Getting Started

Ready to unravel your age? Just follow these simple steps.

    Get the Code:
    Clone this repository or simply download the calculate.py file.

    Open Your Terminal:
    Navigate to the directory where you saved the file.
    Bash

cd path/to/the/folder

Run the Script:
Execute the script using Python 3.
Bash

    python calculate.py

    Answer and Discover:
    The script will ask for your name and age. Type them in, press Enter, and see the magic!

👀 See It in Action

Here's what a typical run looks like. The output for months and days will change depending on the day you run it.
Bash

$ python calculate.py

input your name: Alex
input your age: 25
Alex's age is 25 years or 310 months or 9433 days

<details>
<summary>⚙️ <strong>Curious About How It Works?</strong></summary>

The script's logic is straightforward:

<ol>
<li>It first grabs the current date and time from your computer.</li>
<li>It estimates your birth year by subtracting your age from the current year.</li>
<li>It then meticulously loops through every single year from your estimated birth year to now, adding 365 days for a normal year and 366 for a leap year.</li>
<li>Finally, it adds the days from the months that have already passed in the current year to give you the grand total!</li>
</ol>
</details>
