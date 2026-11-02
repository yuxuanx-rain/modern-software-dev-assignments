"""Recompute comparable tables from unmodified Factory report payloads.

This is an explicit course-template regrouping, not Factory's official pillar weights.
Run from any directory: python3 week5/recompute.py
"""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parent
GROUPS = {
    'Style & Validation': 'lint_config type_check formatter pre_commit_hooks strict_typing naming_consistency',
    'Build System': 'build_cmd_doc deps_pinned vcs_cli_tools automated_pr_review agentic_development fast_ci_feedback build_performance_tracking deployment_frequency single_command_setup feature_flag_infrastructure release_notes_automation progressive_rollout rollback_automation monorepo_tooling release_automation dead_feature_flag_detection',
    'Testing': 'unit_tests_exist integration_tests_exist unit_tests_runnable test_performance_tracking flaky_test_detection test_coverage_thresholds test_naming_conventions test_isolation interactive_qa_exists interactive_qa_runnable',
    'Documentation': 'agents_md readme automated_doc_generation skills documentation_freshness api_schema_docs service_flow_documented agents_md_validation',
    'Dev Environment': 'devcontainer env_template local_services_setup database_schema devcontainer_runnable',
    'Code Quality': 'cyclomatic_complexity large_file_detection dead_code_detection duplicate_code_detection code_modularization tech_debt_tracking n_plus_one_detection heavy_dependency_detection unused_dependencies_detection version_drift_detection',
    'Observability': 'structured_logging distributed_tracing metrics_collection code_quality_metrics error_tracking_contextualized alerting_configured runbooks_documented deployment_observability health_checks circuit_breakers profiling_instrumentation',
    'Security & Governance': 'branch_protection secret_scanning codeowners automated_security_review dependency_update_automation gitignore_comprehensive dast_scanning pii_handling privacy_compliance secrets_management log_scrubbing min_release_age',
    'Task Discovery (additional)': 'issue_templates issue_labeling_system backlog_health pr_templates',
    'Product & Experimentation (additional)': 'product_analytics_instrumentation error_to_insight_pipeline',
}
GROUPS = {k: v.split() for k, v in GROUPS.items()}
NATIVE_GROUPS = {k: list(v) for k, v in GROUPS.items() if k != 'Code Quality'}
NATIVE_GROUPS['Style & Validation'] += 'cyclomatic_complexity large_file_detection dead_code_detection duplicate_code_detection code_modularization tech_debt_tracking n_plus_one_detection'.split()
NATIVE_GROUPS['Build System'] += 'heavy_dependency_detection unused_dependencies_detection version_drift_detection'.split()
all_ids = [c for ids in GROUPS.values() for c in ids]
assert len(all_ids) == len(set(all_ids)) == 84
native_ids = [c for ids in NATIVE_GROUPS.values() for c in ids]
assert len(native_ids) == len(set(native_ids)) == 84 and set(native_ids) == set(all_ids)
level_metadata = json.loads((ROOT / 'evidence/criterion-levels.json').read_text())
assert set(all_ids) == {c['id'] for c in level_metadata}
reports = {}
original_reports = {}
for name in ('dayjs', 'yt-dlp', 'caddy'):
    file = ROOT / 'evidence' / f'{name}-report.json'
    if not file.exists():
        raise SystemExit(f'Waiting for {name} report')
    payload = json.loads(file.read_text())
    report = payload['report']
    original_reports[name] = report
    assert set(report) == set(all_ids)
    assert all(v['denominator'] == 1 and v['numerator'] in (0, 1, None) for v in report.values())
    for meta in level_metadata:
        assert report[meta['id']]['numerator'] is not None or meta['skippable'], meta['id']
    passed = sum(v['numerator'] == 1 for v in report.values())
    failed = sum(v['numerator'] == 0 for v in report.values())
    skipped = sum(v['numerator'] is None for v in report.values())
    evaluated = passed + failed
    rate = passed / evaluated
    level = min(5, int(rate * 5) + 1)
    next_threshold = level / 5
    needed = max(0, math.ceil(next_threshold * evaluated - 1e-10) - passed) if level < 5 else 0
    groups = {}
    for group, ids in GROUPS.items():
        groups[group] = {
            'passed': sum(report[c]['numerator'] == 1 for c in ids),
            'failed': [c for c in ids if report[c]['numerator'] == 0],
            'skipped': [c for c in ids if report[c]['numerator'] is None],
        }
        groups[group]['evaluated'] = groups[group]['passed'] + len(groups[group]['failed'])
    reports[name] = dict(passed=passed, failed=failed, skipped=skipped, evaluated=evaluated,
                         pass_rate=round(rate * 100, 4), level=level,
                         additional_passes_to_next_level_fixed_denominator=needed,
                         groups=groups)

result = {'grouping_note': 'Analyst mapping to the eight course pillars plus two supplemental groups; no original criterion scores changed.',
          'groups': GROUPS, 'native_groups': NATIVE_GROUPS, 'reports': reports}
