"""Pro-style captions: ASS subtitles with word-by-word highlight (karaoke) in 9:16 layout."""
def fmt(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Pro,Arial Black,72,&H00FFFFFF,&H0000FFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,2,2,40,40,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def words_from_segments(segments, chunk=4):
    """Group words into punchy 3-4 word caption lines, keeping timing."""
    lines, cur = [], []
    for seg in segments:
        words = seg["text"].split()
        if not words: continue
        dur = max(seg["end"] - seg["start"], 0.1) / len(words)
        for i, w in enumerate(words):
            cur.append((w, seg["start"] + i * dur, seg["start"] + (i + 1) * dur))
            if len(cur) == chunk:
                lines.append(cur); cur = []
    if cur: lines.append(cur)
    return lines

def to_ass(segments, highlight="&H0000FFFF"):
    out = [HEADER]
    for line in words_from_segments(segments):
        if not line: continue
        start, end = line[0][1], line[-1][2]
        # Highlight the middle word in yellow — classic viral Shorts style
        parts = []
        for idx, (w, _, _) in enumerate(line):
            parts.append(f"{{\\c{highlight}}}{w.upper()}{{\\c&H00FFFFFF}}" if idx == len(line)//2 else w.upper())
        out.append(f"Dialogue: 0,{fmt(start)},{fmt(end)},Pro,,0,0,0,,{' '.join(parts)}")
    return "\n".join(out) + "\n"
