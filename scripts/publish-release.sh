#!/usr/bin/env bash
# Publish only a tagged main revision with a successful complete study pipeline.
set -euo pipefail
: "${RELEASE_TAG:?release tag required}"
: "${GITHUB_SHA:?tag commit required}"
: "${GITHUB_REPOSITORY:?repository required}"
[[ "$RELEASE_TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo 'Invalid release tag' >&2; exit 1; }
[[ "$GITHUB_SHA" =~ ^[a-f0-9]{40}$ ]] || { echo 'Invalid commit identity' >&2; exit 1; }
notes="docs/releases/$RELEASE_TAG.md"
[[ -s "$notes" ]] || { echo 'Release notes missing' >&2; exit 1; }
main_sha="$(gh api "repos/$GITHUB_REPOSITORY/git/ref/heads/main" --jq '.object.sha')"
[[ "$main_sha" == "$GITHUB_SHA" ]] || { echo 'Tag must identify the current main commit' >&2; exit 1; }
tag_sha="$(gh api "repos/$GITHUB_REPOSITORY/commits/$RELEASE_TAG" --jq '.sha')"
[[ "$tag_sha" == "$GITHUB_SHA" ]] || { echo 'Remote tag no longer identifies the verified commit' >&2; exit 1; }
verified_run="$(gh run list --repo "$GITHUB_REPOSITORY" --workflow study-pipeline.yml \
  --branch main --event push --commit "$GITHUB_SHA" --status success --limit 20 --json databaseId \
  --jq '.[0].databaseId // empty')"
[[ "$verified_run" =~ ^[0-9]+$ ]] || { echo 'Successful push CI for this commit is required' >&2; exit 1; }
existing_id="$(gh api --paginate "repos/$GITHUB_REPOSITORY/releases?per_page=100" \
  --jq ".[] | select(.tag_name == \"$RELEASE_TAG\") | .id")"
if [[ -n "$existing_id" ]]; then
  [[ "$existing_id" =~ ^[0-9]+$ ]] || { echo 'Invalid existing release identity' >&2; exit 1; }
  existing_json="$(gh api "repos/$GITHUB_REPOSITORY/releases/$existing_id")"
  EXISTING_RELEASE_JSON="$existing_json" python3 - "$notes" <<'PY'
import json, os, pathlib, sys
release = json.loads(os.environ['EXISTING_RELEASE_JSON'])
expected = pathlib.Path(sys.argv[1]).read_text().replace('\r\n', '\n').strip()
valid = (release.get('tag_name') == os.environ['RELEASE_TAG']
         and release.get('name') == 'PipelineFortress ' + os.environ['RELEASE_TAG']
         and release.get('body', '').replace('\r\n', '\n').strip() == expected
         and release.get('draft') is False and release.get('prerelease') is False)
if not valid:
    raise SystemExit('Existing release differs from the reviewed publication; preserve it and stop')
PY
  echo "Verified existing $RELEASE_TAG after study run $verified_run"
  exit 0
fi
gh release create "$RELEASE_TAG" --repo "$GITHUB_REPOSITORY" --verify-tag \
  --target "$GITHUB_SHA" --title "PipelineFortress $RELEASE_TAG" --notes-file "$notes"
echo "Published $RELEASE_TAG after verified study run $verified_run"
