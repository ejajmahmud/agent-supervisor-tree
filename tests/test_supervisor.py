"""Unit tests for SupervisorTree."""
import unittest
from agent_supervisor_tree.supervisor import SupervisorTree

class TestSupervisorTree(unittest.TestCase):
    def test_one_for_one_restart(self):
        tree = SupervisorTree(strategy="one_for_one", max_restarts=2)
        tree.register_worker("w1", lambda: [1, 2, 3])
        self.assertEqual(tree.get_worker("w1"), [1, 2, 3])

        healed = tree.handle_crash("w1", Exception("boom"))
        self.assertTrue(healed)
        self.assertEqual(tree.stats()["w1"]["restarts"], 1)

    def test_max_restarts_exceeded(self):
        tree = SupervisorTree(max_restarts=1)
        tree.register_worker("w2", lambda: "ok")
        tree.handle_crash("w2", Exception("1"))
        healed2 = tree.handle_crash("w2", Exception("2"))
        self.assertFalse(healed2)
        self.assertEqual(tree.stats()["w2"]["status"], "failed_permanently")

if __name__ == "__main__":
    unittest.main()
