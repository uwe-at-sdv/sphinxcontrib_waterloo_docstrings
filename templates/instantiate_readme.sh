#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd "$(dirname "$0")" && pwd)
repo_dir=$(cd "${script_dir}/.." && pwd)
target=${1:-GITHUB}
version=$(tr -d '[:space:]' < "${repo_dir}/VERSION")

case "${target}" in
	GITHUB)
		readme_template="${script_dir}/README_GITHUB.template.md"
		logo_template="${script_dir}/README_LOGO_GITHUB.template.md"
		target_badges_template="${script_dir}/README_BADGES_GITHUB.template.md"
		;;
	PYPI)
		readme_template="${script_dir}/README_PYPI.template.md"
		logo_template="${script_dir}/README_LOGO_PYPI.template.md"
		target_badges_template="${script_dir}/README_BADGES_PYPI.template.md"
		;;
	*)
		echo "Usage: $0 [GITHUB|PYPI]" >&2
		exit 2
		;;
esac

logo=$(cat "${logo_template}")
common_badges=$(cat "${script_dir}/README_BADGES_COMMON.template.md")
target_badges=$(cat "${target_badges_template}")
badges=$(printf '%s\n%s\n' "${common_badges}" "${target_badges}")
common=$(cat "${script_dir}/README_COMMON.template.md")

python3 - "$readme_template" "$repo_dir/README.md" "$version" "$logo" "$badges" "$common" <<'PY'
from pathlib import Path
import sys

template_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
version = sys.argv[3]
logo = sys.argv[4]
badges = sys.argv[5]
common = sys.argv[6]

text = template_path.read_text()
text = text.replace("_VERSION_", version)
text = text.replace("_README_LOGO_", logo)
text = text.replace("_BADGES_", badges.replace("_VERSION_", version))
text = text.replace("_README_COMMON_", common)
out_path.write_text(text)
PY
