#!/usr/bin/env bash
set -Eeuo pipefail

# usage: file_env VAR [DEFAULT]
#    ie: file_env 'XYZ_DB_PASSWORD' 'example'
# (will allow for "$XYZ_DB_PASSWORD_FILE" to fill in the value of
# "$XYZ_DB_PASSWORD" from a file, especially for Docker's secrets
# feature)
file_env() {
    local var="$1"
    local fileVar="${var}_FILE"
    local def="${2:-}"
    if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
	printf >&2 'error: both %s and %s are set (but are exclusive)\n' "$var" "$fileVar"
	exit 1
    fi
    local val="$def"
    if [ "${!var:-}" ]; then
	val="${!var}"
    elif [ "${!fileVar:-}" ]; then
	val="$(< "${!fileVar}")"
    fi
    export "$var"="$val"
    unset "$fileVar"
}

function docker_setup_env() {
    file_env 'LETHBRIDGE_DB_URI'
    lethbridge -d configure database uri "${LETHBRIDGE_DB_URI}"
    lethbridge -d database upgrade head
}

# is this file is being run or sourced from another script
_is_sourced() {
    # https://unix.stackexchange.com/a/215279
    [ "${#FUNCNAME[@]}" -ge 2 ] \
	&& [ "${FUNCNAME[0]}" = '_is_sourced' ] \
	&& [ "${FUNCNAME[1]}" = 'source' ]
}

function _main() {
    # if the first arg looks like a flag or a subcommand, assume it's
    # for Lethbridge
    COMPREPLY=(
        $(env COMP_WORDS=lethbridge COMP_CWORD=1 \
              _LETHBRIDGE_COMPLETE=complete_bash lethbridge)
    )
    if ([ "${1:0:1}" = '-' ] || echo "${COMPREPLY[@]}" | fgrep -w "$1" > /dev/null); then
        set -- lethbridge "$@"
    fi

    if [ "$1" = 'lethbridge' ]; then
        docker_setup_env
	exec "$@"
    fi

    exec "$@"
}

if ! _is_sourced; then
	_main "$@"
fi
