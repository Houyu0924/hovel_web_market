from pathlib import Path
import subprocess
import sys
import tempfile
import shutil
import json

repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()

required = [
    "run.py",
    "intelligence/search.py",
    "intelligence/articles.py",
    "intelligence/prompts.py",
    "intelligence/context.py",
    "workflow/runner.py",
    "prompts/market.md",
    "tests/test_intelligence.py",
]
missing = [p for p in required if not (repo / p).exists()]
if missing:
    print("Sprint 3 validation failed.")
    for p in missing:
        print("MISSING:", p)
    raise SystemExit(1)

unit = subprocess.run(
    [sys.executable, "-S", "-m", "unittest", "discover", "-s", str(repo / "tests")],
    cwd=repo, capture_output=True, text=True
)
if unit.returncode != 0:
    print(unit.stdout)
    print(unit.stderr)
    raise SystemExit(unit.returncode)

with tempfile.TemporaryDirectory() as tmp:
    test_repo = Path(tmp) / "repo"
    for name in ["workflow","intelligence","prompts","knowledge","articles"]:
        src = repo / name
        if src.exists():
            shutil.copytree(src, test_repo / name)
    shutil.copy2(repo / "run.py", test_repo / "run.py")

    result = subprocess.run(
        [sys.executable, "-S", str(test_repo / "run.py"), "--repo-root", str(test_repo),
         "--topic", "仕事中に眠すぎる"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(result.returncode)

    task_dirs = list((test_repo / "tasks").iterdir())
    if len(task_dirs) != 1:
        raise SystemExit("Smoke test failed: task count mismatch")

    task_dir = task_dirs[0]
    intelligence = json.loads((task_dir / "intelligence.json").read_text(encoding="utf-8"))
    if not intelligence["knowledge_results"]:
        raise SystemExit("Smoke test failed: no knowledge results")
    if not intelligence["related_articles"]:
        raise SystemExit("Smoke test failed: no related articles")

    task = json.loads((task_dir / "task.json").read_text(encoding="utf-8"))
    if task["status"] != "human-review":
        raise SystemExit(f"Unexpected status: {task['status']}")

print("Sprint 3 validation passed.")
print("Unit tests: passed")
print("Knowledge search: passed")
print("Article index: passed")
print("Cannibalization detection: passed")
print("Workflow integration: passed")
