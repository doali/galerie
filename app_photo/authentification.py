# authentification.py

from flask import session
import sqlite3
from functools import wraps

def create_users_table():
    """
    Crée la table des utilisateurs dans la base de données si elle n'existe pas déjà.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'  -- Les rôles peuvent être 'admin' ou 'user'
        )
    ''')
    conn.commit()
    conn.close()

def validate_user(username, password):
    """
    Valide les informations de connexion de l'utilisateur.
    Retourne le rôle de l'utilisateur s'il est valide, sinon None.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT role FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cursor.fetchone()
        if user:
            return user[0]  # Retourne le rôle ('admin' ou 'user')
        return None
    finally:
        conn.close()

def admin_required(f):
    """
    Décorateur pour restreindre l'accès aux administrateurs uniquement.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "role" not in session or session["role"] != "admin":
            return "Accès refusé : vous n'êtes pas administrateur", 403
        return f(*args, **kwargs)
    return decorated_function
