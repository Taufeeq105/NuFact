# fetch_webpages.py
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch_webpage_text(session, url):
    """Fetches and extracts text from a webpage asynchronously."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                return url, text  # Return extracted text
            else:
                return url, f"Failed with status {response.status}"
    except asyncio.TimeoutError:
        return url, "Error: Timeout (Took too long to respond)"
    except Exception as e:
        return url, f"Error: {e}"

async def fetch_multiple_webpages(urls):
    """Fetches multiple webpages asynchronously given a list of URLs."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_webpage_text(session, url) for url in urls]
        return await asyncio.gather(*tasks)  # Run tasks concurrently

