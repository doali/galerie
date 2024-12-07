from flask import Flask, request, render_template

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

def search_image_by_date(year, month, day, image_paths):
    """
    Recherche une image par date (année, mois, jour) dans les chemins d'images.
    """
    date_str = ""
    
    # Créer la chaîne de recherche basée sur les parties disponibles
    if year:
        date_str += year
    if month:
        date_str += f"{month:02d}"
    if day:
        date_str += f"{day:02d}"
    
    # Rechercher les images correspondant à la date
    return [path for path in image_paths if date_str in path]

@app.route("/", methods=["GET", "POST"])
def home():
    image_paths = load_image_paths("images.txt")  # Charger les chemins des images
    query = ""
    results = []

    if request.method == "POST":
        query = request.form.get("search")  # Récupérer la saisie utilisateur
        if query:
            try:
                # Initialisation des variables year, month, day à None
                year, month, day = None, None, None

                # Diviser la requête en parties (année, mois, jour)
                parts = query.split()

                if len(parts) == 1:
                    # Si l'utilisateur a saisi une seule partie (année)
                    year = parts[0]
                elif len(parts) == 2:
                    # Si l'utilisateur a saisi année et mois
                    year, month = parts
                elif len(parts) == 3:
                    # Si l'utilisateur a saisi année, mois et jour
                    year, month, day = parts
                else:
                    results = ["Format incorrect. Saisir une année, mois ou jour sous la forme : AAAA, AAAA MM, ou AAAA MM JJ"]
                    return render_template("index.html", query=query, results=results)

                # Recherche les images correspondant à la date
                results = search_image_by_date(year, month, day, image_paths)
            except ValueError:
                results = ["Format incorrect. Saisir une année, mois ou jour sous la forme : AAAA, AAAA MM, ou AAAA MM JJ"]

    return render_template("index.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
