import json
import tempfile
import unittest
from pathlib import Path
from domain_context.loader import load_domain

FIXTURE = Path("fixtures/domain.json")

class DomainFixtureTest(unittest.TestCase):
    def test_fixture_is_complete(self):
        value = load_domain(FIXTURE)
        self.assertEqual(value["domain"], "emerging-creator-growth")
        self.assertGreaterEqual(len(value["facts"]), 2)

    def test_record_types_cover_requirements(self):
        value = load_domain(FIXTURE)
        # 窗口化、领域归一、反作弊与复核、扶持评估、申诉、快照重现、账号合并
        expected = {
            "统计窗口", "领域基准", "候选结论", "反作弊结论", "复核意见",
            "扶持动作", "效果评估", "申诉记录", "数据快照", "账号血缘事件",
        }
        self.assertTrue(expected.issubset(value["record_types"]))

    def test_workflow_states_cover_review_and_appeal(self):
        value = load_domain(FIXTURE)
        states = value["workflow_states"]
        for state in ["观察中", "候选", "待复核", "已入选", "申诉中", "已结束"]:
            self.assertIn(state, states)
        # 申诉中不是终态，已结束必须存在
        self.assertEqual(states[-1], "已结束")

    def test_facts_state_key_principles(self):
        value = load_domain(FIXTURE)
        facts = "".join(value["facts"])
        for keyword in ["领域", "窗口", "不可改写", "快照", "申诉"]:
            self.assertIn(keyword, facts)

    def test_sample_supports_replay_and_normalization(self):
        value = load_domain(FIXTURE)
        sample = value["sample"]
        # 可重现：结论绑定快照与规则版本；领域归一：带同期领域基准
        self.assertIn("snapshot_id", sample)
        self.assertIn("rule_version", sample)
        self.assertIn("domain_benchmark", sample)
        self.assertIn("window_signals", sample)

    def test_loader_rejects_missing_critical_record_type(self):
        value = load_domain(FIXTURE)
        value["record_types"].remove("数据快照")
        with tempfile.TemporaryDirectory() as tmp:
            broken = Path(tmp) / "domain.json"
            broken.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_domain(broken)

if __name__ == "__main__":
    unittest.main()
