import sys; sys.path.insert(0, ".")
import unittest
from rm_service.clipper import moments, subtitles
from rm_service.dropship.research import czk_price, research

SEGS = [{"start": 0, "end": 4, "text": "I bought the world's biggest mystery box for one million dollars!"},
        {"start": 4, "end": 8, "text": "Last person to leave wins $500,000!"},
        {"start": 30, "end": 34, "text": "and then we walked over here quietly"}]

class TestClipper(unittest.TestCase):
    def test_best_moment_is_the_hook(self):
        m = moments.find_best_moment(SEGS, 45)
        self.assertIn("million", m["text"]); self.assertGreater(m["score"], 5)
    def test_hook_title(self):
        self.assertIn("#shorts", moments.make_hook_title(moments.find_best_moment(SEGS), "x"))
    def test_ass_916_captions(self):
        ass = subtitles.to_ass(SEGS)
        self.assertIn("PlayResX: 1080", ass); self.assertIn("PlayResY: 1920", ass); self.assertIn("Dialogue:", ass)

class TestDropship(unittest.TestCase):
    def test_czk_price_psychology(self):
        self.assertEqual(czk_price(10) % 10, 9)  # ends in 9
        self.assertGreater(czk_price(10), 10 * 23)
    def test_research_sorted(self):
        r = research(5); self.assertEqual(len(r), 5)
        self.assertTrue(all(r[i]["score"] >= r[i+1]["score"] for i in range(4)))

if __name__ == "__main__": unittest.main()
