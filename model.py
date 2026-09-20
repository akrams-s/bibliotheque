# model.py
# ============================================
# Modèle : gestion de la base de données SQLite
# ============================================

import sqlite3


class BibliothequeModel:
    def __init__(self, db_name="bibliotheque.db"):
        self.db_name = db_name
        self.creer_table()

    def connecter(self):
        return sqlite3.connect(self.db_name)

    def creer_table(self):
        conn = self.connecter()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                annee INTEGER NOT NULL,
                genre TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def ajouter_livre(self, titre, auteur, annee, genre):
        conn = self.connecter()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO livres (titre, auteur, annee, genre) VALUES (?, ?, ?, ?)",
            (titre, auteur, annee, genre)
        )
        conn.commit()
        conn.close()

    def rechercher_livre(self, critere):
        conn = self.connecter()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM livres
            WHERE titre LIKE ? 
               OR auteur LIKE ? 
               OR CAST(annee AS TEXT) LIKE ? 
               OR genre LIKE ?
        """, (f"%{critere}%", f"%{critere}%", f"%{critere}%", f"%{critere}%"))
        res = cur.fetchall()
        conn.close()
        return res
    
    def rechercher_livre_avancee(self, titre, auteur, annee, genre):
        """Recherche avec plusieurs critères combinés"""
        conn = self.connecter()
        cur = conn.cursor()
        
        # Construire la requête dynamiquement
        conditions = []
        params = []
        
        if titre:
            conditions.append("titre LIKE ?")
            params.append(f"%{titre}%")
        if auteur:
            conditions.append("auteur LIKE ?")
            params.append(f"%{auteur}%")
        if annee:
            conditions.append("CAST(annee AS TEXT) LIKE ?")
            params.append(f"%{annee}%")
        if genre:
            conditions.append("genre LIKE ?")
            params.append(f"%{genre}%")
        
        # Si aucun critère, retourner tous les livres
        if not conditions:
            cur.execute("SELECT * FROM livres")
        else:
            query = "SELECT * FROM livres WHERE " + " AND ".join(conditions)
            cur.execute(query, params)
        
        res = cur.fetchall()
        conn.close()
        return res

    def modifier_livre(self, livre_id, titre, auteur, annee, genre):
        conn = self.connecter()
        cur = conn.cursor()
        cur.execute("""
            UPDATE livres
            SET titre=?, auteur=?, annee=?, genre=?
            WHERE id=?
        """, (titre, auteur, annee, genre, livre_id))
        conn.commit()
        conn.close()

    def supprimer_livre(self, livre_id):
        conn = self.connecter()
        cur = conn.cursor()
        cur.execute("DELETE FROM livres WHERE id=?", (livre_id,))
        conn.commit()
        conn.close()

    def afficher_tous(self):
        conn = self.connecter()
        cur = conn.cursor()
        cur.execute("SELECT * FROM livres")
        res = cur.fetchall()
        conn.close()
        return res
