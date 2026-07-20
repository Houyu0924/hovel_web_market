from pathlib import Path
import shutil,sys
source_root=Path(__file__).resolve().parent
target_root=Path(sys.argv[1]).expanduser().resolve() if len(sys.argv)>1 else Path.cwd().resolve()
backup_root=target_root/".hovel_backup_sprint1"
for source in source_root.rglob("*"):
 if source.is_dir(): continue
 relative=source.relative_to(source_root)
 if str(relative) in {"install_sprint1.py","README_SPRINT1.md"}: continue
 if ".hovel_backup_sprint1" in relative.parts: continue
 target=target_root/relative
 try:
  if source.resolve()==target.resolve(): continue
 except FileNotFoundError: pass
 target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():
  backup=backup_root/relative
  backup.parent.mkdir(parents=True,exist_ok=True)
  if not backup.exists(): shutil.copy2(target,backup)
 shutil.copy2(source,target)
print("HOVEL Sprint 1 installed successfully.")
print("Run: python3 scripts/validate_sprint1.py")
