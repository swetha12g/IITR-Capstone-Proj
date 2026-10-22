#!/usr/bin/env python3
"""Recompute a public, source-free study dashboard from private normalized data."""
import argparse
from collections import Counter
import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scores(labels):
    result = Counter({'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0})
    for row in labels:
        truth, detected = row['ground_truth_positive'], row['detected']
        if type(truth) is not bool or type(detected) is not bool:
            raise ValueError('labels must be explicit booleans')
        result['TP' if truth and detected else 'FN' if truth else 'FP' if detected else 'TN'] += 1
    tp, fp, fn = result['TP'], result['FP'], result['FN']
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = 2 * precision * recall / (precision + recall) if precision is not None and recall is not None and precision + recall else None
    return {**result, 'precision': precision, 'recall': recall, 'f1': f1, 'sample_size': len(labels),
            'introduced_known_issues': tp + fn, 'caught_known_issues': tp, 'missed_known_issues': fn,
            'fixture_target_80_percent_met': recall >= 0.8 if recall is not None else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--findings', type=Path, required=True)
    parser.add_argument('--labels', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    normalized = json.loads(args.findings.read_text())
    labels = json.loads(args.labels.read_text())
    stages = {s: Counter() for s in ['sast', 'sca', 'secrets', 'iac', 'container', 'dast']}
    for finding in normalized['findings']:
        stage = 'secrets' if finding['scanner_stage'].startswith('secrets-') else finding['scanner_stage']
        stages[stage][finding['severity']] += 1
    stage_labels = {s: scores([r for r in labels['labels'] if r['stage'] == s]) for s in stages}
    day4 = json.loads((ROOT / 'reports/sanitized/day4/gate-summary.json').read_text())
    container_path = ROOT / 'reports/sanitized/pipeline/container.json'
    container = json.loads(container_path.read_text()) if container_path.exists() else {}
    critical_issues = len({f['issue_id'] for f in normalized['findings'] if f['severity'] == 'CRITICAL'})
    durations = []
    for stage in stages:
        p = ROOT / 'reports/sanitized/pipeline' / (stage + '.json')
        if p.exists():
            d = json.loads(p.read_text());durations.append({'stage': stage, 'seconds': d['duration_seconds'], 'observations': 1})
    result = {'schema_version': 1, 'scope': labels['scope'], 'labels_independently_human_reviewed': False,
              'counts': normalized['counts'], 'critical_issues': critical_issues, 'stage_observations': {s: dict(c) for s, c in stages.items()},
              'detection': scores(labels['labels']), 'detection_by_stage': stage_labels, 'stage_durations': durations,
              'timing_note': 'One observation per available stage; no percentile or end-to-end timing inferred from separate runs.',
              'image_comparison': day4['comparison'], 'image_vulnerabilities': {k: v['by_severity'] for k, v in day4['container'].items()},
              'sbom_components': container.get('sbom', day4['sbom'])['components'], 'current_container_image_id': container.get('image_config_id'),
              'database_updated_at': day4['database']['metadata']['UpdatedAt'], 'database_scope': 'historical Day 4 comparison',
              'deferred_day4_findings': day4.get('deferred_findings', day4.get('blockers')), 'production_readiness_claimed': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    with args.output.with_suffix('.csv').open('w', newline='') as output:
        writer = csv.writer(output, lineterminator='\n');writer.writerow(['stage', 'severity', 'observations'])
        for stage, counts in stages.items():
            for severity, count in sorted(counts.items()):writer.writerow([stage, severity, count])
    metric = result['detection']
    cards = [('Underlying issues', normalized['counts']['unique_issues']), ('Scanner observations', normalized['counts']['observations']),
             ('Critical issues', critical_issues), ('Known fixture misses', metric['FN']), ('SBOM components', result['sbom_components'])]
    cards_html = ''.join('<div class="card"><span>' + html.escape(label) + '</span><strong>' + str(value) + '</strong></div>' for label, value in cards)
    rows = ''.join('<tr><td>' + stage.upper() + '</td><td>' + str(sum(counts.values())) + '</td><td>' + str(counts.get('CRITICAL', 0)) + '</td><td>' + str(counts.get('HIGH', 0)) + '</td><td>' + str(stage_labels[stage]['TP']) + '</td><td>' + str(stage_labels[stage]['FN']) + '</td></tr>' for stage, counts in stages.items())
    percent = lambda v: 'N/A' if v is None else f'{100*v:.1f}%'
    document = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PipelineFortress study evidence</title>
<style>body{margin:0;background:#f4f7fa;color:#153047;font:16px system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:44px 24px}h1{font-size:38px;margin:8px 0}h2{font-size:23px;margin-top:34px}.eyebrow{letter-spacing:.12em;color:#256b78;font-size:12px}.banner{padding:16px 20px;background:#fff1d3;border-left:4px solid #bc7c13;border-radius:5px;line-height:1.6}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px;margin:24px 0}.card{background:white;border:1px solid #dce6ec;border-radius:10px;padding:20px}.card span{display:block;color:#526c7b;font-size:14px}.card strong{font-size:36px;display:block;margin-top:8px;color:#166e79}table{background:white;border-collapse:collapse;width:100%;border-radius:8px;overflow:hidden}th,td{padding:14px;text-align:left;border-bottom:1px solid #e0e8ee}th{background:#153047;color:white;font-size:13px}.muted{color:#526c7b;line-height:1.7}.metrics{display:flex;gap:24px;flex-wrap:wrap;padding:20px;background:white;border-radius:8px}.metrics strong{color:#166e79}.foot{font-size:13px;margin-top:32px;border-top:1px solid #d4e0e8;padding-top:20px}a{color:#166e79}</style>
<main><div class="eyebrow">CAP-DSE-3W · OWNED STUDY LAB</div><h1>PipelineFortress</h1><p class="muted">Measured scanner evidence, known misses and deferred remediation.</p><div class="banner"><b>Study execution continues with deferred risks.</b> Security findings remain visible. This dashboard does not claim production readiness, complete CIS coverage or successful live AI evaluation.</div><div class="cards">CARDS</div><h2>Six scan stages</h2><table><thead><tr><th>Stage</th><th>Observations</th><th>Critical</th><th>High</th><th>Fixture TP</th><th>Fixture FN</th></tr></thead><tbody>ROWS</tbody></table><h2>Curated detection evaluation</h2><div class="metrics"><span>Precision <strong>PRECISION</strong></span><span>Recall <strong>RECALL</strong></span><span>F1 <strong>FONE</strong></span><span>Labeled cases <strong>SAMPLES</strong></span></div><p class="muted">This is a small, post-hoc fixture/control set. It includes a verified authorization miss. The fixture target cannot be generalized to all real application vulnerabilities; labels are not independently human reviewed.</p><h2>Historical Day 4 image comparison</h2><p class="muted">Before critical remediation: baseline image 101 vulnerability identities, original hardened image 100. One unknown CA advisory was removed, with no new identities in the frozen-DB comparison. These historical counts predate the critical fixes. Current critical counts appear in the cards and stage table above; the inventory card uses the latest container receipt. The NetworkPolicy gap remains deferred.</p><p class="foot">Source-free exports: <a href="JSONFILE">dashboard JSON</a> · <a href="CSVFILE">stage CSV</a>. No raw finding text, source, credentials or private locations are embedded.</p></main></html>'''
    for key, value in {'CARDS': cards_html, 'ROWS': rows, 'PRECISION': percent(metric['precision']), 'RECALL': percent(metric['recall']),
                       'FONE': percent(metric['f1']), 'SAMPLES': str(metric['sample_size']), 'JSONFILE': args.output.with_suffix('.json').name,
                       'CSVFILE': args.output.with_suffix('.csv').name}.items():document = document.replace(key, value)
    args.output.write_text(document)
    print(json.dumps({'output': str(args.output.resolve().relative_to(ROOT)), 'detection': metric}))


if __name__ == '__main__':
    main()
