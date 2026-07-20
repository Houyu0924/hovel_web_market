import json
from pathlib import Path

def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def write_json(path,data):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def write_text(path,content):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content.rstrip()+"\n",encoding="utf-8")
def read_text(path): return Path(path).read_text(encoding="utf-8")
