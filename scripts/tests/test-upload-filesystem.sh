#!/usr/bin/env bash
set -euo pipefail

scripts_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
project_root="$(dirname "$scripts_dir")"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
mkdir "$tmp_dir/bin"

cat > "$tmp_dir/bin/pio" <<'MOCK'
#!/usr/bin/env bash
printf '%s\n' "$PWD" "$@" > "$PIO_TEST_OUTPUT"
exit "${PIO_TEST_EXIT_CODE:-0}"
MOCK
chmod +x "$tmp_dir/bin/pio"

export PATH="$tmp_dir/bin:$PATH"
export PIO_TEST_OUTPUT="$tmp_dir/output"
cd "$tmp_dir"
bash "$scripts_dir/upload-filesystem.sh"

mapfile -t actual < "$PIO_TEST_OUTPUT"
if [[ "${actual[0]}" != "$project_root" ]]; then
  printf 'Expected project root %s, got %s\n' "$project_root" "${actual[0]}" >&2
  exit 1
fi
if [[ "${actual[*]:1}" != "run -t uploadfs" ]]; then
  printf 'Unexpected pio arguments: %s\n' "${actual[*]:1}" >&2
  exit 1
fi

export PIO_TEST_EXIT_CODE=17
if bash "$scripts_dir/upload-filesystem.sh"; then
  echo "Expected the wrapper to propagate pio's exit code 17" >&2
  exit 1
else
  actual_exit_code=$?
fi
if [[ "$actual_exit_code" -ne 17 ]]; then
  printf 'Expected exit code 17, got %s\n' "$actual_exit_code" >&2
  exit 1
fi

printf 'Linux uploader wrapper tests passed\n'
