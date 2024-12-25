from flask import Flask, request, render_template
import re

app = Flask(__name__)

def load_image_paths(file_path):
    """
    Charge les chemins d'images depuis un fichier.
    """
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        return []

# def search_images(query, image_paths):
#     """
#     Recherche des images correspondant à une date ou une sous-chaîne.
#     """
#     query = query.lower()  # Convertir la requête en minuscules pour une recherche insensible à la casse
#     return [path for path in image_paths if query in path.lower()]  # Filtrer les images contenant la sous-chaîne

def search_images(query, image_paths):
    """
    Recherche des images correspondant à un motif basé sur une expression régulière.

    :param query: Expression régulière pour rechercher dans les noms de fichiers.
    :param image_paths: Liste des chemins d'images.
    :return: Liste des chemins d'images correspondant au motif.
    """
    try:
        pattern = re.compile(query, re.IGNORECASE)  # Créer un motif insensible à la casse
        return [path for path in image_paths if pattern.search(path)]  # Filtrer avec le motif
    except re.error as e:
        raise ValueError(f"Expression régulière invalide : {e}")    

@app.route("/", methods=["GET", "POST"])
def home():
    image_paths = load_image_paths("images.txt")  # Charger les chemins des images
    query = ""
    results = []
    page = 1  # Numéro de page par défaut
    per_page = 20  # Nombre d'images par page

    if request.method == "POST":
        query = request.form.get("search")  # Récupérer la saisie utilisateur
        if query:
            results = search_images(query, image_paths)  # Recherche des images

    # Pagination
    try:
        page = int(request.args.get("page", 1))  # Numéro de la page (par défaut : 1)
    except ValueError:
        page = 1

    # Conserver la requête si elle est transmise via GET (navigation)
    if not results and "query" in request.args:
        query = request.args.get("query")
        if query:
            results = search_images(query, image_paths)

    total_results = len(results)
    total_pages = (total_results + per_page - 1) // per_page  # Calcul du nombre total de pages
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]

    return render_template(
        "index.html",
        query=query,
        results=paginated_results,
        page=page,
        total_pages=total_pages,
        total_results=total_results,
        per_page=per_page
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
