"""Command-line interface for the Docker Compose Template scaffolder.

Part of Docker Compose Template by Viprasol Tech Private Limited (https://viprasol.com).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import __version__
from .generator import render_compose
from .models import GenerateOptions
from .stacks import get_stack, list_stacks, stack_keys
from .validator import validate_file, validate_text


def _parse_ports(values: Sequence[str] | None) -> dict[str, int]:
    overrides: dict[str, int] = {}
    for raw in values or []:
        if "=" not in raw:
            raise ValueError(f"invalid --port {raw!r}, expected service=port")
        service, _, port = raw.partition("=")
        service = service.strip()
        if not service:
            raise ValueError(f"invalid --port {raw!r}, empty service name")
        try:
            overrides[service] = int(port)
        except ValueError as exc:
            raise ValueError(f"invalid --port {raw!r}, port must be an integer") from exc
    return overrides


def _cmd_list(_: argparse.Namespace) -> int:
    for stack in list_stacks():
        names = ", ".join(svc.name for svc in stack.services)
        print(f"{stack.key:<18} {stack.title}")
        print(f"  {stack.description}")
        print(f"  services: {names}")
    return 0


def _cmd_generate(args: argparse.Namespace) -> int:
    try:
        stack = get_stack(args.stack)
    except KeyError as exc:
        print(str(exc), file=sys.stderr)
        print(f"available: {', '.join(stack_keys())}", file=sys.stderr)
        return 2

    try:
        port_overrides = _parse_ports(args.port)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    options = GenerateOptions(
        project_name=args.name,
        port_overrides=port_overrides,
        with_volumes=not args.no_volumes,
        restart_policy=args.restart,
    )
    text = render_compose(stack, options)

    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        print(f"wrote {args.output}")
    else:
        sys.stdout.write(text)
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    if args.file == "-":
        result = validate_text(sys.stdin.read())
    else:
        result = validate_file(args.file)

    if result.ok:
        print(f"OK: {len(result.service_names)} service(s): {', '.join(result.service_names)}")
        return 0

    print("INVALID:", file=sys.stderr)
    for err in result.errors:
        print(f"  - {err}", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    """Construct the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="dct",
        description="Docker Compose Template — scaffold dev stacks from curated templates.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list available stacks")
    p_list.set_defaults(func=_cmd_list)

    p_gen = sub.add_parser("generate", help="generate a docker-compose.yml")
    p_gen.add_argument("stack", help=f"stack key ({', '.join(stack_keys())})")
    p_gen.add_argument("-n", "--name", default="myapp", help="project name")
    p_gen.add_argument(
        "-p",
        "--port",
        action="append",
        metavar="SERVICE=PORT",
        help="override a service host port (repeatable)",
    )
    p_gen.add_argument("--no-volumes", action="store_true", help="omit named volumes")
    p_gen.add_argument("--restart", default="unless-stopped", help="restart policy")
    p_gen.add_argument("-o", "--output", help="write to file instead of stdout")
    p_gen.set_defaults(func=_cmd_generate)

    p_val = sub.add_parser("validate", help="validate a compose file")
    p_val.add_argument("file", help="path to a compose file, or '-' for stdin")
    p_val.set_defaults(func=_cmd_validate)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the ``dct`` console script."""
    parser = build_parser()
    args = parser.parse_args(argv)
    func = args.func
    result: int = func(args)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
