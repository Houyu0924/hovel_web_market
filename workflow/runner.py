import argparse
import re
import json
from datetime import datetime, timezone
from pathlib import Path

from .models import Task, utc_now
from .storage import read_json, write_json, write_text, read_text
from .agents.registry import get_agent
from .validators.schema_validator import validate_workflow, validate_inputs, validate_output
from intelligence.context import IntelligenceLayer

def slugify(value):
    value = value.strip().lower()
    value = re.sub(r"[^\w\-ぁ-んァ-ヶ一-龠々ー]+", "-", value, flags=re.UNICODE)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:40] or "article"

def create_task_id(topic):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{slugify(topic)}"

def save_task(task_dir, task):
    write_json(task_dir / "task.json", task.to_dict())

def write_handoff(task_dir, task, current_stage, next_stage, output_file):
    write_json(task_dir / "handoffs" / f"{current_stage}-to-{next_stage}.json", {
        "task_id": task.task_id,
        "from_stage": current_stage,
        "to_stage": next_stage,
        "output_file": output_file,
        "created_at": utc_now(),
    })

def intelligence_inputs(context):
    data = context.to_dict()
    return {
        "_intelligence.json": json.dumps(data, ensure_ascii=False, indent=2),
        "_knowledge_context": "\n".join(
            f"- {x['path']} ({x['score']}): {x['excerpt']}"
            for x in data["knowledge_results"]
        ) or "- 該当なし",
        "_related_articles": "\n".join(
            f"- {x['title']} ({x['score']}): {x['path']}"
            for x in data["related_articles"]
        ) or "- 該当なし",
        "_cannibalization_risks": "\n".join(
            f"- {x['title']} ({x['score']}): {x['path']}"
            for x in data["cannibalization_risks"]
        ) or "- 該当なし",
        "_internal_links": "\n".join(
            f"- {x['title']}: {x['path']}"
            for x in data["internal_link_candidates"]
        ) or "- 該当なし",
    }

def run_workflow(repo_root, topic, resume=None):
    repo_root = Path(repo_root).resolve()
    workflow = read_json(repo_root / "workflow" / "workflow.json")
    validate_workflow(workflow)

    tasks_root = repo_root / "tasks"
    tasks_root.mkdir(parents=True, exist_ok=True)

    if resume:
        task_dir = tasks_root / resume
        data = read_json(task_dir / "task.json")
        task = Task(**data)
        task.log("workflow_resumed")
        topic = task.topic
    else:
        task = Task(task_id=create_task_id(topic), topic=topic)
        task_dir = tasks_root / task.task_id
        task_dir.mkdir(parents=True)
        task.log("workflow_created")

    layer = IntelligenceLayer(repo_root)
    context = layer.build_context(topic)
    write_json(task_dir / "intelligence.json", context.to_dict())
    shared = intelligence_inputs(context)

    task.status = "running"
    save_task(task_dir, task)

    try:
        stages = workflow["stages"]
        for i, stage in enumerate(stages):
            output_path = task_dir / stage["output"]
            if output_path.exists() and output_path.read_text(encoding="utf-8").strip():
                task.log("stage_skipped_existing", stage=stage["id"])
                continue

            validate_inputs(stage, task_dir)
            task.current_stage = stage["id"]
            task.log("stage_started", stage=stage["id"])
            save_task(task_dir, task)

            inputs = {name: read_text(task_dir / name) for name in stage["requires"]}
            inputs.update(shared)
            agent = get_agent(stage["agent"])
            content = agent.run(task.topic, inputs)

            header = (
                f"<!-- prompt-version: {context.prompt_version} -->\n"
                f"<!-- knowledge-results: {len(context.knowledge_results)} -->\n"
                f"<!-- related-articles: {len(context.related_articles)} -->\n\n"
            )
            write_text(output_path, header + content)
            validate_output(stage, task_dir)

            task.artifacts[stage["id"]] = stage["output"]
            task.log("stage_completed", stage=stage["id"], output=stage["output"])

            next_stage = stages[i + 1]["id"] if i + 1 < len(stages) else workflow["final_status"]
            write_handoff(task_dir, task, stage["id"], next_stage, stage["output"])
            save_task(task_dir, task)

        task.status = workflow["final_status"]
        task.current_stage = workflow["final_status"]
        task.log("workflow_completed", status=task.status)
        save_task(task_dir, task)

        write_text(task_dir / "review.md", f"""# Human Review Queue

- Task ID: `{task.task_id}`
- Topic: {task.topic}
- Status: `{task.status}`
- Knowledge results: {len(context.knowledge_results)}
- Cannibalization risks: {len(context.cannibalization_risks)}

## 必須確認
- [ ] intelligence.json
- [ ] 既存記事との重複
- [ ] 根拠確認
- [ ] 内部リンク
- [ ] アフィリエイト表記
- [ ] 公開承認
""")
        return task_dir

    except Exception as exc:
        task.status = "failed"
        task.log("workflow_failed", error=str(exc))
        save_task(task_dir, task)
        raise

def main():
    parser = argparse.ArgumentParser(description="HOVEL Knowledge-Aware Workflow Engine")
    parser.add_argument("--topic")
    parser.add_argument("--resume")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    if not args.topic and not args.resume:
        parser.error("--topic または --resume が必要です")

    task_dir = run_workflow(args.repo_root, args.topic or "", args.resume)
    print("Workflow completed.")
    print(f"Task directory: {task_dir}")
    print("Status: human-review")
    return 0
