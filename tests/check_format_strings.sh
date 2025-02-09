#!/usr/bin/env bash
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Nho Luong
#  Date: 2017-06-29 15:48:48 +0200 (Thu, 29 Jun 2017)
#
#  https://github.com/nholuongut/pylib
#
#  License: see accompanying Nho Luong LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn and optionally send me feedback to help improve or steer this or other code I publish
#
#  https://www.linkedin.com/in/nholuong
#

set -u
srcdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$srcdir/.." || exit 1;

# shellcheck disable=SC1091
. tests/utils.sh

section "Checking Python format strings"

start_time="$(start_timer)"

set +e
for x in "${@:-$(find . -iname '*.py' -o -iname '*.jy')}"; do
    isExcluded "$x" && continue
    output="$(grep -E ' log\.(info|warn|error|debug|notice)' "$x" | grep -v "['\"]")"
    if [ -n "$output" ]; then
        echo "$x contains potentially unsafe string interpolation behaviour:"
        echo "$output"
        echo
    fi
done

time_taken "$start_time"
section2 "Finished checking python format strings"

exit 0
