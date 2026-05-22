import json

from sqlalchemy.orm import Session

from app.models.source import Source
from app.repositories.category_repository import DEFAULT_CATEGORIES, CategoryRepository


SOURCES = [
    {"name": "Netflix TechBlog", "company": "Netflix", "base_url": "https://netflixtechblog.com", "feed_url": "https://netflixtechblog.com/feed", "sitemap_url": None, "allowed_domains": ["netflixtechblog.com"], "crawl_mode": "feed", "enabled": True},
    {"name": "Uber Blog: Engineering", "company": "Uber", "base_url": "https://www.uber.com/us/en/blog/engineering/", "feed_url": None, "sitemap_url": None, "allowed_domains": ["www.uber.com", "eng.uber.com"], "crawl_mode": "html_index", "enabled": True},
    {"name": "The Cloudflare Blog", "company": "Cloudflare", "base_url": "https://blog.cloudflare.com", "feed_url": "https://blog.cloudflare.com/rss/", "sitemap_url": None, "allowed_domains": ["blog.cloudflare.com"], "crawl_mode": "feed", "enabled": True},
    {"name": "Engineering at Meta", "company": "Meta", "base_url": "https://engineering.fb.com", "feed_url": "https://engineering.fb.com/feed/", "sitemap_url": None, "allowed_domains": ["engineering.fb.com"], "crawl_mode": "feed", "enabled": True},
    {"name": "LinkedIn Engineering", "company": "LinkedIn", "base_url": "https://www.linkedin.com/blog/engineering", "feed_url": "https://engineering.linkedin.com/blog.rss", "sitemap_url": None, "allowed_domains": ["www.linkedin.com", "engineering.linkedin.com"], "crawl_mode": "feed", "enabled": True},
    {"name": "AWS Architecture Blog", "company": "AWS", "base_url": "https://aws.amazon.com/blogs/architecture/", "feed_url": "https://aws.amazon.com/blogs/architecture/feed/", "sitemap_url": None, "allowed_domains": ["aws.amazon.com"], "crawl_mode": "feed", "enabled": True},
    {"name": "Stripe Blog: Engineering", "company": "Stripe", "base_url": "https://stripe.com/blog/engineering", "feed_url": "https://stripe.com/blog/feed.rss", "sitemap_url": None, "allowed_domains": ["stripe.com"], "crawl_mode": "feed", "enabled": True},
    {"name": "Discord Blog: Engineering & Developers", "company": "Discord", "base_url": "https://discord.com/category/engineering", "feed_url": None, "sitemap_url": None, "allowed_domains": ["discord.com"], "crawl_mode": "html_index", "enabled": True},
    {"name": "Slack Engineering", "company": "Slack", "base_url": "https://slack.engineering", "feed_url": "https://slack.engineering/feed", "sitemap_url": None, "allowed_domains": ["slack.engineering"], "crawl_mode": "feed", "enabled": True},
]


def seed_categories_and_sources(db: Session) -> None:
    CategoryRepository(db).seed_defaults()
    if db.query(Source).count() == 0:
        for source in SOURCES:
            payload = source.copy()
            payload["allowed_domains"] = json.dumps(payload["allowed_domains"])
            db.add(Source(**payload))
        db.commit()


__all__ = ["DEFAULT_CATEGORIES", "SOURCES", "seed_categories_and_sources"]
