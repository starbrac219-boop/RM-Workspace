"""End-to-end: discover -> pick moment -> captions -> 9:16 render -> upload."""
import json
from .. import config, store
from . import discover, moments, subtitles, render as R, upload as U

DEMO_SEGMENTS = [  # used only when no real video/transcription is available yet
    {"start": 0, "end": 4, "text": "I bought the world's biggest mystery box for one million dollars!"},
    {"start": 4, "end": 8, "text": "Last person to leave this circle wins $500,000!"},
    {"start": 8, "end": 12, "text": "This challenge is completely insane and impossible!"},
]

def run_once(use_demo=False):
    store.init()
    videos = DEMO if use_demo else discover.fetch_rss()
    results = []
    for v in videos:
        if store.seen(v["video_id"]): continue
        store.mark(v["video_id"], v["title"], "discovered")
        segments = DEMO_SEGMENTS if use_demo else None
        if segments is None:
            results.append({**v, "status": "discovered — transcription runs after yt-dlp/whisper install (SETUP.md)"})
            continue
        moment = moments.find_best_moment(segments, config.CLIP_LENGTH_SECONDS)
        title = moments.make_hook_title(moment, v["title"])
        plan = {**R.plan_clip(v, moment), "title": title,
                "captions_preview": subtitles.to_ass(segments)[:400]}
        if not config.DRY_RUN and not use_demo:
            src = R.download(v["url"], config.CLIPS_DIR)
            segs = R.transcribe(src)
            moment = moments.find_best_moment(segs, config.CLIP_LENGTH_SECONDS)
            ass = config.CLIPS_DIR / f"{v['video_id']}.ass"; ass.write_text(subtitles.to_ass(segs))
            out = config.CLIPS_DIR / f"{v['video_id']}_short.mp4"
            R.render(src, moment["start"], moment["end"], ass, out)
            plan.update(U.upload_short(out, moments.make_hook_title(moment, v["title"]),
                                       f"Clip from: {v['url']}\n#shorts"))
            store.mark(v["video_id"], v["title"], plan.get("status", "rendered"))
        results.append(plan)
    return results

DEMO = [{"video_id": "DEMO123", "title": "I Spent 50 Hours In Solitary Confinement",
         "url": "https://www.youtube.com/watch?v=DEMO123", "published": "2026-01-01"}]
