from hashlib import sha256
from importlib.metadata import version
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
versions = {}
for requirement in (root / "requirements.txt").read_text().splitlines():
    name, expected = requirement.split("==")
    versions[name] = version(name)
    if versions[name] != expected:
        raise SystemExit(f"{name}: expected {expected}, found {versions[name]}")

for language in ("c", "python"):
    (root / "generated" / language).mkdir(parents=True, exist_ok=True)
plugin = Path(sys.executable).parent / "protoc-gen-nanopb"
subprocess.run([
    sys.executable, "-m", "grpc_tools.protoc", "-I.",
    f"--plugin=protoc-gen-nanopb={plugin}",
    "--nanopb_out=../generated/c", "--python_out=../generated/python",
    *[p.name for p in sorted((root / "proto").glob("*.proto"))],
], cwd=root / "proto", check=True)
sources = sorted((root / "proto").glob("*.proto")) + sorted((root / "proto").glob("*.options"))
manifest = {
    "versions": versions,
    "sources": {p.name: sha256(p.read_bytes()).hexdigest() for p in sources},
}
(root / "generated" / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print("Generated nanopb C and Python codecs; recorded schema hashes and tool versions.")
