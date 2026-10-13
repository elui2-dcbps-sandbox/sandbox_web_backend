"""Synthetic backend for a public dependency-fix rehearsal."""


def preview_record(name: str) -> dict[str, str]:
    return {"name": name.strip(), "kind": "synthetic"}
