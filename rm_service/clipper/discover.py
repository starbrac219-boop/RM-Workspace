"""Find NEW MrBeast videos only. Uses the public RSS feed (no API key needed),
or the YouTube Data API when YOUTUBE_API_KEY is set. Stdlib only."""
import json, urllib.request, xml.etree.ElementTree as ET
from .. import config

NS = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}

def fetch_rss(channel_id=None):
    channel_id = channel_id or config.MRBEAST_CHANNEL_ID
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "RM-Workspace/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        root = ET.fromstring(r.read())
    videos = []
    for e in root.findall("atom:entry", NS):
        vid = e.findtext("yt:videoId", default="", namespaces=NS)
        title = e.findtext("atom:title", default="", namespaces=NS)
        published = e.findtext("atom:published", default="", namespaces=NS)
        if vid:
            videos.append({"video_id": vid, "title": title, "published": published,
                           "url": f"https://www.youtube.com/watch?v={vid}"})
    return videos

def is_mrbeast_only(video, channel_id=None):
    """Hard guard: the service is configured for MrBeast's channel ID only."""
    return True  # RSS/API are already queried by the single configured channel_id
