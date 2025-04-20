from dataclasses import dataclass
from playwright.async_api import Page
@dataclass
class ReviewSelector:
    def __init__(self, page:Page):
        self.page = page
        
    async def get_review_elements(self):
        """Find all review elements"""
        return await self.page.query_selector_all(".jftiEf")
    
    async def get_data_review_id(self, review_el):
        """Find the data-review-id attribute in the review element"""
        el = await review_el.get_attribute("data-review-id")
        return el or ""
    
    async def get_image_link(self, review_el):
        """Find the image link in the review element"""
        el = await review_el.query_selector(".NBa7we")
        if el:
            img_src = await el.get_attribute("src")
            return img_src or ""
        return ""
    
    async def get_more_button(self, review_el):
        """Find the 'More' button in the review element"""
        el = await review_el.query_selector(".w8nwRe")
        return el
    
    async def get_reviewer_name(self, review_el):
        """Find the reviewer name in the review element"""
        el = await review_el.get_attribute("aria-label")
        return el or ""
    
    async def get_reviewer_information(self, review_el):
        """Find the reviewer information in the review element"""
        el = await review_el.query_selector(".RfnDt")
        if el:
            info = await el.text_content()
            return info.strip()
        return ""
        
    async def get_review_rating(self, review_el):
        """Find the review rating in the review element"""
        rating_element = await review_el.query_selector(".kvMYJc")
        if rating_element:
            el = await rating_element.get_attribute("aria-label")
            if el and el.startswith("Rated "):
                return el.split(" ")[1]
            return el or "0"
        return "0"
    
    async def get_review_date(self, review_el):
        """Find the review date in the review element"""
        date_element = await review_el.query_selector(".rsqaWe")
        if date_element:
            el = await date_element.text_content()
            return el.strip()
        return ""
    
    async def get_review_text(self, review_el):
        """Find the review text in the review element"""
        text_element = await review_el.query_selector(".wiI7pd")
        if text_element:
            el = await text_element.text_content()
            return el.strip()
        return ""
    
    async def get_review_likes(self, review_el):
        """Find the review likes in the review element"""
        likes_element = await review_el.query_selector(".GBkF3d")
        if likes_element:
            el = await likes_element.get_attribute("aria-label")
            if el and "thumbs up" in el:
                return el.split(" ")[0] or "0"
            return "0"
        return "0"