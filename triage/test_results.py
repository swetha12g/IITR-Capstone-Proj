"""Extract only numeric test totals from supported runner summaries."""
import re


def parse_test_totals(output, runner):
    output = re.sub(r'\x1b\[[0-9;]*m', '', output)
    if runner == 'node':
        values = {}
        for key in ('tests', 'pass', 'fail', 'cancelled', 'skipped', 'todo'):
            matches = re.findall(r'^(?:ℹ|#)\s+' + key + r'\s+(\d+)\s*$', output, re.M)
            if len(matches) != 1:
                raise ValueError('missing or ambiguous Node test totals')
            values[key] = int(matches[0])
        if values['tests'] != sum(values[k] for k in ('pass', 'fail', 'cancelled', 'skipped', 'todo')):
            raise ValueError('inconsistent Node test totals')
        return {'passed': values['pass'], 'failed': values['fail'], 'skipped': values['skipped'],
                'cancelled': values['cancelled'], 'todo': values['todo'], 'total': values['tests']}
    if runner == 'vitest':
        matches = re.findall(r'^\s*Tests\s+(.+?)\s+\((\d+)\)\s*$', output, re.M)
        if len(matches) != 1:
            raise ValueError('missing or ambiguous Vitest test totals')
        parts, total = matches[0]
        values = {key: 0 for key in ('passed', 'failed', 'skipped', 'todo')}
        for number, key in re.findall(r'(\d+) (passed|failed|skipped|todo)', parts):
            values[key] += int(number)
        if sum(values.values()) != int(total):
            raise ValueError('inconsistent Vitest test totals')
        return {**values, 'cancelled': 0, 'total': int(total)}
    raise ValueError('unsupported test runner')