common = [c for c in all_ids if all(r[c]['numerator'] is not None for r in original_reports.values())]
result['common_evaluated_criteria'] = common
result['common_evaluated_scores'] = {
    name: {'passed': sum(report[c]['numerator'] for c in common), 'evaluated': len(common)}
    for name, report in original_reports.items()
}
# Exclude observer-dependent checks symmetrically, without changing raw scores.
# Execution checks depend on the local toolchain or documentation fallback;
# history checks cannot be established reliably from depth-one clones.
exclusions = {
    'vcs_cli_tools': 'The auditing machine lacks authenticated gh/glab.',
    'unit_tests_runnable': 'Dependencies or a supported runtime were unavailable.',
    'interactive_qa_runnable': 'Failed locally or passed through documentation fallback, not a successful live run.',
    'devcontainer_runnable': 'The local devcontainer CLI was unavailable.',
    'agentic_development': 'A depth-one clone cannot establish historical adoption; absence of local workflows is narrower evidence.',
    'documentation_freshness': 'Shallow boundary commits do not reliably establish document modification dates.',
}
filtered_common = [c for c in common if c not in exclusions]
result['observer_sensitivity'] = {
    'note': 'Analyst sensitivity calculation only. Exclusions are applied to all repositories, including affected passes. No official score or maturity level is reassigned.',
    'excluded_criteria': exclusions,
    'per_repo_scores': {},
    'common_criteria': filtered_common,
    'common_scores': {},
}
for name, report in original_reports.items():
    remaining = [c for c in all_ids if c not in exclusions and report[c]['numerator'] is not None]
    result['observer_sensitivity']['per_repo_scores'][name] = {
        'passed': sum(report[c]['numerator'] for c in remaining), 'evaluated': len(remaining),
    }
    result['observer_sensitivity']['common_scores'][name] = {
        'passed': sum(report[c]['numerator'] for c in filtered_common), 'evaluated': len(filtered_common),
    }
result['pooled_pillar_counts'] = {
    group: {'passed': sum(r['groups'][group]['passed'] for r in reports.values()),
            'failed': sum(len(r['groups'][group]['failed']) for r in reports.values()),
            'evaluated': sum(r['groups'][group]['evaluated'] for r in reports.values())}
    for group in GROUPS
}
(ROOT / 'evidence/comparison.json').write_text(json.dumps(result, indent=2) + '\n')
lines = ['| Comparison basis | Day.js | yt-dlp | Caddy |', '|---|---:|---:|---:|']
variants = [
    ('Original Factory results', {name: {'passed': r['passed'], 'evaluated': r['evaluated']} for name, r in reports.items()}),
    ('Criteria evaluated in all three', result['common_evaluated_scores']),
    ('After excluding six observer/history-sensitive checks', result['observer_sensitivity']['per_repo_scores']),
    ('Common criteria after those exclusions', result['observer_sensitivity']['common_scores']),
]
for label, scores in variants:
    cells = [f"{s['passed']}/{s['evaluated']} ({100*s['passed']/s['evaluated']:.2f}%)" for s in scores.values()]
    lines.append('| ' + label + ' | ' + ' | '.join(cells) + ' |')
(ROOT / 'evidence/sensitivity-table.md').write_text('\n'.join(lines) + '\n')
lines = ['| Current Factory category | Day.js | yt-dlp | Caddy |', '|---|---:|---:|---:|']
for group, ids in NATIVE_GROUPS.items():
    cells = []
    for name, report in original_reports.items():
        passed = sum(report[c]['numerator'] == 1 for c in ids)
        evaluated = sum(report[c]['numerator'] is not None for c in ids)
        skipped = len(ids) - evaluated
        cells.append(f'{passed}/{evaluated} ({100*passed/evaluated:.1f}%); {skipped} N/A' if evaluated else f'N/A; {skipped} skipped')
    display = {'Dev Environment': 'Development Environment', 'Observability': 'Debugging & Observability',
               'Security & Governance': 'Security', 'Task Discovery (additional)': 'Task Discovery',
               'Product & Experimentation (additional)': 'Product & Experimentation'}.get(group, group)
    lines.append('| ' + display + ' | ' + ' | '.join(cells) + ' |')
(ROOT / 'evidence/native-pillar-table.md').write_text('\n'.join(lines) + '\n')
lines = ['| Pillar | Day.js | yt-dlp | Caddy |', '|---|---:|---:|---:|']
for group in GROUPS:
    cells = []
    for name in reports:
        g = reports[name]['groups'][group]
        e = g['evaluated']
        cells.append(f"{g['passed']}/{e} ({100*g['passed']/e:.1f}%); {len(g['skipped'])} N/A" if e else f"N/A; {len(g['skipped'])} skipped")
    lines.append('| ' + group + ' | ' + ' | '.join(cells) + ' |')
(ROOT / 'evidence/pillar-table.md').write_text('\n'.join(lines) + '\n')
lines = ['| Pillar | Day.js | yt-dlp | Caddy |', '|---|---|---|---|']
for group in GROUPS:
    cells = []
    for name in reports:
        ids = reports[name]['groups'][group]['failed']
        cells.append(', '.join(f'`{c}`' for c in ids) or 'None')
    lines.append('| ' + group + ' | ' + ' | '.join(cells) + ' |')
(ROOT / 'evidence/failures-table.md').write_text('\n'.join(lines) + '\n')
for name, r in reports.items():
    print(name, {k: v for k, v in r.items() if k != 'groups'})
print('\n'.join((ROOT / 'evidence/pillar-table.md').read_text().splitlines()))
