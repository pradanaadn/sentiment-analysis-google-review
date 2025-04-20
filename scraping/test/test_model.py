import pytest
from datetime import datetime
import json
from model import Reviewer, Review, GoogleMapReview


@pytest.fixture
def reviewer():
    return Reviewer(name="Alice")

def make_review(name="Alice", rating=4.5, review_date="2025-04-19", text="Great place!", num_likes=2):
    reviewer = Reviewer(name=name)
    return Review(
        reviewer=reviewer,
        rating=rating,
        review_date=review_date,
        text=text,
        num_likes=num_likes
    )
    
def test_match_num_review(reviewer):
    reviewer.match("123 reviews")
    assert reviewer.num_review == 123
    assert reviewer.num_photos is None
    assert reviewer.title is None


def test_match_num_photos(reviewer):
    reviewer.match("45 photos")
    assert reviewer.num_photos == 45
    assert reviewer.num_review is None
    assert reviewer.title is None


def test_match_local_guide(reviewer):
    reviewer.match("local guide")
    assert reviewer.title == "Local Guide"


def test_match_unknown_format(capsys, reviewer):
    reviewer.match("unexpected text")
    captured = capsys.readouterr()
    assert "Unknown text format: unexpected text" in captured.out
    assert reviewer.invalid_format == ["Unexpected Text"]


def test_extract_badge_tier_matches(reviewer):
    url = "https://lh3.googleusercontent.com/.../mo-ba4-br100"
    reviewer.extract_badge_tier(url)
    assert reviewer.badge == "ba4"


def test_extract_badge_tier_no_matches(reviewer):
    url = "https://lh3.googleusercontent.com/.../mo-br100"
    reviewer.extract_badge_tier(url)
    assert reviewer.badge is None


def test_str2profile_combined():
    r = Reviewer(name="Bob")
    profile = "Local Guide · 200 reviews · 50 photos"
    r.str2profile(profile)
    assert r.title == "Local Guide"
    assert r.num_review == 200
    assert r.num_photos == 50


def test_str2profile_invalid_combined():
    r = Reviewer(name="Bob")
    profile = "International Guide · 200 follower · 50 videos"
    r.str2profile(profile)
    assert r.invalid_format == ["International Guide ", " 200 Follower ", " 50 Videos"]


def test_review_dataclass_fields():
    r = Reviewer(name="Carol")
    review_date = "2025-04-20"
    review = Review(reviewer=r, rating=4.5, review_date=review_date, text="Great!")
    assert isinstance(review.scrape_date, datetime)
    assert review.reviewer is r
    assert review.rating == 4.5
    assert review.review_date == review_date
    assert review.text == "Great!"
    assert review.num_likes is None

def test_add_review_and_to_json():
    scraper = GoogleMapReview(url="https://example.com")
    r1 = make_review()
    r2 = make_review(name="Bob", rating=3.0, review_date="2025-04-20", text="It was ok", num_likes=None)
    scraper.add_review(r1)
    scraper.add_review(r2)

    json_str = scraper.to_json()
    data = json.loads(json_str)
    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["rating"] == 4.5
    assert data[0]["text"] == "Great place!"
    assert data[0]["review_date"] == "2025-04-19"
    assert data[0]["num_likes"] == 2

    assert data[1]["rating"] == 3.0
    assert data[1]["text"] == "It was ok"
    assert data[1]["review_date"] == "2025-04-20"
    assert data[1]["num_likes"] is None