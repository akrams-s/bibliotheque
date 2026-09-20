# view.py
# =====================================================
# Vue : Interface graphique CustomTkinter
# =====================================================

import customtkinter as ctk
from tkinter import ttk


class BibliothequeView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("📚 Bibliothèque personnelle")
        self.geometry("1100x700")
        self.minsize(1000, 650)

        # Default theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Status bar
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(side="bottom", pady=5)


        # ================= Header =================
        header = ctk.CTkFrame(self, height=80)
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="📚 Bibliothèque personnelle",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(side="left", padx=25, pady=20)

        self.switch_theme = ctk.CTkSwitch(
            header,
            text="🌙 Dark mode",
            command=self.toggle_theme
        )
        self.switch_theme.pack(side="right", padx=25)

        # ================= Main =================
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # ================= Form =================
        form_card = ctk.CTkFrame(main, corner_radius=18)
        form_card.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            form_card,
            text="📝 Informations du livre",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=20, pady=15)

        form = ctk.CTkFrame(form_card, fg_color="transparent")
        form.pack(padx=20, pady=10)

        self.entrees = {}
        champs = ["Titre", "Auteur", "Annee", "Genre"]

        for i, champ in enumerate(champs):
            ctk.CTkLabel(form, text=champ).grid(row=i, column=0, sticky="w", pady=8)
            entry = ctk.CTkEntry(form, width=300)
            entry.grid(row=i, column=1, padx=(10, 0), pady=8)
            self.entrees[champ.lower()] = entry

        # ================= Buttons =================
        actions = ctk.CTkFrame(main, corner_radius=18)
        actions.pack(fill="x", pady=(0, 20))

        button_container = ctk.CTkFrame(actions, fg_color="transparent")
        button_container.pack(expand=True)


        self.btn_ajouter = ctk.CTkButton(actions, text="➕ Ajouter")
        self.btn_rechercher = ctk.CTkButton(actions, text="🔍 Rechercher")
        self.btn_modifier = ctk.CTkButton(actions, text="✏️ Modifier")
        self.btn_supprimer = ctk.CTkButton(actions, text="🗑 Supprimer")
        self.btn_afficher = ctk.CTkButton(actions, text="📋 Afficher tout")
        self.btn_annuler = ctk.CTkButton(actions, text="↩ Annuler")
        self.btn_quitter = ctk.CTkButton(actions, text="❌ Quitter", fg_color="red", command=self.destroy)

        for btn in [
            self.btn_ajouter, self.btn_rechercher, self.btn_modifier,
            self.btn_supprimer, self.btn_afficher, self.btn_annuler, self.btn_quitter
        ]:
            btn.pack(in_=button_container, side="left", padx=10, pady=15)


        # ================= Table =================
        table_card = ctk.CTkFrame(main, corner_radius=18)
        table_card.pack(fill="both", expand=True)

        ctk.CTkLabel(
            table_card,
            text="📖 Collection de livres",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=20, pady=15)

        columns = ("id", "titre", "auteur", "annee", "genre")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings")
        # style = ttk.Style()
        # style.map("Treeview",
        #         background=[("selected", "#3A8DFF")])


        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")
            self.tree.column("id", width=60)
            self.tree.column("titre", width=250)
            self.tree.column("auteur", width=200)
            self.tree.column("annee", width=100)
            self.tree.column("genre", width=150)


        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)

    # ================= Utils =================
    def toggle_theme(self):
        mode = "dark" if self.switch_theme.get() else "light"
        ctk.set_appearance_mode(mode)

    def get_inputs(self):
        return {k: v.get() for k, v in self.entrees.items()}

    def set_inputs(self, livre):
        _, titre, auteur, annee, genre = livre
        self.entrees["titre"].delete(0, "end")
        self.entrees["auteur"].delete(0, "end")
        self.entrees["annee"].delete(0, "end")
        self.entrees["genre"].delete(0, "end")

        self.entrees["titre"].insert(0, titre)
        self.entrees["auteur"].insert(0, auteur)
        self.entrees["annee"].insert(0, annee)
        self.entrees["genre"].insert(0, genre)

    def clear_form(self):
        for e in self.entrees.values():
            e.delete(0, "end")
            e.configure(border_color="gray")  # Réinitialiser la couleur des bordures

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def afficher_livres(self, livres):
        self.clear_table()
        for livre in livres:
            self.tree.insert("", "end", values=livre)