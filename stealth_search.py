
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def stealth_search(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Apply stealth
        await Stealth().apply_stealth_async(page)
        
        print(f"Searching for: {query}")
        try:
            await page.goto(f"https://duckduckgo.com/?q={query}", wait_until="networkidle")
            
            title = await page.title()
            print(f"Page Title: {title}")
            
            # Wait for results on DuckDuckGo
            try:
                await page.wait_for_selector("div.results--main", timeout=10000)
            except Exception as e:
                print(f"Could not find results: {e}")
                content = await page.content()
                print(f"Content snippet: {content[:1000]}")
                return

            # Extract some results
            results = await page.evaluate('''() => {
                const items = Array.from(document.querySelectorAll('article'));
                return items.slice(0, 3).map(item => {
                    const titleEl = item.querySelector('h2');
                    const linkEl = item.querySelector('a');
                    return {
                        title: titleEl ? titleEl.innerText : 'No Title',
                        link: linkEl ? linkEl.href : 'No Link'
                    };
                });
            }''')
            
            for i, res in enumerate(results):
                print(f"{i+1}. {res['title']} - {res['link']}")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "Obscura headless browser"
    asyncio.run(stealth_search(query))
