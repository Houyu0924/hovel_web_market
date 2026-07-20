import argparse,re
from datetime import datetime,timezone
from pathlib import Path
from .models import Task,utc_now
from .storage import read_json,write_json,write_text,read_text
from .agents.registry import get_agent
from .validators.schema_validator import validate_workflow,validate_inputs,validate_output
from ai import AIConfig,AIService


def slugify(v):
    v=re.sub(r"[^\w\-ぁ-んァ-ヶ一-龠々ー]+","-",v.strip().lower(),flags=re.UNICODE)
    return re.sub(r"-+","-",v).strip("-")[:40] or "article"


def task_id(topic):
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")+"-"+slugify(topic)


def save_task(d,t):
    write_json(d/"task.json",t.to_dict())


def run_workflow(repo_root,topic,resume=None):
    repo_root=Path(repo_root).resolve()
    wf=read_json(repo_root/"workflow/workflow.json")
    validate_workflow(wf)
    ai_service=AIService(AIConfig.from_env())
    tasks=repo_root/"tasks"
    tasks.mkdir(exist_ok=True)

    if resume:
        d=tasks/resume
        t=Task(**read_json(d/"task.json"))
        t.log("workflow_resumed")
        topic=t.topic
    else:
        t=Task(task_id(topic),topic)
        d=tasks/t.task_id
        d.mkdir()
        t.log("workflow_created")

    t.status="running"
    save_task(d,t)

    try:
        stages=wf["stages"]
        for i,s in enumerate(stages):
            out=d/s["output"]
            if out.exists() and out.read_text(encoding="utf-8").strip():
                t.log("stage_skipped_existing",stage=s["id"])
                continue

            validate_inputs(s,d)
            t.current_stage=s["id"]
            t.log("stage_started",stage=s["id"])
            save_task(d,t)

            inputs={n:read_text(d/n) for n in s["requires"]}
            deterministic=get_agent(s["agent"]).run(t.topic,inputs)
            generation=ai_service.generate(s["id"],t.topic,inputs,deterministic)
            write_text(out,generation.text)
            validate_output(s,d)

            t.artifacts[s["id"]]=s["output"]
            t.log(
                "stage_completed",
                stage=s["id"],
                output=s["output"],
                provider=generation.provider,
                model=generation.model,
                response_id=generation.response_id,
                ai_error=generation.error,
            )
            nxt=stages[i+1]["id"] if i+1<len(stages) else wf["final_status"]
            write_json(
                d/"handoffs"/f"{s['id']}-to-{nxt}.json",
                {
                    "task_id":t.task_id,
                    "from_stage":s["id"],
                    "to_stage":nxt,
                    "output_file":s["output"],
                    "provider":generation.provider,
                    "model":generation.model,
                    "created_at":utc_now(),
                },
            )
            save_task(d,t)

        t.status=wf["final_status"]
        t.current_stage=t.status
        t.log("workflow_completed",status=t.status)
        save_task(d,t)
        write_text(
            d/"review.md",
            f"# Human Review Queue\n\n- Task ID: `{t.task_id}`\n- Topic: {t.topic}\n- Status: `{t.status}`\n- AI enabled: `{ai_service.config.enabled}`\n",
        )
        return d
    except Exception as e:
        t.status="failed"
        t.log("workflow_failed",error=str(e))
        save_task(d,t)
        raise


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--topic")
    p.add_argument("--resume")
    p.add_argument("--repo-root",default=".")
    a=p.parse_args()
    if not a.topic and not a.resume:
        p.error("--topic または --resume が必要です")
    d=run_workflow(a.repo_root,a.topic or "",a.resume)
    print("Workflow completed.")
    print("Task directory:",d)
    print("Status: human-review")
    return 0
