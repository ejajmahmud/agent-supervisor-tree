"""Erlang-inspired supervisor hierarchy for self-healing agent processes."""
from typing import Dict, Any, Callable, List


class SupervisorTree:
    def __init__(self, strategy: str = "one_for_one", max_restarts: int = 5):
        self.strategy = strategy  # "one_for_one" or "one_for_all"
        self.max_restarts = max_restarts
        self._workers: Dict[str, Dict[str, Any]] = {}

    def register_worker(self, name: str, factory_fn: Callable[[], Any]) -> None:
        self._workers[name] = {
            "factory": factory_fn,
            "instance": factory_fn(),
            "restarts": 0,
            "status": "running"
        }

    def get_worker(self, name: str) -> Any:
        return self._workers[name]["instance"]

    def handle_crash(self, name: str, error: Exception) -> bool:
        if name not in self._workers:
            return False

        worker = self._workers[name]
        if worker["restarts"] >= self.max_restarts:
            worker["status"] = "failed_permanently"
            return False

        if self.strategy == "one_for_one":
            worker["instance"] = worker["factory"]()
            worker["restarts"] += 1
            worker["status"] = "running"
            return True
        elif self.strategy == "one_for_all":
            for w in self._workers.values():
                w["instance"] = w["factory"]()
                w["restarts"] += 1
                w["status"] = "running"
            return True

        return False

    def stats(self) -> Dict[str, Any]:
        return {
            name: {"status": w["status"], "restarts": w["restarts"]}
            for name, w in self._workers.items()
        }
