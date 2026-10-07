import json
import unittest
from pathlib import Path
from unittest.mock import patch

from crossrenamertool.core import presets as presets_manager


class TestPresets(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.tmp_dir = tempfile.mkdtemp()
        self.tmp_path = Path(self.tmp_dir) / "prefixes.json"
        self.tmp_path.write_text(json.dumps({"presets": ["CTRL", "JNT"]}))
        
        self.patcher = patch.dict(presets_manager._PATHS, {"prefixes": self.tmp_path})
        self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_load_presets(self):
        result = presets_manager.load_presets("prefixes")
        self.assertEqual(result, ["CTRL", "JNT"])

    def test_add_preset(self):
        presets_manager.add_preset("prefixes", "FK")
        result = presets_manager.load_presets("prefixes")
        self.assertIn("FK", result)

    def test_no_duplicate(self):
        presets_manager.add_preset("prefixes", "CTRL")   # already exists
        result = presets_manager.load_presets("prefixes")
        self.assertEqual(result.count("CTRL"), 1)

