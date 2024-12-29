#!/usr/bin/env bash

function usage {
	echo "$(basename ${0}) <mot-clef> <fichiers>"
}

[ "${1}" == '--help' ] || [ ${#} -le 1 ] && usage && exit 0

mot_clef=${1}
shift
fichiers=${@}

for fichier in ${fichiers}; do
    # Utilisation de IFS pour éviter la séparation des chemins contenant des espaces
    while IFS= read -r ch; do
        libelle=$(echo "${ch}" | cut -d: -f1)
        chemin=$(echo "${ch}" | cut -d: -f2-)

        if [[ "${mot_clef}" =~ "${libelle}" ]]; then
            echo "${chemin}" | cut -d: -f 2-
        fi
    done < "${fichier}"
done
