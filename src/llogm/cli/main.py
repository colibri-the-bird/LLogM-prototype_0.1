import argparse, json, sys
from pathlib import Path

def _ok(msg): 
    print(msg, file=sys.stderr)

def cmd_sanity(args):
    try:
        from .. import __version__ as v
    except Exception:
        v = "dev"
    _ok(f"LLogM OK, version {v}")
    print(json.dumps({"status": "ok"}))

def cmd_extract(args):
    inp = Path(args.input)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)  # гарантируем, что папка для вывода есть
    lines = inp.read_text(encoding="utf-8").splitlines()
    events = [
        {
            "id": f"e{i+1}",
            "type": "LineEvent",
            "text": ln.strip(),
            "spans": [],
            "concepts": []
        }
        for i, ln in enumerate(lines) if ln.strip()
    ]
    out.write_text(
        json.dumps({"concepts": [], "events": events}, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    _ok(f"wrote {out}")

def build():
    p = argparse.ArgumentParser("llogm")
    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("sanity")
    s1.set_defaults(fn=cmd_sanity)

    s2 = sub.add_parser("extract")
    s2.add_argument("--input", required=True)
    s2.add_argument("--output", required=True)
    s2.set_defaults(fn=cmd_extract)

    return p

def main():
    args = build().parse_args()
    args.fn(args)

if __name__ == "__main__":
    main()
