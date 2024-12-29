# app.py

from flask import Flask, request, render_template, redirect, url_for, session, flash
from authentification import validate_user, create_users_table, admin_required  # Importer les fonctions nécessaires
import sqlite3
import re

app = Flask(__name__)
app.secret_key = "votre_cle_secrete"  # Clé secrète pour gérer les sessions

# Crée la table des utilisateurs au démarrage
create_users_table()

def load_image_paths(file_path):
    """
    Charge les chemins d'images depuis un fichier.
    """
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        return []

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

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Route pour la page de connexion des utilisateurs.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Vérification des identifiants via la fonction de authentification
        role = validate_user(username, password)

        if role:
            session["username"] = username
            session["role"] = role
            flash("Connexion réussie", "success")
            return redirect(url_for("home"))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """
    Route pour déconnexion.
    """
    session.pop("username", None)
    session.pop("role", None)
    flash("Vous avez été déconnecté", "info")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Route pour l'inscription des utilisateurs.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role", "user")  # Par défaut, le rôle est "user"

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role),
            )
            conn.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Ce nom d'utilisateur existe déjà.", "error")
        finally:
            conn.close()

    return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
def home():
    """
    Route principale pour la galerie.
    """
    if "username" not in session:
        flash("Veuillez vous connecter pour accéder à la galerie", "warning")
        return redirect(url_for("login"))

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
        per_page=per_page,
    )

@app.route("/admin")
@admin_required
def admin_dashboard():
    """
    Tableau de bord pour les administrateurs.
    """
    return "Bienvenue dans le tableau de bord administrateur"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
