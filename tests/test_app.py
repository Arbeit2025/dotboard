import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import app as app_module  # noqa: E402


class DotBoardTest(unittest.TestCase):
    def setUp(self):
        self.client = app_module.app.test_client()

    def test_healthz(self):
        res = self.client.get("/healthz")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "ok")

    def test_index_ok(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        body = res.get_data(as_text=True)
        self.assertIn("お絵かきボード", body)

    def test_canvas_present(self):
        body = self.client.get("/").get_data(as_text=True)
        self.assertIn('<canvas id="board" width="16" height="16"', body)
        self.assertIn("PNGで保存", body)
        self.assertIn("ぜんぶ消す", body)

    def test_palette_colors(self):
        self.assertEqual(len(app_module.COLORS), 12)
        body = self.client.get("/").get_data(as_text=True)
        for c in app_module.COLORS:
            self.assertIn(c, body)


if __name__ == "__main__":
    unittest.main()
