import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
import pages  # noqa: E402


class PagesTest(unittest.TestCase):
    def setUp(self):
        self.files = pages.write()

    def test_every_nav_link_has_a_page(self):
        for slug, _ in pages.NAV + pages.MORE:
            self.assertIn(f"{slug}.html", self.files)

    def test_internal_links_resolve(self):
        for name in self.files:
            text = (pages.SITE / name).read_text(encoding="utf-8")
            for href in re.findall(r'href="(/[^"]*)"', text):
                path = href.strip("/")
                if not path or path.startswith("assets/"):
                    continue
                self.assertTrue((pages.SITE / f"{path}.html").exists(), f"{name} links to {href}")

    def test_each_page_has_its_own_title(self):
        titles = [re.search(r"<title>(.*?)</title>", (pages.SITE / n).read_text(encoding="utf-8")).group(1)
                  for n in self.files]
        self.assertEqual(len(titles), len(set(titles)))

    def test_no_inline_styles(self):
        # the security policy blocks them
        for name in self.files:
            self.assertNotIn("style=", (pages.SITE / name).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
