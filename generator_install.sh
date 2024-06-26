#!/bin/sh

install_package() (
	pkgName="$1"
	echo "Try to install --${pkgName}--"
	case $(uname) in
		(Linux*)
			if which pacman >/dev/null 2>&1; then
				yes | sudo -p 'Pass required for pacman install: ' \
					pacman -S "$pkgName"
			elif which apt-get >/dev/null 2>&1; then
				sudo -p 'Pass required for apt-get install: ' \
					DEBIAN_FRONTEND=noninteractive apt-get -y install "$pkgName"
			fi
			;;
		(Darwin*)
			yes | brew install "$pkgName"
			;;
		(*)
			;;
	esac
)

get_pkg_mgr() {
	define_consts >&2
	case $(uname) in
		(Linux*)
			if  which pacman >/dev/null 2>&1; then
				echo 'pacman'
				return 0
			elif which apt-get >/dev/null 2>&1; then
				echo 'apt-get'
				return 0
			fi
			;;
		(Darwin*)
			echo 'homebrew'
			return 0
			;;
		(*)
			;;
	esac
	return 1
}

pkgMgrChoice=$(get_pkg_mgr)

[ -n "$pkgMgrChoice" ] || show_err_and_exit "No package manager set"

if rbenv -v >/dev/null; then
	install_package rbenv
fi


case $(uname) in
	(Linux*)
		if [ "$pkgMgrChoice" = 'apt-get' ]; then
			if ! dpkg -s autoconf 2>/dev/null; then
				install_package autoconf
			fi
			if ! dpkg -s patch 2>/dev/null; then
				install_package patch
			fi
			if ! dpkg -s build-essential 2>/dev/null; then
				install_package build-essential
			fi
			if ! dpkg -s rustc 2>/dev/null; then
				install_package rustc
			fi
			if ! dpkg -s libssl-dev 2>/dev/null; then
				install_package libssl-dev
			fi
			if ! dpkg -s libyaml-dev 2>/dev/null; then
				install_package libyaml-dev
			fi
			if ! dpkg -s libreadline6-dev 2>/dev/null; then
				install_package libreadline6-dev
			fi
			if ! dpkg -s zlib1g-dev 2>/dev/null; then
				install_package zlib1g-dev
			fi
			if ! dpkg -s libgmp-dev 2>/dev/null; then
				install_package libgmp-dev
			fi
			if ! dpkg -s libncurses5-dev 2>/dev/null; then
				install_package libncurses5-dev
			fi
			if ! dpkg -s libffi-dev 2>/dev/null; then
				install_package libffi-dev
			fi
			if ! dpkg -s libgdbm6 2>/dev/null; then
				install_package libgdbm6
			fi
			if ! dpkg -s libgdbm-dev 2>/dev/null; then
				install_package libgdbm-dev
			fi
			if ! dpkg -s libdb-dev 2>/dev/null; then
				install_package libdb-dev
			fi
			if ! dpkg -s uuid-dev 2>/dev/null; then
				install_package uuid-dev
			fi
		fi
		;;
	(*) ;;
esac



if ruby -v 2>/dev/null; then;
	rbenv install 3.1.2
fi



