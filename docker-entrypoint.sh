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

# check whether the argument is a Lethbridge command
COMPREPLY=(
    $(env COMP_WORDS=lethbridge COMP_CWORD=1 \
          _LETHBRIDGE_COMPLETE=complete_bash lethbridge)
)
_is_command() {
    case "${COMPREPLY[@]}" in
        *"$1"*)
            return 0
            ;;
    esac
    return 1
}

docker_setup_env() {
    file_env 'LETHBRIDGE_DB_URI' sqlite:///galaxy.sqlite

    # use the same global options as the container command
    local arg
    local args=()
    for arg; do
        if [ "$arg" = 'lethbridge' ]; then
            :
        elif _is_command "$arg"; then
            break
        else
            args+=("$arg")
        fi
    done

    lethbridge "${args[@]}" configure set database uri "${LETHBRIDGE_DB_URI}"
    lethbridge "${args[@]}" database upgrade head
}

# is this file is being run or sourced from another script
_is_sourced() {
    # https://unix.stackexchange.com/a/215279
    [ "${#FUNCNAME[@]}" -ge 2 ] \
	&& [ "${FUNCNAME[0]}" = '_is_sourced' ] \
	&& [ "${FUNCNAME[1]}" = 'source' ]
}

# check arguments for an option that would cause Lethbridge to stop
_want_help() {
    local arg
    for arg; do
        case "$arg" in
            --help|-v|--version)
                return 0
                ;;
        esac
    done
    return 1
}

_main() {
    # if the first arg looks like a Lethbridge flag or command, assume
    # it's for Lethbridge
    if [ "${1:0:1}" = '-' ] || _is_command $1; then
        set -- lethbridge "$@"
    fi

    if [ "$1" = 'lethbridge' ] && ! _want_help "$@"; then
        docker_setup_env "$@"
	exec "$@"
    fi

    exec "$@"
}

if ! _is_sourced; then
	_main "$@"
fi
