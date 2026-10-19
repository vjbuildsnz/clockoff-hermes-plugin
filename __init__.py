"""One native ClockOff plugin; authentication stays in Hermes's MCP connector."""
from pathlib import Path

from . import delivery


def register(ctx):
    root = Path(__file__).resolve().parent
    for source in sorted((root / "skills").glob("*/SKILL.md")):
        header = source.read_text().split("---", 2)[1]
        fields = dict(line.split(": ", 1) for line in header.strip().splitlines())
        ctx.register_skill(source.parent.name, source, description=fields["description"])
    delivery.register(ctx)
