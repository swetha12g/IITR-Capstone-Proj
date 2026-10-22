"""Construct an allowlisted source-free payload; unknown content is never copied."""
import hashlib
import json
import re


class Refused(ValueError):
    """A fixed, content-free refusal; never interpolate untrusted evidence."""


FINDING_KEYS = {'finding_id', 'issue_id', 'scanner_stage', 'rule_id', 'severity', 'original_severity', 'component',
                'version', 'fixed_versions', 'location', 'line', 'first_seen', 'status', 'source_records'}
SAST_RULES = {'pf-sql-template-query', 'pf-eval-input', 'pf-shell-command', 'pf-weak-md5', 'pf-tls-validation-disabled', 'pf-jwt-decode'}
CATEGORIES = {'sast': 'source', 'sca': 'dependency', 'container': 'runtime-package', 'iac': 'configuration',
              'secrets-history': 'credentials', 'secrets-tree': 'credentials', 'dast': 'web'}
VERSION = re.compile(r'[0-9][A-Za-z0-9.+:~_-]{0,79}')


def refuse(condition):
    if not condition:
        raise Refused('payload-refused')


def public_rule(finding, verified_rules):
    rule = finding['rule_id']
    refuse(isinstance(rule, str) and rule.isascii() and rule in verified_rules)
    stage = finding['scanner_stage']
    if stage == 'sast':
        suffix = rule.split('.')[-1]
        refuse(suffix in SAST_RULES)
        return suffix
    if stage.startswith('secrets-'):
        return 'SECRET-DETECTED'
    pattern = r'(?:CVE-\d{4}-\d{4,}|GHSA-[a-z0-9-]{10,}|DSA-\d+-\d+|GHSA-[a-z0-9-]+)' if stage in {'sca', 'container'} else r'(?:CKV(?:2)?_[A-Z0-9_]+|ZAP-\d+)'
    refuse(bool(re.fullmatch(pattern, rule)))
    return rule


def sanitize(findings, verified_rules):
    refuse(isinstance(findings, list) and 0 < len(findings) <= 40)
    payload = []
    aliases = {}
    for finding in findings:
        refuse(isinstance(finding, dict) and set(finding) == FINDING_KEYS)
        refuse(finding['scanner_stage'] in CATEGORIES and finding['severity'] in {'INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL', 'UNKNOWN'})
        refuse(bool(re.fullmatch(r'F-[a-f0-9]{24}', finding['finding_id'])) and bool(re.fullmatch(r'I-[a-f0-9]{24}', finding['issue_id'])))
        rule = public_rule(finding, verified_rules)
        alias = 'C-' + hashlib.sha256((finding['component'] or finding['location']).encode()).hexdigest()[:12]
        item = {'finding_id': finding['finding_id'], 'issue_id': finding['issue_id'], 'rule_id': rule,
                'severity': finding['severity'], 'category': CATEGORIES[finding['scanner_stage']], 'component_alias': alias}
        if finding['version']:
            refuse(isinstance(finding['version'], str) and bool(VERSION.fullmatch(finding['version'])))
            refuse(isinstance(verified_rules, dict) and finding['version'] in verified_rules[rule]['versions'])
            item['verified_version'] = finding['version']
        # Public fixed versions are advisory evidence, never inferred from model text.
        fixed = finding['fixed_versions']
        refuse(isinstance(fixed, list) and len(fixed) <= 20 and all(isinstance(v, str) and VERSION.fullmatch(v) for v in fixed))
        if fixed:
            refuse(isinstance(verified_rules, dict) and set(fixed) <= verified_rules[rule]['fixed_versions'])
        item['verified_fixed_versions'] = fixed
        payload.append(item)
        aliases[alias] = {'component': finding['component'], 'location': finding['location']}
    refuse(len({f['finding_id'] for f in payload}) == len(payload))
    body = json.dumps({'schema_version': 1, 'findings': payload}, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()
    # Only generated aliases, verified identifiers, enums and versions enter this
    # object. Check the actual serialization as a second independent boundary.
    refuse(len(body) <= 40000)
    refuse(not re.search(rb'(?:https?://|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|/home/|/etc/|BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9_-]{12,}|ghp_[A-Za-z0-9]{20,}|```)', body))
    return body, aliases
