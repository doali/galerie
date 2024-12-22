function usage {
	echo "$(basename ${0}) <--cat mot-clef> <fichier> <chemin_images>"
}

[ "${1}" == '--help' ] || [ ${#} == 0 ] || [ ${#} -lt 2 ] && usage && exit 0

if [ "${1}" != '--cat' ]; then
	mot_clef=_
else
	mot_clef=${2}
	shift
	shift
fi

fichier=${1}
shift
chemin=${@}

[ -f ${fichier} ] || touch ${fichier}

for ch in "${chemin}"; do
	echo "${mot_clef}:${ch}" >>${fichier}
done
