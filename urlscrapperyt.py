import asyncio
import pandas as pd
from playwright.async_api import async_playwright

# Configuration
MAX_TAGS = 4           # Number of tags to extract from the video
VIDEOS_PER_TAG = 2     # Number of videos to scrape per tag
OUTPUT_CSV = "tag_search_results.csv"

async def get_video_tags(page):
    tag_element = await page.query_selector('meta[name="keywords"]')
    if tag_element:
        content = await tag_element.get_attribute("content")
        if content:
            tags = [tag.strip() for tag in content.split(",") if tag.strip()]
            print(f"[INFO] Found tags: {tags[:MAX_TAGS]}")
            return tags[:MAX_TAGS]
    print("[WARNING] No tags found.")
    return []

async def search_youtube_for_tag(tag, page, max_results=VIDEOS_PER_TAG):
    search_url = f"https://www.youtube.com/results?search_query={tag.replace(' ', '+')}"
    await page.goto(search_url, timeout=60000)
    await page.wait_for_selector("ytd-video-renderer", timeout=10000)

    results = []
    elements = await page.query_selector_all("ytd-video-renderer a#video-title")

    for el in elements:
        title = await el.get_attribute("title")
        href = await el.get_attribute("href")
        if title and href and "/watch" in href:
            results.append({
                "search_tag": tag,
                "title": title.strip(),
                "url": f"https://www.youtube.com{href.strip()}"
            })
            if len(results) >= max_results:
                break

    return results

async def scrape_by_tags(video_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("[STEP] Visiting video page...")
        await page.goto(video_url, timeout=60000)

        # Step 1: Get tags
        tags = await get_video_tags(page)

        # Step 2: Search for videos per tag
        all_results = []
        for tag in tags:
            print(f"[SEARCH] Searching for tag: {tag}")
            tag_results = await search_youtube_for_tag(tag, page)
            all_results.extend(tag_results)

        await browser.close()

        # Step 3: Save to CSV
        if all_results:
            df = pd.DataFrame(all_results)
            df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
            print(f"[SUCCESS] Saved {len(df)} results to '{OUTPUT_CSV}'")
        else:
            print("[INFO] No videos found.")

if __name__ == "__main__":
    try:
        video_url = input("Enter the YouTube video URL: ")
        asyncio.run(scrape_by_tags(video_url))
    except Exception as e:
        print(f"[ERROR] {e}")
