from pathlib import Path
import sys
repo=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
required=["company/mission.md","company/vision.md","company/values.md","company/organization.md","company/decision-log/DL-2026-001-ai-marketing-department.md","company/decision-log/DL-2026-002-source-of-truth.md","os/hovel-os.md","os/standards/evidence.md","os/standards/writing.md","os/standards/seo.md","os/standards/review.md","os/schemas/article.yaml","os/schemas/market.yaml","os/schemas/product.yaml","os/schemas/review.yaml","os/schemas/decision.yaml","knowledge/README.md","ai/README.md"]
missing=[p for p in required if not (repo/p).exists()]
if missing:
 print("Sprint 1 validation failed.")
 [print("  MISSING:",p) for p in missing]
 raise SystemExit(1)
print("Sprint 1 validation passed.")
print("Checked files:",len(required))
