class ValidationError(RuntimeError): pass

def validate_workflow(workflow):
    stages=workflow.get("stages",[])
    if not stages: raise ValidationError("Workflow has no stages")
    ids=set(); outputs=set(); available=set()
    for s in stages:
        for k in ("id","agent","output","requires"):
            if k not in s: raise ValidationError(f"Missing {k}: {s}")
        if s["id"] in ids: raise ValidationError(f"Duplicate id: {s['id']}")
        if s["output"] in outputs: raise ValidationError(f"Duplicate output: {s['output']}")
        missing=[x for x in s["requires"] if x not in available]
        if missing: raise ValidationError(f"Unavailable requirements for {s['id']}: {missing}")
        ids.add(s["id"]); outputs.add(s["output"]); available.add(s["output"])

def validate_inputs(stage,task_dir):
    missing=[x for x in stage["requires"] if not (task_dir/x).exists()]
    if missing: raise ValidationError(f"Missing inputs for {stage['id']}: {missing}")

def validate_output(stage,task_dir):
    p=task_dir/stage["output"]
    if not p.exists() or not p.read_text(encoding="utf-8").strip():
        raise ValidationError(f"Invalid output for {stage['id']}: {stage['output']}")
