# Vidsrc-Movies-downloader
🎬 Vidsrc Movies Downloader

A powerful Python tool designed to automate the searching and downloading of movies using the Vidsrc API. This script handles the entire workflow: from querying a local database to asynchronous chunk downloading for maximum efficiency.
✨ Features

    Smart Search: Instantly find titles within a local Movies_vidsrc.json catalog using regex-based matching.

    Traffic Analysis: Leverages Selenium and BrowserMob Proxy to automatically sniff and capture the source master playlist URL (.m3u8).

    Asynchronous Downloading: Utilizes aiohttp and asyncio to download video segments in parallel batches, significantly reducing wait times.

    Auto-Merging: Automatically sorts and merges all downloaded chunks into a single, high-quality Movie.mp4 file.

🛠️ Prerequisites

Before running the script, ensure you have the following installed:

    Python 3.x

    GeckoDriver (for Firefox/Selenium)

    BrowserMob Proxy (essential for intercepting HTTP/HTTPS traffic)

Required Python Libraries:
Bash

pip install requests selenium browsermob-proxy aiohttp

🚀 Getting Started

    Configure the Proxy: In Vidsrc movies downloader.py, update the server = Server("...") line with the actual path to your BrowserMob Proxy bin folder.

    Prepare the Database: Ensure Movies_vidsrc.json is located in the same directory as the script.

    Run the Script:
    Bash

    python "Vidsrc movies downloader.py"

    Search & Download: Enter the movie name when prompted, select the correct match from the list, and let the script handle the rest.

⚠️ Legal Disclaimer

This project is for educational purposes only. The author is not responsible for any misuse of this tool. Please respect content providers' terms of service and local copyright laws.
