import unittest
from pathlib import Path
from domain_context.loader import load_domain

FIXTURE = Path("fixtures/domain.json")

REQUIRED_SIGNALS = ["作者起始时间", "作品主题", "原创状态", "有效观看", "主动推荐", "负反馈", "扶持动作"]
REQUIRED_POLICIES = ["comparison", "history", "review", "transparency", "snapshot", "evaluation"]

class DomainFixtureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.value = load_domain(FIXTURE)

    def test_fixture_is_complete(self):
        self.assertEqual(self.value["domain"], "emerging-creator-growth")
        self.assertGreaterEqual(len(self.value["facts"]), 2)

    def test_window_signals_cover_required_signals(self):
        for signal in REQUIRED_SIGNALS:
            self.assertIn(signal, self.value["window_signals"])

    def test_policies_cover_product_rules(self):
        policies = self.value["policies"]
        for key in REQUIRED_POLICIES:
            self.assertTrue(policies.get(key), f"缺少策略 {key}")

    def test_records_support_review_snapshot_and_appeal(self):
        for record_type in ["反作弊结论", "复核意见", "名单快照", "申诉记录"]:
            self.assertIn(record_type, self.value["record_types"])
        self.assertIn("申诉中", self.value["workflow_states"])

    def test_sample_window_signals_match_catalog(self):
        sample_signals = self.value["sample"]["window_signals"]
        for signal in self.value["window_signals"]:
            self.assertIn(signal, sample_signals)

if __name__ == "__main__":
    unittest.main()
