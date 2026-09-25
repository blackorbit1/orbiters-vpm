import copy
import unittest
from orbiters_migration import verify, FEED

class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.old = {"id":"cc.orbiters.vpm", "url":"https://old.invalid/index.json", "packages":{"tool":{"versions":{"1.0.0":{"name":"tool", "version":"1.0.0", "url":"https://github.com/example/tool.zip", "zipSHA256":"abc"}}}}}
        self.new = copy.deepcopy(self.old)
        self.new["url"] = FEED
    def test_preserves_versions(self):
        verify(self.new, self.old)
    def test_blocks_missing_versions(self):
        self.new["packages"]["tool"]["versions"] = {}
        with self.assertRaises(ValueError): verify(self.new, self.old)
    def test_blocks_changed_artifacts(self):
        self.new["packages"]["tool"]["versions"]["1.0.0"]["zipSHA256"] = "changed"
        with self.assertRaises(ValueError): verify(self.new, self.old)
    def test_applies_creator_visibility_after_handover(self):
        self.old["url"] = FEED
        self.new["packages"]["tool"]["versions"] = {}
        verify(self.new, self.old)

if __name__ == "__main__": unittest.main()
