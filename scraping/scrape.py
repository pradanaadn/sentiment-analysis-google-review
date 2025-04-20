from playwright.async_api import async_playwright
from adapter import ReviewSelector

class GoogleMapScraper:
    def __init__(self, headless: bool = False, slow_mo: int = 50):
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser = None
        self.page = None
        self.review_selector = None
    async def start(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
            args=["--lang=en-US"]
        )
        context = await self.browser.new_context(
            locale="en-US",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9"
            }
        )
        
        self.page = await context.new_page()
        self.review_selector = ReviewSelector(self.page)
        
    async def close(self):
        if self.browser:
            await self.browser.close()

    async def goto(self, url: str):
        url +="&hl=en"
        await self.page.goto(url)

    async def open_review_tab(self):
        try:
            await self.page.click('button[aria-label^="Reviews"]')
            await self.page.wait_for_timeout(3000)
            print("Successfully opened reviews tab")
        except Exception as e:
            print(f"Error opening reviews tab: {e}")
  
            
    async def extract_review(self):
        """Extract reviews from the current page and return them as structured data"""
        reviews = []

        # Find all review elements
        review_elements = await self.review_selector.get_review_elements()
        print(f"Found {len(review_elements)} reviews")

        for review_el in review_elements:
            try:
                more_btn = await review_el.query_selector(".w8nwRe")
                if more_btn:
                    print("Clicking 'More' button to load full review text")
                    
                    await more_btn.click()
                    await self.page.wait_for_timeout(300)
                    
                name_el = await review_el.query_selector(".d4r55")
                name = await name_el.text_content() if name_el else "Unknown"

                # Extract rating
                rating_el = await review_el.query_selector(".kvMYJc")
                rating = None
                if rating_el:
                    aria_label = await rating_el.get_attribute("aria-label")
                    if aria_label:
                        try:
                            rating_parts = aria_label.split(" ")
                            if len(rating_parts) > 1:
                                rating = float(rating_parts[0])
                        except (ValueError, IndexError):
                            pass

                # Extract review text
                text_el = await review_el.query_selector(".wiI7pd")
                text = await text_el.text_content() if text_el else ""

                # Extract time/date
                time_el = await review_el.query_selector(".rsqaWe")
                time = await time_el.text_content() if time_el else ""

                # Add review to our list
                review_data = {
                    "name": name,
                    "rating": rating,
                    "text": text,
                    "time": time,
                }
                reviews.append(review_data)

            except Exception as e:
                print(f"Error extracting review data: {e}")

        print(f"Successfully extracted {len(reviews)} reviews")
        print(reviews)
    async def load_more_reviews(self):
        await self.page.evaluate('window.scrollBy(0,1000)')
        await self.page.wait_for_timeout(1000)
    
    async def scrape(self, url: str, num_reviws: int = 11):
        await self.start()
        await self.goto(url)
        await self.open_review_tab()
        
        
        await self.extract_review()
        await self.load_more_reviews()
        await self.extract_review()
        await self.close()