from dataclasses import dataclass, field
from typing import Optional
import re
from datetime import datetime
import json
@dataclass
class Reviewer:
    name: str
    title: Optional[str] = None
    badge: Optional[str] = None
    num_review: Optional[int] = None
    num_photos: Optional[int] = None
    invalid_format: Optional[list] = field(default_factory=list)
    
    def match(self, text:str):
        if "reviews" in text:
            self.num_review = int(text.strip().split(" ")[0])
        elif "photo" in text:
            self.num_photos = int(text.strip().split(" ")[0])
        elif "local guide" in text:
            self.title = text.strip().title()
            
        else:
            print(f"Unknown text format: {text}")
            self.invalid_format.append(text.title())
            
    def extract_badge_tier(self, text: str):
        badge = re.search(r"ba(\d+)", text)
        if badge:
            self.badge = badge.group(0)
        else:
            self.badge = None
            
    def str2profile(self, profile: str):
        """Convert a string to a profile object"""
        parts = profile.split("·")
        for part in parts:
            self.match(part.lower())
        
@dataclass
class Review:
    reviewer: Reviewer
    rating: float
    scrape_date = datetime.now()
    review_date: str
    text: str
    num_likes: Optional[int] = None
    visited_on:Optional[str] = None
    wait_time:Optional[str] = None
    reservation_recommendation:Optional[str] = None
    
@dataclass
class GoogleMapReview:
    url: str
    reviews: list[Review] = field(default_factory=list)
    
    def add_review(self, review: Review):
        self.reviews.append(review)
        
    def to_json(self):
        """Convert the reviews to JSON format"""
        return json.dumps([review.__dict__ for review in self.reviews], default=str)
        