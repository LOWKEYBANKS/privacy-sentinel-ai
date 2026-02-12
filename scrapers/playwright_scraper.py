from playwright.async_api import async_playwright
import trafilatura
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def scrape_dynamic_content(url: str) -> str:
    """
    Scrapes dynamic content from a given URL using Playwright's async API and extracts
    the main text content using Trafilatura.
    """
    logger.info(f"Attempting to scrape URL: {url} with Playwright (async)")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            # Wait for the page to load dynamic content, adjust as needed
            await page.wait_for_load_state("networkidle") 
            html_content = await page.content()
            await browser.close()
            
            logger.info("Playwright successfully fetched HTML content. Now extracting with Trafilatura.")
           extracted_text = trafilatura.extract(html_content, include_comments=False, include_tables=False)

            
            if not extracted_text:
                logger.warning(f"Trafilatura extraction failed for {url}. Falling back to raw HTML.")
                return html_content
            
            logger.info(f"Successfully extracted content from {url} using Trafilatura.")
            return extracted_text
    except Exception as e:
        logger.error(f"Error scraping {url} with Playwright: {e}")
        return ""

if __name__ == "__main__":
    import asyncio
    async def main():
        test_url = "https://www.example.com"
        print(f"Scraping {test_url}...")
        content = await scrape_dynamic_content(test_url)
        if content:
            print(f"Content length: {len(content)} characters")
            print(content[:500]) # Print first 500 characters
        else:
            print("Failed to retrieve content.")
    asyncio.run(main())
