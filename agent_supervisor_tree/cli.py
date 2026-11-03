"""Command-line interface for Agent Supervisor Tree."""
import argparse
from .supervisor import SupervisorTree

def main():
    parser = argparse.ArgumentParser(description="Agent Supervisor Tree CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate self-healing supervisor restarts")
    args = parser.parse_args()

    tree = SupervisorTree(strategy="one_for_one", max_restarts=3)
    tree.register_worker("git_worker", lambda: {"state": "clean"})
    print("Worker online. Initial stats:", tree.stats())

    print("Simulating crash on git_worker...")
    healed = tree.handle_crash("git_worker", RuntimeError("OOM in subprocess"))
    print(f"Self-healed: {healed}. Stats after reboot: {tree.stats()}")

if __name__ == "__main__":
    main()
