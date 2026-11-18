#!/usr/bin/env bash
set -eu
task_case_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cp "$task_case_dir/fixtures/rows.json" rows.json
