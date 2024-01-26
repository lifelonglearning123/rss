import feedparser
import PyRSS2Gen
import datetime
import time
import re


def markdown_image_to_html(description):
    # Regex to find Markdown image syntax
    markdown_image_regex = r"!\[.*?\]\((.*?)\)"
    # Replace Markdown image syntax with HTML <img> tag
    html_description = re.sub(markdown_image_regex, r'<img src="\1" alt="Image">', description)
    return html_description


# Function to extract image URLs
def extract_image_urls(text):
    # This regex will find all URLs that start with http(s)://
    urls = re.findall(r'http[s]?://[^\s]+', text)
    return urls

# Function to embed images in the description
def embed_images_in_description(description):
    image_urls = extract_image_urls(description)
    for url in image_urls:
        img_tag = f'<img src="{url}" alt="Image" />'
        description = description.replace(url, img_tag)
    return description



# Fetches GHL Feed
def fetch_rss(url):
    return feedparser.parse(url)

source_rss_url = "https://ideas.gohighlevel.com/api/changelog/feed.rss"
feed = fetch_rss(source_rss_url)

# Creates the RSS feed header
def create_my_feed(entries):
    rss = PyRSS2Gen.RSS2(
        title = "macaws.ai function updates",
        link = "http://macaws.ai/",
        description = "My custom RSS feed",
        lastBuildDate = datetime.datetime.now(),
        items = entries
    )
    return rss

# Converts datetime format
def struct_time_to_datetime(struct_time):
    return datetime.datetime.fromtimestamp(time.mktime(struct_time))

# Search for GHL and change with macaws.ai
def replace_keywords(content):
    content = content.replace("ghl", "macaws.ai")
    content = content.replace("gohighlevel", "macaws.ai")
    return content

my_entries = []
for entry in feed.entries:
    full_description = replace_keywords(entry.description)
   #full_description = embed_images_in_description(full_description)
    full_description = markdown_image_to_html(full_description)
    my_entries.append(PyRSS2Gen.RSSItem(
        title = replace_keywords(entry.title),
        description = full_description,  # Ensure this is treated as raw HTML
        pubDate = struct_time_to_datetime(entry.published_parsed)
    ))

# Retrieve all new RSS feed after parsing
my_rss_feed = create_my_feed(my_entries)

# Saves the RSS feed xml
rss_xml = my_rss_feed.to_xml()
with open("myrssfeed.xml", "w", encoding='utf-8') as file:
    file.write(rss_xml)
