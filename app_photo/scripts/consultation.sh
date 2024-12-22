#!/usr/bin/env bash

function usage {
	echo "$(basename ${0}) <mot-clef> <fichiers>"
}

[ "${1}" == '--help' ] || [ ${#} == 0 ] && usage && exit 0

mot_clef=${1}
shift
fichiers=${@}

for fichier in ${fichiers}; do
	for ch in $(cat ${fichier}); do
		libelle=$(echo ${ch} | cut -d: -f1)
		chemin=$(echo ${ch} | cut -d: -f2-)

		if [[ "${mot_clef}" =~ "${libelle}" ]]; then
			echo "${ch}" | cut -d: -f 2-
		fi
	done
done
