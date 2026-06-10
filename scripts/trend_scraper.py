#!/usr/bin/env python3
"""
Collect lightweight trend signals for meme ideation.

This script intentionally favors public, stable-ish sources first. X/Twitter is
kept behind an explicit optional adapter because direct scraping is brittle and
often requires account cookies, proxies, or paid scraping infrastructure.
"""

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from html import unescape
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


USER_AGENT = "meme-generator-skill/0.1 (+https://github.com/hyj-STAR/meme-generator.skill)"


@dataclass
class TrendItem:
    source: str
    title: str
    url: str
    score: str = ""
    summary: str = ""


def fetch_text(url: str, timeout: int = 20) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/json"})
    with urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


class GitHubTrendingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.in_article = False
        self.in_h2 = False
        self.in_p = False
        self.current = None
        self.buffer = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "")
        if tag == "article":
            self.in_article = True
            self.current = {"repo": "", "url": "", "summary": ""}
        elif self.in_article and tag == "h2":
            self.in_h2 = True
            self.buffer = []
        elif self.in_article and self.in_h2 and tag == "a":
            href = attrs.get("href", "")
            if href:
                self.current["url"] = f"https://github.com{href}"
        elif self.in_article and tag == "p" and "col-9" in classes:
            self.in_p = True
            self.buffer = []

    def handle_endtag(self, tag):
        if tag == "h2" and self.in_h2:
            repo = " ".join("".join(self.buffer).split())
            repo = repo.replace(" / ", "/").replace(" ", "")
            self.current["repo"] = repo
            self.in_h2 = False
        elif tag == "p" and self.in_p:
            self.current["summary"] = " ".join("".join(self.buffer).split())
            self.in_p = False
        elif tag == "article" and self.in_article:
            if self.current and self.current["repo"]:
                self.items.append(self.current)
            self.current = None
            self.in_article = False

    def handle_data(self, data):
        if self.in_h2 or self.in_p:
            self.buffer.append(data)


def scrape_github_trending(language: str = "", since: str = "daily", limit: int = 10) -> list[TrendItem]:
    path = f"/trending/{quote_plus(language)}" if language else "/trending"
    html = fetch_text(f"https://github.com{path}?since={since}")
    parser = GitHubTrendingParser()
    parser.feed(html)
    return [
        TrendItem(
            source="github_trending",
            title=item["repo"],
            url=item["url"],
            summary=item["summary"],
        )
        for item in parser.items[:limit]
    ]


def scrape_reddit(subreddit: str = "memes", sort: str = "hot", limit: int = 10) -> list[TrendItem]:
    url = f"https://www.reddit.com/r/{quote_plus(subreddit)}/{sort}.json?limit={limit}"
    raw = fetch_text(url)
    data = json.loads(raw)
    items = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        title = post.get("title", "").strip()
        permalink = post.get("permalink", "")
        score = str(post.get("score", ""))
        if title:
            items.append(
                TrendItem(
                    source=f"reddit/r/{subreddit}",
                    title=title,
                    url=f"https://www.reddit.com{permalink}",
                    score=score,
                    summary=post.get("selftext", "")[:180],
                )
            )
    return items


def scrape_x_placeholder(query: str, limit: int = 10) -> list[TrendItem]:
    try:
        from Scweet import Scweet  # type: ignore
    except Exception:
        print(
            "X adapter is not installed. Use GitHub/Reddit now, or install Scweet/Twikit and provide account auth.",
            file=sys.stderr,
        )
        return []

    import os

    auth_token = os.getenv("X_AUTH_TOKEN") or os.getenv("TWITTER_AUTH_TOKEN")
    if not auth_token:
        print("Set X_AUTH_TOKEN before using --source x.", file=sys.stderr)
        return []

    scraper = Scweet(auth_token=auth_token)
    tweets = scraper.search(query, limit=limit)
    items = []
    for tweet in tweets[:limit]:
        text = str(tweet.get("text") or tweet.get("content") or "").strip()
        url = str(tweet.get("url") or "")
        if text:
            items.append(TrendItem(source="x", title=text[:120], url=url, summary=text))
    return items


def meme_angles(items: list[TrendItem]) -> list[str]:
    angles = []
    for item in items:
        title = re.sub(r"\s+", " ", item.title)
        if not title:
            continue
        angles.append(f"看到「{title}」：表面很淡定 / 内心已经开始做梗图")
    return angles


def main():
    parser = argparse.ArgumentParser(description="Collect trend signals for meme generation")
    parser.add_argument("--source", choices=["github", "reddit", "x"], default="github")
    parser.add_argument("--query", default="", help="X search query or optional topic hint")
    parser.add_argument("--language", default="", help="GitHub Trending language")
    parser.add_argument("--since", default="daily", choices=["daily", "weekly", "monthly"])
    parser.add_argument("--subreddit", default="memes")
    parser.add_argument("--sort", default="hot", choices=["hot", "new", "top", "rising"])
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--angles", action="store_true", help="Also print meme angle drafts")
    args = parser.parse_args()

    started = time.strftime("%Y-%m-%d")
    if args.source == "github":
        items = scrape_github_trending(args.language, args.since, args.limit)
    elif args.source == "reddit":
        try:
            items = scrape_reddit(args.subreddit, args.sort, args.limit)
        except HTTPError as exc:
            print(
                f"Reddit blocked the public JSON request ({exc.code}). "
                "Try GitHub source now, or use Reddit's official API / a logged-in export later.",
                file=sys.stderr,
            )
            items = []
        except URLError as exc:
            print(f"Reddit request failed: {exc}", file=sys.stderr)
            items = []
    else:
        items = scrape_x_placeholder(args.query, args.limit)

    if args.format == "json":
        print(json.dumps({"date": started, "items": [asdict(item) for item in items]}, ensure_ascii=False, indent=2))
        return

    print(f"Trend signals ({started})")
    for idx, item in enumerate(items, 1):
        score = f" score={item.score}" if item.score else ""
        print(f"{idx}. [{item.source}]{score} {unescape(item.title)}")
        if item.summary:
            print(f"   {unescape(item.summary)}")
        print(f"   {item.url}")
    if args.angles:
        print("\nMeme angle drafts")
        for idx, angle in enumerate(meme_angles(items[:5]), 1):
            print(f"{idx}. {angle}")


if __name__ == "__main__":
    main()
