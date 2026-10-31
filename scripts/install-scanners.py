#!/usr/bin/env python3
"""Install hash-pinned official scanner distributions into project-local tools."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / ".tools/day3"
PRIVATE = ROOT / "reports/private/day3"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if sys.version_info[:2] != (3, 10) or platform.system() != "Linux" or platform.machine() != "x86_64":
        raise RuntimeError("Scanner lock requires Python 3.10 on Linux x86_64")
    TOOLS.mkdir(parents=True, exist_ok=True)
    PRIVATE.mkdir(parents=True, exist_ok=True)
    pins = json.loads((ROOT / "locks/scanners/tools.json").read_text())
    lock = ROOT / pins["semgrep"]["requirements"]
    assert sha(lock) == pins["semgrep"]["requirements_sha256"]
    env = os.environ.copy()
    home = PRIVATE / "bootstrap-home"
    home.mkdir(exist_ok=True)
    env.update({"HOME": str(home), "PIP_CONFIG_FILE": os.devnull,
                "PIP_INDEX_URL": "https://pypi.org/simple", "PIP_EXTRA_INDEX_URL": "",
                "PIP_CACHE_DIR": str(TOOLS / "pip-cache"), "SEMGREP_SEND_METRICS": "off",
                "SEMGREP_ENABLE_VERSION_CHECK": "0", "SEMGREP_APP_TOKEN": "",
                "SEMGREP_SETTINGS_FILE": str(home / "semgrep-settings.yml")})
    with (PRIVATE / "scanner-bootstrap.log").open("ab") as output:
        venv = TOOLS / "semgrep"
        if not (venv / "bin/python").exists():
            subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(venv)], check=True, env=env, stdout=output, stderr=subprocess.STDOUT)
        subprocess.run([sys.executable, "-m", "pip", "--python", str(venv / "bin/python"), "install",
                        "--disable-pip-version-check", "--require-hashes", "--only-binary=:all:", "-r", str(lock)],
                       check=True, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=600)
        for name in ["trivy", "gitleaks"]:
            pin = pins[name]
            archive = TOOLS / pin["archive"]
            if not archive.is_file() or sha(archive) != pin["sha256"]:
                subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location", "--connect-timeout", "20",
                                "--max-time", "180", "--retry", "2", pin["url"], "--output", str(archive)],
                               check=True, stdout=output, stderr=subprocess.STDOUT, timeout=600)
            assert sha(archive) == pin["sha256"]
            with tarfile.open(archive) as source:
                member = next(m for m in source.getmembers() if m.name == name and m.isfile())
                (TOOLS / name).write_bytes(source.extractfile(member).read())
            (TOOLS / name).chmod(0o755)
    versions = {}
    for name, executable, args in [("semgrep", TOOLS / "semgrep/bin/semgrep", ["--version"]),
                                   ("trivy", TOOLS / "trivy", ["--version"]), ("gitleaks", TOOLS / "gitleaks", ["version"])]:
        version = subprocess.check_output([str(executable), *args], env=env, text=True, timeout=30).strip()
        assert pins[name]["version"] in version
        versions[name] = {"version": pins[name]["version"], "distribution_hash_verified": True}
    public = ROOT / "reports/sanitized/day3"
    public.mkdir(parents=True, exist_ok=True)
    summary = {"tools": versions, "semgrep_hashed_distributions": sum(bool(line.strip()) for line in lock.read_text().splitlines()),
               "platform": "linux-x86_64", "python": "3.10", "system_installation": False}
    (public / "tools-verification.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
