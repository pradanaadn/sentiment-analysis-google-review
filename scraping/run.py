import asyncio
from scrape import GoogleMapScraper


async def main():
    scraper = GoogleMapScraper()
    await scraper.start()
    await scraper.goto("https://www.google.com/maps/place/Monas/@-6.1753871,106.8245779,17z/data=!3m1!4b1!4m6!3m5!1s0x2e69f5d2e764b12d:0x3d2ad6e1e0e9bcc8!8m2!3d-6.1753924!4d106.8271528!16zL20vMDNxN2hz?entry=ttu&g_ep=EgoyMDI1MDQxNi4xIKXMDSoASAFQAw%3D%3D")
    await scraper.open_review_tab()
    await scraper.extract_review()

if __name__ == "__main__":
    asyncio.run(main())