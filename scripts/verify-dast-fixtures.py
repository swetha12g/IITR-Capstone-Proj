#!/usr/bin/env python3
"""Prove selected passive checks against bad/fixed loopback-only fixtures."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
HOOK = '''import http.server, os, threading
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        if os.environ['PF_FIXTURE_FIXED'] == '1':
            self.send_header('Content-Security-Policy', "default-src 'none'; frame-ancestors 'none'")
            self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(b'<!doctype html><html><title>Owned passive fixture</title><p>Study fixture</p></html>')
    def log_message(self, *args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1', 8089), Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
'''


def main():
    pin = json.loads((ROOT / 'locks/scanners/zap.json').read_text())
    run = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    base = ROOT / 'reports/private/day5'
    base.mkdir(parents=True, exist_ok=True)
    # Acquire the large image separately: a cold pull must not consume the
    # short timeout intended for the actual filesystem permission probe.
    with (base / ('fixture-image-' + run + '.log')).open('wb') as log:
        present = subprocess.run(['docker', 'image', 'inspect', pin['image']], stdout=log, stderr=subprocess.STDOUT)
        if present.returncode:
            subprocess.run(['docker', 'pull', pin['image']], check=True, stdout=log, stderr=subprocess.STDOUT, timeout=600)
    results = []
    for fixed in [False, True]:
        label = 'fixed' if fixed else 'bad'
        private = ROOT / 'reports/private/day5' / ('fixture-' + run + '-' + label)
        private.mkdir(parents=True)
        # Prove the hosted-runner mismatch with an actual different-UID write,
        # then prove supplementary group access repairs it without mode0777.
        probe_uid = 65532 if os.getuid() != 65532 else 65533
        private.chmod(0o755)
        probe = ['docker', 'run', '--rm', '--network', 'none', '--user', str(probe_uid) + ':' + str(probe_uid),
                 '--group-add', str(private.stat().st_gid), '-v', str(private) + ':/zap/wrk:rw', pin['image'],
                 'python3', '-c', "from pathlib import Path;Path('/zap/wrk/write-probe').write_text('owned fixture')"]
        with (private / 'access-probe.log').open('wb') as log:
            before_write = subprocess.run(probe, stdout=log, stderr=subprocess.STDOUT, timeout=30).returncode
            private.chmod(0o770)
            after_write = subprocess.run(probe, stdout=log, stderr=subprocess.STDOUT, timeout=30).returncode
        assert before_write != 0 and after_write == 0 and 'PermissionError' in (private / 'access-probe.log').read_text()
        (private / 'write-probe').unlink()
        (private / 'hook.py').write_text(HOOK)
        (private / 'rules.conf').write_text('10038\tFAIL\tMissing CSP\n10021\tFAIL\tMissing nosniff\n')
        name = 'pf-zap-fixture-' + run.lower() + '-' + label
        started = time.monotonic()
        code = None
        try:
            with (private / 'scan.log').open('wb') as log:
                process = subprocess.run(['docker', 'run', '--rm', '--name', name, '--network', 'none',
                    '--group-add', str(private.stat().st_gid),
                    '-e', 'PF_FIXTURE_FIXED=' + str(int(fixed)), '-v', str(private) + ':/zap/wrk:rw', pin['image'],
                    'zap-baseline.py', '--autooff', '-t', 'http://127.0.0.1:8089', '-m', '1', '-T', '3',
                    '-c', 'rules.conf', '-J', 'zap.json', '--hook', '/zap/wrk/hook.py',
                    '-z', '-config api.addrs.addr.name=^(127[.]0[.]0[.]1|0:0:0:0:0:0:0:1|::1|zap)$ -config api.addrs.addr.regex=true'],
                    stdout=log, stderr=subprocess.STDOUT, timeout=240)
                code = process.returncode
        finally:
            subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        report = private / 'zap.json'
        data = json.loads(report.read_text())
        alerts = {str(a['pluginid']) for site in data['site'] for a in site['alerts']}
        selected = {'10038', '10021'} & alerts
        clean = not subprocess.check_output(['docker', 'ps', '-a', '--filter', 'name=^/' + name + '$', '--format', '{{.ID}}']).strip()
        passed = code in ({0, 2} if fixed else {1}) and selected == (set() if fixed else {'10038', '10021'}) and clean
        results.append({'case': label, 'passed': passed, 'exit_code': code, 'selected_alert_ids': sorted(selected),
                        'different_uid_write_before_exit': before_write, 'different_uid_write_after_exit': after_write,
                        'report_sha256': hashlib.sha256(report.read_bytes()).hexdigest(), 'cleanup_verified': clean,
                        'network': 'none; fixture and scanner share container loopback only',
                        'duration_seconds': round(time.monotonic() - started, 2)})
    receipt = {'scanner_image': pin['image'], 'observed_at_utc': datetime.now(timezone.utc).isoformat(),
               'passed': all(r['passed'] for r in results), 'cases': results}
    target = ROOT / 'reports/sanitized/day5/fixture-evidence.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))
    return 0 if receipt['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
