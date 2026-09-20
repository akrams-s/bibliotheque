# controller.py
from tkinter import messagebox
from model import BibliothequeModel


class BibliothequeController:
    def __init__(self, vue):
        self.vue = vue
        self.modele = BibliothequeModel()
        self.livre_selectionne_id = None

        self.vue.btn_ajouter.configure(command=self.ajouter)
        self.vue.btn_rechercher.configure(command=self.rechercher)
        self.vue.btn_modifier.configure(command=self.modifier)
        self.vue.btn_supprimer.configure(command=self.supprimer)
        self.vue.btn_afficher.configure(command=self.afficher_tous)
        self.vue.btn_annuler.configure(command=self.annuler)
        #some shortcuts for the buttons: Esc for annuler, Enter for ajouter, Backspace for supprimer
        self.vue.tree.bind("<<TreeviewSelect>>", self.selectionner)
        self.vue.bind("<Escape>", lambda e: self.annuler())
        self.vue.bind("<Return>", lambda e: self.ajouter())
        self.vue.tree.bind("<BackSpace>", lambda e: self.supprimer())  # Only when tree has focus

        self.afficher_tous()

    def valider(self, data):
        erreur = False

        for champ, valeur in data.items():
            entry = self.vue.entrees[champ]

            if valeur.strip() == "":
                entry.configure(border_color="red")
                erreur = True
            else:
                entry.configure(border_color="gray")

        if erreur:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return False

        if not data["annee"].isdigit():
            messagebox.showerror("Erreur", "L'année doit être numérique.")
            return False

        return True


    def ajouter(self):
        data = self.vue.get_inputs()
        if self.valider(data):
            self.modele.ajouter_livre(
                data["titre"], data["auteur"],
                int(data["annee"]), data["genre"]
            )
            self.annuler()
            self.afficher_tous()

    def rechercher(self):
        # Récupérer tous les critères de recherche
        titre = self.vue.entrees["titre"].get().strip()
        auteur = self.vue.entrees["auteur"].get().strip()
        annee = self.vue.entrees["annee"].get().strip()
        genre = self.vue.entrees["genre"].get().strip()
        
        # Rechercher avec tous les critères
        self.vue.afficher_livres(self.modele.rechercher_livre_avancee(titre, auteur, annee, genre))

    def modifier(self):
        if self.livre_selectionne_id is None:
            messagebox.showwarning("Attention", "Sélectionnez un livre")
            return
        data = self.vue.get_inputs()
        if self.valider(data):
            self.modele.modifier_livre(
                self.livre_selectionne_id,
                data["titre"], data["auteur"],
                int(data["annee"]), data["genre"]
            )
            self.annuler()
            self.afficher_tous()

    def supprimer(self):
        if self.livre_selectionne_id is None:
            messagebox.showwarning("Attention", "Sélectionnez un livre")
            return
        if self.livre_selectionne_id and messagebox.askyesno("Confirmation", "Supprimer ce livre ?"):
            self.modele.supprimer_livre(self.livre_selectionne_id)
            self.annuler()
            self.afficher_tous()

    def afficher_tous(self):
        self.vue.afficher_livres(self.modele.afficher_tous())
        count = len(self.modele.afficher_tous()) #status bar counter
        self.vue.status_label.configure(text=f"📊 {count} livres enregistrés") 


    def selectionner(self, event):
        sel = self.vue.tree.selection()
        if sel:
            livre = self.vue.tree.item(sel[0])["values"]
            self.livre_selectionne_id = livre[0]
            self.vue.set_inputs(livre)

    def annuler(self):
        self.vue.tree.selection_remove(self.vue.tree.selection())
        self.livre_selectionne_id = None
        self.vue.clear_form()
        # self.afficher_tous()  # Réafficher tous les livres après annulation