"""Audited public HTTP downloads with a conservative global 10 GB budget."""

import json
import urllib.request
import urllib.parse
import datetime
from droid2sim.paths import ROOT

LEDGER = ROOT / "downloads.json"
LIMIT = 9_000_000_000  # additionally reserve 1 GB for dependencies/docs/protocol overhead


def log(s):
    with (ROOT / "LOG.md").open("a") as f:
        f.write("\n- " + datetime.datetime.now(datetime.timezone.utc).isoformat() + " " + s + "\n")


def fetch(url, target):
    target = ROOT / target
    target.parent.mkdir(parents=True, exist_ok=True)
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else []
    if target.exists() and any(
        x["file"] == str(target.relative_to(ROOT)) and x.get("complete") for x in ledger
    ):
        return target
    log(f"Download: `python download.py {url} {target.relative_to(ROOT)}`")
    entry = dict(url=url, file=str(target.relative_to(ROOT)), bytes=0, complete=False)
    ledger.append(entry)
    try:
        with urllib.request.urlopen(url, timeout=90) as r, target.open("wb") as f:
            size = int(r.headers.get("Content-Length", 0))
            if sum(x["bytes"] for x in ledger) + size >= LIMIT:
                raise RuntimeError("Download budget exceeded")
            while chunk := r.read(1024 * 1024):
                if sum(x["bytes"] for x in ledger) + len(chunk) >= LIMIT:
                    raise RuntimeError("Download budget exceeded")
                f.write(chunk)
                entry["bytes"] += len(chunk)
            entry["complete"] = True
    finally:
        LEDGER.write_text(json.dumps(ledger, indent=2))
        log(
            f"Download result: {entry}; cumulative payload {sum(x['bytes'] for x in ledger):,} bytes (+ reserved dependency allowance)."
        )
    return target


def listing(prefix, target):
    url = "https://storage.googleapis.com/storage/v1/b/gresearch/o?" + urllib.parse.urlencode(
        {"prefix": prefix, "maxResults": 1000}
    )
    return json.loads(fetch(url, target).read_text())


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="'sample' or a public HTTP URL")
    parser.add_argument("target", nargs="?", help="Destination relative to the repository")
    args = parser.parse_args(argv)
    if args.source == "sample":
        manifest = listing("robotics/droid_100/", "sources/sample_listing.json")
        if "nextPageToken" in manifest:
            raise RuntimeError("Unexpected >1000 sample files")
        items = manifest.get("items", [])
        print("Sample bytes", sum(int(item.get("size", 0)) for item in items), flush=True)
        for item in items:
            if int(item.get("size", 0)):
                fetch(
                    "https://storage.googleapis.com/gresearch/"
                    + urllib.parse.quote(item["name"], safe="/"),
                    "data/" + item["name"].removeprefix("robotics/"),
                )
    else:
        if not args.target:
            parser.error("A destination is required for URL downloads")
        fetch(args.source, args.target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
