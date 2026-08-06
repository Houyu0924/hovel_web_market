from pathlib import Path

class PromptEngine:
    def __init__(self, prompts_root):
        self.root = Path(prompts_root)

    def load(self, name):
        path = self.root / f"{name}.md"
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")
        return path.read_text(encoding="utf-8")

    def render(self, name, context):
        template = self.load(name)
        for key, value in context.items():
            template = template.replace("{{" + key + "}}", str(value))
        return template
