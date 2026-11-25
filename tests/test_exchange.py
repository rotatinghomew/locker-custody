"""核对交换资料的客户编号、时序和关联条件。"""
import json
from pathlib import Path
import unittest


SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def rows(name):
    content = (SAMPLES / f"{name}.ndjson").read_text(encoding="utf-8")
    return [json.loads(line) for line in content.splitlines()]


class ExchangeSampleTest(unittest.TestCase):
    def test_records_are_json_objects(self):
        files = sorted(SAMPLES.glob("*.ndjson"))
        self.assertEqual(len(files), 5)
        for path in files:
            with self.subTest(path=path.name):
                records = rows(path.stem)
                self.assertTrue(records)
                self.assertTrue(all(isinstance(row, dict) for row in records))

    def test_related_records_preserve_source_evidence(self):
        carrier = rows("carrier")
        self.assertEqual(carrier[0]["task"], carrier[1]["task"])
        self.assertNotEqual(carrier[0]["fleet"], carrier[1]["fleet"])
        self.assertGreater(carrier[0]["revision"], carrier[2]["revision"])
        cabinet = rows("cabinet")
        self.assertGreater(cabinet[1]["revision"], cabinet[2]["revision"])
        self.assertEqual(cabinet[2]["handoff"], carrier[4]["handoff"])
        self.assertEqual(cabinet[2]["parcel"], carrier[4]["parcel"])
        self.assertLess(rows("parcels")[1]["from"], rows("parcels")[0]["until"])
