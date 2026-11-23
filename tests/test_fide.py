import io
import sys
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
import fide  # noqa: E402

PLAYER = """<player><fideid>{id}</fideid><name>{name}</name><country>{fed}</country><sex>{sex}</sex>
<title>{title}</title><w_title></w_title><o_title></o_title><foa_title></foa_title>
<rating>{std}</rating><games>3</games><k>10</k><rapid_rating>{rap}</rapid_rating><rapid_games>0</rapid_games><rapid_k>0</rapid_k>
<blitz_rating>0</blitz_rating><blitz_games>0</blitz_games><blitz_k>0</blitz_k><birthday>{born}</birthday><flag>{flag}</flag></player>"""


def zipped(players):
    xml = "<playerslist>" + "".join(PLAYER.format(**p) for p in players) + "</playerslist>"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("players_list_xml_foa.xml", xml)
    return buf.getvalue()


def p(id, name, std, fed="NOR", sex="M", title="GM", rap=0, born=1990, flag=""):
    return dict(id=id, name=name, std=std, fed=fed, sex=sex, title=title, rap=rap, born=born, flag=flag)


class FideTest(unittest.TestCase):
    def lists(self, players):
        return fide.build(fide.players(zipped(players)), datetime(2026, 11, 1, tzinfo=timezone.utc))

    def test_inactive_players_are_left_out(self):
        out = self.lists([p(1, "Active, One", 2700), p(2, "Gone, Two", 2800, flag="i")])
        self.assertEqual([r["id"] for r in out["standard"]["open"]], [1])

    def test_names_and_ties(self):
        out = self.lists([p(1, "Carlsen, Magnus", 2800), p(2, "Gukesh D", 2750, fed="IND", born=2006),
                          p(3, "Other, A", 2750)])
        rows = out["standard"]["open"]
        self.assertEqual(rows[0]["name"], "Magnus Carlsen")
        self.assertEqual([r["rank"] for r in rows], [1, 2, 2])

    def test_each_list_has_its_own_ranks(self):
        out = self.lists([p(1, "Top, A", 2800), p(2, "Gukesh D", 2750, fed="IND", born=2006)])
        self.assertEqual(out["standard"]["open"][1]["rank"], 2)
        self.assertEqual(out["standard"]["india"][0]["rank"], 1)
        self.assertEqual(out["standard"]["juniors"][0]["id"], 2)

    def test_women_and_girls(self):
        out = self.lists([p(1, "Hou, Yifan", 2600, sex="F", born=1994), p(2, "Lee, Alice", 2470, sex="F", born=2009)])
        self.assertEqual(len(out["standard"]["women"]), 2)
        self.assertEqual([r["id"] for r in out["standard"]["girls"]], [2])

    def test_unrated_control_is_skipped(self):
        out = self.lists([p(1, "Std, Only", 2500), p(2, "Both, Two", 2400, rap=2450)])
        self.assertEqual([r["id"] for r in out["rapid"]["open"]], [2])


if __name__ == "__main__":
    unittest.main()
