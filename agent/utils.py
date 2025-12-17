from bs4 import BeautifulSoup, Comment
import re

def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove scripts, styles, head, etc.
    for tag in soup(["script", "style", "meta", "noscript", "head", "title", "nav", "footer", "header"]):
        tag.decompose()

    # Remove comments
    for comment in soup.find_all(string=lambda s: isinstance(s, Comment)):
        comment.extract()

    # Remove elements that are visually hidden
    bad_selectors = [
        "[hidden]",
        "[style*='display:none']",
        "[style*='visibility:hidden']",
        "[style*='opacity:0']",
    ]
    for selector in bad_selectors:
        for tag in soup.select(selector):
            tag.decompose()

    # Extract visible text
    text = soup.get_text(separator=" ", strip=True)

    return text