#!/usr/bin/env python3
"""
write_data.py

Create a JSON snapshot of all simple data objects found in a Python file
(or module).  Works in two modes:

    $ python write_data.py maritime_data.py           # file path
    $ python write_data.py maritime_data              # module name
    $ python write_data.py maritime_data.py  out.json # custom output name

The JSON is perfect for re-loading later with the companion
`read_data.py` (or anything that can read JSON).
"""

from __future__ import annotations

import importlib
import importlib.util
import inspect
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable

# ---------------------------------------------------------------------------#
# Helpers                                                                    #
# ---------------------------------------------------------------------------#

_JSON_PRIMITIVES = (int, float, str, bool, list, tuple, dict, type(None))


def _is_serialisable(value: Any) -> bool:
    """
    Recursively check that *value* can be written directly with json.dump.
    """
    if isinstance(value, _JSON_PRIMITIVES):
        if isinstance(value, (list, tuple)):
            return all(_is_serialisable(v) for v in value)
        if isinstance(value, dict):
            return all(
                isinstance(k, (str, int)) and _is_serialisable(v)
                for k, v in value.items()
            )
        return True
    return False


def _dump_module(module: ModuleType, outfile: Path) -> None:
    """
    Scan *module* for public, JSON-friendly globals and write them to *outfile*.
    """
    payload: dict[str, Any] = {}

    for name, obj in module.__dict__.items():
        if name.startswith("_"):  # ignore dunders / private attrs
            continue
        if inspect.ismodule(obj) or inspect.isfunction(obj) or inspect.isclass(obj):
            continue  # skip code objects
        if _is_serialisable(obj):
            payload[name] = obj

    outfile.parent.mkdir(parents=True, exist_ok=True)
    with outfile.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=2, ensure_ascii=False)

    print(f"[✓] Wrote {len(payload):,} variables to '{outfile}'.", flush=True)


def _load_pyfile(path: Path, module_name: str | None = None) -> ModuleType:
    """
    Load the file at *path* as a proper module and return it.
    """
    if not path.suffix == ".py":
        raise ValueError(f"{path} is not a '.py' file")
    spec = importlib.util.spec_from_file_location(module_name or path.stem, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def _parse_cli(argv: list[str]) -> tuple[str, Path]:
    """
    Return (first_arg, output_json_path); exit on bad usage.
    """
    if len(argv) < 2:
        sys.exit("Usage: python write_data.py <module_or_path> [output.json]")
    first_arg = argv[1]
    output = Path(argv[2]) if len(argv) > 2 else Path("instance.json")
    return first_arg, output


# ---------------------------------------------------------------------------#
# Main script                                                                #
# ---------------------------------------------------------------------------#

def main(argv: Iterable[str] | None = None) -> None:
    argv = list(argv or sys.argv)
    first_arg, output_path = _parse_cli(argv)

    maybe_path = Path(first_arg)
    try:
        if maybe_path.suffix == ".py" and maybe_path.exists():
            # Treat the argument as a file path
            module = _load_pyfile(maybe_path)
        else:
            # Treat the argument as a normal importable module name
            module = importlib.import_module(first_arg)
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"Could not load '{first_arg}': {exc}")

    _dump_module(module, output_path)


if __name__ == "__main__":
    main()
