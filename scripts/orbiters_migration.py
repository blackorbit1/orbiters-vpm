"""Keep the existing VCC URL working, switching its landing page only after parity."""
import json
import os
import urllib.request
from pathlib import Path

DESTINATION = "https://orbiters.cc/vpm/orbiters"
FEED = DESTINATION + "/index.json"
OLD_FEED = "https://blackorbit1.github.io/orbiters-vpm/index.json"


def read_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Orbiters-VPM-Migration/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read(8 * 1024 * 1024 + 1)
    if len(data) > 8 * 1024 * 1024:
        raise ValueError("Catalog is unexpectedly large")
    return json.loads(data)


def verify(candidate, existing):
    if candidate.get("id") != "cc.orbiters.vpm" or candidate.get("url") != FEED:
        raise ValueError("Orbiters has not published the canonical repository yet")
    packages = candidate.get("packages", {})
    if not packages and existing.get("url") != FEED:
        raise ValueError("Orbiters catalog is empty")
    # The first handover must preserve all versions and checksums. Once the old
    # catalog has the canonical URL, future deliberate hide/remove choices apply.
    if existing.get("url") != FEED:
        for name, package in existing.get("packages", {}).items():
            for version, old in package["versions"].items():
                new = packages.get(name, {}).get("versions", {}).get(version)
                if not new or new.get("zipSHA256") != old.get("zipSHA256") or new.get("url") != old.get("url"):
                    raise ValueError(f"Migration has not preserved {name} {version}")
    for name, package in packages.items():
        for version, manifest in package["versions"].items():
            if manifest.get("name") != name or manifest.get("version") != version or not manifest.get("zipSHA256"):
                raise ValueError("Invalid package manifest")


def write_site(feed):
    output = Path("Website")
    output.mkdir(exist_ok=True)
    (output / "index.json").write_text(json.dumps(feed, ensure_ascii=False), encoding="utf-8")
    (output / "index.html").write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0;url={DESTINATION}"><link rel="canonical" href="{DESTINATION}"><title>Orbiters VPM</title><body><p>The Orbiters package listing has moved. <a href="{DESTINATION}">Open Orbiters VPM</a>.</p><script>location.replace({json.dumps(DESTINATION)} + location.search + location.hash);</script></body></html>''', encoding="utf-8")


def main():
    ready = False
    existing = read_json(OLD_FEED)
    try:
        candidate = read_json(FEED)
        verify(candidate, existing)
        write_site(candidate)
        ready = True
        print("Orbiters is ready. Publishing the redirect and canonical feed mirror.")
    except Exception as error:
        print(f"Orbiters handover deferred: {type(error).__name__}: {error}")
        if existing.get("url") == FEED:
            write_site(existing)
            ready = True
            print("Preserving the last canonical feed; hidden versions will not reappear during an outage.")
        else:
            print("The original listing build will run; existing VCC installations remain supported.")
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        output.write(f"ready={str(ready).lower()}\n")


if __name__ == "__main__":
    main()
