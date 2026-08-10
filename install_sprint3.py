from pathlib import Path
import shutil
import sys

source_root = Path(__file__).resolve().parent
target_root = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
backup_root = target_root / ".hovel_backup_sprint3"

exclude = {"install_sprint3.py", "README_SPRINT3.md"}

for source in source_root.rglob("*"):
    if source.is_dir() or "__pycache__" in source.parts:
        continue
    rel = source.relative_to(source_root)
    if str(rel) in exclude:
        continue
    target = target_root / rel
    try:
        if source.resolve() == target.resolve():
            continue
    except FileNotFoundError:
        pass
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        backup = backup_root / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copy2(target, backup)
    shutil.copy2(source, target)

print("HOVEL Sprint 3 installed.")
print("Target:", target_root)
print("Validate: python3 scripts/validate_sprint3.py")
