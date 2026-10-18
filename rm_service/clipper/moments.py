"""Pick the most 'clippable' moment from a transcript.
Heuristic scoring works offline; if OPENAI_API_KEY is set it can be extended with an LLM call."""
import re

HOOK_WORDS = {
    "money": 3, "$": 3, "million": 4, "billion": 4, "dollars": 3, "win": 3, "wins": 3,
    "challenge": 3, "last to": 4, "survive": 4, "impossible": 3, "world's": 3, "biggest": 3,
    "insane": 3, "crazy": 2, "never": 2, "only": 2, "first": 2, "free": 2, "giveaway": 4,
    "24 hours": 3, "100": 2, "1000": 3, "eliminated": 3, "fail": 2, "wins a": 4,
}

def score_sentence(text):
    t = text.lower(); s = 0.0
    for w, pts in HOOK_WORDS.items():
        if w in t: s += pts
    s += min(len(re.findall(r"\d", t)) * 0.5, 3)          # numbers hook viewers
    if "!" in text: s += 1
    if text.strip().endswith("?"): s += 0.5
    return s

def find_best_moment(segments, clip_len=45):
    """segments: [{'start': float, 'end': float, 'text': str}] -> best window dict."""
    if not segments: return None
    best, best_score = None, -1
    for i, seg in enumerate(segments):
        score, end, j = 0.0, seg["start"], i
        while j < len(segments) and segments[j]["end"] - seg["start"] <= clip_len:
            score += score_sentence(segments[j]["text"]); end = segments[j]["end"]; j += 1
        if score > best_score:
            best_score = score
            best = {"start": seg["start"], "end": end, "score": round(best_score, 2),
                    "text": " ".join(s["text"] for s in segments[i:j])[:500]}
    return best

def make_hook_title(moment, video_title=""):
    text = (moment or {}).get("text", "")
    m = re.search(r"[^.!?]*(\$[\d,]+|million|billion)[^.!?]*", text, re.I)
    hook = (m.group(0).strip() if m else video_title)[:70]
    return f"{hook} 😱🔥 #shorts"
