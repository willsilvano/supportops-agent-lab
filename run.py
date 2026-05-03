import argparse
import importlib
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TESTS_DIR = ROOT / "tests"

TEST_MODULES = {
    "ex00": "tests.test_ex00_setup",
    "ex01": "tests.test_ex01_mock_api",
    "ex03": "tests.test_ex03_schema_wrapper",
    "ex05": "tests.test_ex05_agent_loop",
    "ex10": "tests.test_ex10_rag_retrieval",
    "ex11": "tests.test_ex11_guardrails",
    "ex12": "tests.test_ex12_eval_dataset",
}


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def doctor() -> int:
    print(f"Python: {sys.version.split()[0]}")
    required_paths = [
        ROOT / "README.md",
        ROOT / "RULES.md",
        ROOT / "supportops_agent",
        ROOT / "supportops_agent" / "data" / "tickets.json",
        ROOT / "supportops_agent" / "data" / "docs" / "runbook-auth.md",
        ROOT / "tests",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_paths if not path.exists()]
    if missing:
        print("Missing paths:")
        for item in missing:
            print(f" - {item}")
        return 1
    for module in [
        "supportops_agent.data_loader",
        "supportops_agent.mock_api.server",
        "supportops_agent.clients.mock_service_client",
        "supportops_agent.agent.output_schemas",
    ]:
        importlib.import_module(module)
    print("Doctor OK: estrutura e imports principais validos.")
    return 0


def setup() -> int:
    requirements = ROOT / "requirements.txt"
    result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements)])
    return result.returncode


def run_tests(target: str) -> int:
    if target == "all":
        modules = list(TEST_MODULES.values())
    else:
        if target not in TEST_MODULES:
            print(f"Exercicio desconhecido: {target}")
            print("Use um destes:", ", ".join(TEST_MODULES))
            return 1
        modules = [TEST_MODULES[target]]

    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for module_name in modules:
        suite.addTests(loader.loadTestsFromName(module_name))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def mock_api(port: int) -> int:
    from supportops_agent.mock_api.server import run_server

    run_server(port=port)
    return 0


def demo() -> int:
    from supportops_agent.agent.graph import run_supportops_flow

    load_dotenv(ROOT / ".env")
    result = run_supportops_flow("Analise o ticket TCK-4821")
    print(result.get("final_answer"))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("setup")
    api_parser = sub.add_parser("mock-api")
    api_parser.add_argument("--port", type=int, default=8000)
    test_parser = sub.add_parser("test")
    test_parser.add_argument("target")
    sub.add_parser("demo")
    args = parser.parse_args()

    os.chdir(ROOT)
    if args.command == "doctor":
        return doctor()
    if args.command == "setup":
        return setup()
    if args.command == "mock-api":
        return mock_api(args.port)
    if args.command == "test":
        return run_tests(args.target)
    if args.command == "demo":
        return demo()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

