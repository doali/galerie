# ==============================================================================
# Etant donne un fichier situe a chemin_fichier
# et contenant des lignes de la forme 

# mot_clef_1:chemin/vers/une/image_1
# mot_clef_2:chemin/vers/une/image_1
# mot_clef_2:chemin/vers/une/image_2
#
# renvoie un resultat de la forme
# chemin/vers/une/image_1
# chemin/vers/une/image_2
# ------------------------------------------------------------------------------
# Permet de renvoyer les chemins sans doublons des images (a telecharger....)
# ==============================================================================
[ $# -ne 1 ] && echo "Usage: $(basename $0) <chemin_fichiers>" && exit 0

chemin_fichier=$1

sort ${chemin_fichier} -t: -k 2 | cut -d: -f2- | uniq
