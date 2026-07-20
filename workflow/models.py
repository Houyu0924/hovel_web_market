from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

@dataclass
class Task:
    task_id: str
    topic: str
    status: str = "queued"
    current_stage: str = "pending"
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    artifacts: dict = field(default_factory=dict)
    logs: list = field(default_factory=list)
    def log(self,event,**details):
        self.logs.append({"at":utc_now(),"event":event,**details})
        self.updated_at=utc_now()
    def to_dict(self): return asdict(self)
