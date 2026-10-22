"""Reject malformed, omitted, invented and ungrounded triage output."""
import json
import re
from jsonschema import Draft202012Validator


SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['triage'], 'properties': {
    'triage': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False,
        'required': ['finding_id', 'issue_id', 'priority', 'reason', 'fix', 'references', 'operation'], 'properties': {
            'finding_id': {'type': 'string'}, 'issue_id': {'type': 'string'},
            'priority': {'type': 'string', 'enum': ['P1', 'P2', 'P3']},
            'reason': {'type': 'string', 'minLength': 1, 'maxLength': 400},
            'fix': {'type': 'array', 'minItems': 3, 'maxItems': 5, 'items': {'type': 'string', 'minLength': 1, 'maxLength': 300}},
            'references': {'type': 'array', 'items': {'type': 'string'}},
            'operation': {'type': 'string', 'enum': ['manual-review', 'disable-sa-token', 'require-nonroot', 'add-liveness-probe']}
        }}}}}
OPERATIONS = {'CKV_K8S_38': 'disable-sa-token', 'CKV_K8S_23': 'require-nonroot', 'CKV_K8S_8': 'add-liveness-probe'}


class InvalidTriage(ValueError):
    pass


def validate(response, payload):
    if any(Draft202012Validator(SCHEMA).iter_errors(response)):
        raise InvalidTriage('triage-schema-invalid')
    inputs = {f['finding_id']: f for f in payload['findings']}
    seen = []
    for item in response['triage']:
        finding = inputs.get(item['finding_id'])
        if finding is None or item['issue_id'] != finding['issue_id']:
            raise InvalidTriage('triage-unknown-finding-or-cluster')
        seen.append(item['finding_id'])
        allowed = {'manual-review', OPERATIONS.get(finding['rule_id'], 'manual-review')}
        if item['operation'] not in allowed:
            raise InvalidTriage('triage-unsupported-operation')
        if any(ref != finding['rule_id'] for ref in item['references']):
            raise InvalidTriage('triage-invented-reference')
        text = json.dumps([item['reason'], item['fix']])
        if any(ref != finding['rule_id'] for ref in re.findall(r'(?:CVE-\d{4}-\d{4,}|GHSA-[A-Za-z0-9-]+|CKV(?:2)?_[A-Z0-9_]+)', text)):
            raise InvalidTriage('triage-invented-reference')
        versions = re.findall(r'\b\d+\.\d+(?:\.\d+)?(?:[-+~][A-Za-z0-9.-]+)?', text)
        if any(v not in finding['verified_fixed_versions'] + [finding.get('verified_version')] for v in versions):
            raise InvalidTriage('triage-invented-version')
        if re.search(r'https?://|/home/|/etc/|```|BEGIN .*PRIVATE KEY|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', text):
            raise InvalidTriage('triage-unsafe-content')
    if len(seen) != len(set(seen)) or set(seen) != set(inputs):
        raise InvalidTriage('triage-omitted-or-duplicate-finding')
    return response
