from pathlib import Path
import subprocess,sys,tempfile,shutil,json
repo=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd().resolve()
required=["run.py","workflow/workflow.json","workflow/runner.py","workflow/models.py","workflow/storage.py","workflow/agents/registry.py","workflow/validators/schema_validator.py"]
missing=[x for x in required if not (repo/x).exists()]
if missing: raise SystemExit("Missing: "+", ".join(missing))
with tempfile.TemporaryDirectory() as tmp:
    r=Path(tmp)/"repo"; shutil.copytree(repo/"workflow",r/"workflow"); shutil.copy2(repo/"run.py",r/"run.py")
    z=subprocess.run([sys.executable,str(r/"run.py"),"--repo-root",str(r),"--topic","会社員向け耳栓比較"],capture_output=True,text=True)
    if z.returncode: print(z.stdout,z.stderr); raise SystemExit(z.returncode)
    ds=list((r/"tasks").iterdir()); assert len(ds)==1
    needed=["task.json","market.md","seo.md","investment.md","product.md","draft.md","factcheck.md","editor.md","review.md"]
    miss=[x for x in needed if not (ds[0]/x).exists()]
    if miss: raise SystemExit("Missing outputs: "+", ".join(miss))
    task=json.loads((ds[0]/"task.json").read_text(encoding="utf-8"))
    if task["status"]!="human-review": raise SystemExit("Unexpected status")
print("Sprint 2 validation passed.")
print("Smoke test: passed")
