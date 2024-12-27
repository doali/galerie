# ==============================================================================
# Generation du fichier images.txt
# - contenant tous les chemins des images trouvees
# => a lancer au niveau de galerie/app_photo
# ==============================================================================
#find static/images/* -iname "*.jpeg" -o -iname "*.jpg" -o -iname "*.png" -o -iname "*.mp4" | grep -vi system >images.txt
find static/images/* -iname "*.jpeg" -o -iname "*.jpg" -o -iname "*.png" | grep -vi system >images.txt
