from pathlib import Path
import shutil,sys
src=Path(__file__).resolve().parent; dst=Path(sys.argv[1]).expanduser().resolve() if len(sys.argv)>1 else Path.cwd().resolve(); backup=dst/".hovel_backup_sprint2"
for p in src.rglob("*"):
    if p.is_dir() or "__pycache__" in p.parts or p.name in {"install_sprint2.py","README_SPRINT2.md"}: continue
    rel=p.relative_to(src); q=dst/rel
    try:
        if p.resolve()==q.resolve(): continue
    except FileNotFoundError: pass
    q.parent.mkdir(parents=True,exist_ok=True)
    if q.exists():
        b=backup/rel; b.parent.mkdir(parents=True,exist_ok=True)
        if not b.exists(): shutil.copy2(q,b)
    shutil.copy2(p,q)
print("HOVEL Sprint 2 installed.")
print("Run: python3 scripts/validate_sprint2.py")
