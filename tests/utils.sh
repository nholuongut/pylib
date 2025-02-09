#!/usr/bin/env bash
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Nho Luong
#  Date: 2015-05-25 01:38:24 +0100 (Mon, 25 May 2015)
#
#  https://github.com/nholuongut/pylib
#
#  License: see accompanying Nho Luong LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn and optionally send me feedback to help improve or steer this or other code I publish
#
#  https://www.linkedin.com/in/nholuong
#

set -euo pipefail
srcdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

hr(){
    echo "===================="
}

if [ -n "${TRAVIS:-}" ]; then
    sudo=sudo
else
    sudo=""
fi
export sudo

#export SPARK_HOME="$(ls -d tests/spark-*-bin-hadoop* | head -n 1)"

# shellcheck disable=SC1090
. "$srcdir/excluded.sh"

check(){
    cmd="$1"
    msg="$2"
    if eval "$cmd"; then
        echo "SUCCESS: $msg"
    else
        echo "FAILED: $msg"
        exit 1
    fi
}

# shellcheck disable=SC1090
. "$srcdir/../bash-tools/lib/utils.sh"
