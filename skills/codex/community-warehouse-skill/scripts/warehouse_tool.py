#!/usr/bin/env python3
"""Small dependency-free client for the Warehouse HTTP Tool API."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def fail(message, code=2):
    print(message, file=sys.stderr)
    raise SystemExit(code)


def config():
    base = os.environ.get("YEYING_WAREHOUSE_URL", "").rstrip("/")
    token = os.environ.get("YEYING_WAREHOUSE_TOOL_TOKEN", "") or os.environ.get("YEYING_WAREHOUSE_TOKEN", "")
    if not base:
        fail("YEYING_WAREHOUSE_URL is required")
    if not token:
        fail("YEYING_WAREHOUSE_TOOL_TOKEN or YEYING_WAREHOUSE_TOKEN is required")
    return base, token


def request(method, path, token, payload=None):
    body = None
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
            value = json.loads(raw.decode("utf-8")) if raw else {}
            print(json.dumps(value, ensure_ascii=False, indent=2))
            return 0
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.dumps(json.loads(raw), ensure_ascii=False)
        except json.JSONDecodeError:
            detail = raw
        print("Warehouse HTTP %d: %s" % (exc.code, detail), file=sys.stderr)
        return 10 if exc.code in (401, 403, 409, 412, 413) else 11
    except urllib.error.URLError as exc:
        print("Warehouse connection failed: %s" % exc.reason, file=sys.stderr)
        return 12


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("catalog")
    call = sub.add_parser("call")
    call.add_argument("name")
    call.add_argument("arguments", nargs="?", default="{}", help="JSON object")
    put = sub.add_parser("put")
    put.add_argument("path")
    put.add_argument("content")
    put.add_argument("--content-type", default="text/markdown; charset=utf-8")
    put.add_argument("--encoding", choices=("utf-8", "base64"), default="utf-8")
    put.add_argument("--overwrite", action="store_true")
    read = sub.add_parser("read")
    read.add_argument("path")
    read.add_argument("--max-bytes", type=int)
    listing = sub.add_parser("list")
    listing.add_argument("prefix", nargs="?", default="/")
    listing.add_argument("--delimiter", default="/")
    stat = sub.add_parser("stat")
    stat.add_argument("path")
    args = parser.parse_args()
    base, token = config()

    if args.command == "catalog":
        return request("GET", base + "/api/v1/public/tools/warehouse", token)
    if args.command == "call":
        try:
            arguments = json.loads(args.arguments)
        except json.JSONDecodeError as exc:
            fail("arguments must be valid JSON: %s" % exc)
        if not isinstance(arguments, dict):
            fail("arguments must be a JSON object")
        return request("POST", base + "/api/v1/public/tools/warehouse/call", token,
                       {"name": args.name, "arguments": arguments})
    if args.command == "put":
        return request("POST", base + "/api/v1/public/tools/warehouse/call", token, {
            "name": "warehouse.object.put",
            "arguments": {"path": args.path, "content": args.content,
                           "encoding": args.encoding, "contentType": args.content_type,
                           "overwrite": args.overwrite},
        })
    if args.command == "read":
        arguments = {"path": args.path, "mode": "content"}
        if args.max_bytes is not None:
            arguments["maxBytes"] = args.max_bytes
        return request("POST", base + "/api/v1/public/tools/warehouse/call", token,
                       {"name": "warehouse.object.read", "arguments": arguments})
    if args.command == "list":
        return request("POST", base + "/api/v1/public/tools/warehouse/call", token,
                       {"name": "warehouse.object.list", "arguments":
                        {"prefix": args.prefix, "delimiter": args.delimiter}})
    return request("POST", base + "/api/v1/public/tools/warehouse/call", token,
                   {"name": "warehouse.object.stat", "arguments": {"path": args.path}})


if __name__ == "__main__":
    raise SystemExit(main())
