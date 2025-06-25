import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from exceptions import LivreInexistantError, MembreInexistantError
from bibliotheque import Livre, Membre

class BibliothequeGUI(tk.Tk):
    def __init__(self, biblio):
        super().__init__()
        self.title(" GESTION BIBLIOTHÈQUE MERIEM ")
        self.geometry("1200x800")
        self.configure(bg="#e5f0f9")
        lbl_titre = tk.Label(
            self,
            text="📚 GESTION BIBLIOTHÈQUE MERIEM 📚",
            font=("Helvetica", 28, "bold"),
            fg="#FFFFFF",
            bg="#1d5492"
    )
        lbl_titre.pack(pady=20)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 14, "bold"), background="#0f659f", foreground="white", padding=10)
        style.map("TButton", background=[("active", "#1f5c83")])
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="#d0e0f0")
        style.configure("Treeview", font=("Helvetica", 13))
        style.configure("TLabel", font=("Helvetica", 14))
        style.configure("TEntry", font=("Helvetica", 13))

        self.biblio = biblio

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill='both')

        self.tab_livres = ttk.Frame(self.notebook)
        self.tab_membres = ttk.Frame(self.notebook)
        self.tab_emprunts = ttk.Frame(self.notebook)
        self.tab_stats = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_livres, text="📚 Livres")
        self.notebook.add(self.tab_membres, text="👤 Membres")
        self.notebook.add(self.tab_emprunts, text="🔁 Emprunts")
        self.notebook.add(self.tab_stats, text="📊 Statistiques")

        self.construire_onglet_livres()
        self.construire_onglet_membres()
        self.construire_onglet_emprunts()
        self.construire_onglet_stats()

    # --- Onglet Livres ---
    def construire_onglet_livres(self):
        colonnes = ("ISBN", "Titre", "Auteur", "Année", "Genre", "Statut")
        self.tree_livres = ttk.Treeview(self.tab_livres, columns=colonnes, show='headings', height=15)
        for col in colonnes:
            self.tree_livres.heading(col, text=col)
            self.tree_livres.column(col, width=160, anchor='center')
        self.tree_livres.pack(expand=1, fill='both')

        frm_btns = ttk.Frame(self.tab_livres)
        frm_btns.pack(pady=8)
        btn_refresh = ttk.Button(frm_btns, text="Actualiser", command=self.afficher_livres)
        btn_refresh.grid(row=0, column=0, padx=10)
        btn_supprimer = ttk.Button(frm_btns, text="🗑️ Supprimer Livre", command=self.supprimer_livre)
        btn_supprimer.grid(row=0, column=1, padx=10)

        self.afficher_livres()

        frm_ajout = ttk.Frame(self.tab_livres)
        frm_ajout.pack(pady=15, fill='x')

        labels = ["ISBN", "Titre", "Auteur", "Année", "Genre"]
        self.entries_livre = {}
        for i, label in enumerate(labels):
            ttk.Label(frm_ajout, text=label).grid(row=0, column=i, padx=5, sticky='w')
            entry = ttk.Entry(frm_ajout, width=20)
            entry.grid(row=1, column=i, padx=5)
            self.entries_livre[label.lower()] = entry

        btn_ajouter = ttk.Button(frm_ajout, text="➕ Ajouter Livre", command=self.ajouter_livre)
        btn_ajouter.grid(row=1, column=len(labels), padx=15)

    def ajouter_livre(self):
        isbn = self.entries_livre["isbn"].get().strip()
        titre = self.entries_livre["titre"].get().strip()
        auteur = self.entries_livre["auteur"].get().strip()
        annee = self.entries_livre["année"].get().strip()
        genre = self.entries_livre["genre"].get().strip()

        if not (isbn and titre and auteur and annee and genre):
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return
        try:
            self.biblio.chercher_livre(isbn)
            messagebox.showerror("Erreur", f"Le livre avec ISBN {isbn} existe déjà.")
            return
        except LivreInexistantError:
            pass

        nouveau_livre = Livre(isbn, titre, auteur, annee, genre)
        self.biblio.ajouter_livre(nouveau_livre)
        self.biblio.sauvegarder_livres()
        messagebox.showinfo("Succès", f"Livre '{titre}' ajouté.")
        self.afficher_livres()
        for entry in self.entries_livre.values():
            entry.delete(0, tk.END)

    def supprimer_livre(self):
        selected = self.tree_livres.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner un livre à supprimer.")
            return
        item = self.tree_livres.item(selected[0])
        isbn = item['values'][0]
        confirm = messagebox.askyesno("Confirmation", f"Supprimer le livre ISBN {isbn} ?")
        if confirm:
            try:
                self.biblio.supprimer_livre(isbn)
                self.biblio.sauvegarder_livres()
                messagebox.showinfo("Succès", "Livre supprimé.")
                self.afficher_livres()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def afficher_livres(self):
        for i in self.tree_livres.get_children():
            self.tree_livres.delete(i)
        for livre in self.biblio.liste_livres:
            self.tree_livres.insert('', 'end', values=(livre.ISBN, livre.titre, livre.auteur, livre.annee, livre.genre, livre.statut))

    # --- Onglet Membres ---
    def construire_onglet_membres(self):
        colonnes = ("ID", "Nom", "Livres empruntés")
        self.tree_membres = ttk.Treeview(self.tab_membres, columns=colonnes, show='headings', height=15)
        for col in colonnes:
            self.tree_membres.heading(col, text=col)
            self.tree_membres.column(col, width=220, anchor='center')
        self.tree_membres.pack(expand=1, fill='both')

        frm_btns = ttk.Frame(self.tab_membres)
        frm_btns.pack(pady=8)
        btn_refresh = ttk.Button(frm_btns, text="Actualiser", command=self.afficher_membres)
        btn_refresh.grid(row=0, column=0, padx=10)
        btn_supprimer = ttk.Button(frm_btns, text="🗑️ Supprimer Membre", command=self.supprimer_membre)
        btn_supprimer.grid(row=0, column=1, padx=10)

        self.afficher_membres()

        frm_ajout = ttk.Frame(self.tab_membres)
        frm_ajout.pack(pady=15, fill='x')

        ttk.Label(frm_ajout, text="ID").grid(row=0, column=0, padx=5)
        self.entry_id_membre = ttk.Entry(frm_ajout, width=25)
        self.entry_id_membre.grid(row=1, column=0, padx=5)

        ttk.Label(frm_ajout, text="Nom").grid(row=0, column=1, padx=5)
        self.entry_nom_membre = ttk.Entry(frm_ajout, width=25)
        self.entry_nom_membre.grid(row=1, column=1, padx=5)

        btn_ajouter = ttk.Button(frm_ajout, text="➕ Ajouter Membre", command=self.ajouter_membre)
        btn_ajouter.grid(row=1, column=2, padx=15)

    def ajouter_membre(self):
        id_membre = self.entry_id_membre.get().strip()
        nom = self.entry_nom_membre.get().strip()

        if not id_membre or not nom:
            messagebox.showerror("Erreur", "Tous les champs sont requis.")
            return
        try:
            self.biblio.chercher_membre(id_membre)
            messagebox.showerror("Erreur", f"Le membre avec ID {id_membre} existe déjà.")
            return
        except MembreInexistantError:
            pass

        nouveau_membre = Membre(id_membre, nom)
        self.biblio.enregistrer_membre(nouveau_membre)
        self.biblio.sauvegarder_membres()
        messagebox.showinfo("Succès", f"Membre '{nom}' ajouté.")
        self.afficher_membres()

        self.entry_id_membre.delete(0, tk.END)
        self.entry_nom_membre.delete(0, tk.END)

    def supprimer_membre(self):
        selected = self.tree_membres.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner un membre à supprimer.")
            return
        item = self.tree_membres.item(selected[0])
        membre_id = item['values'][0]
        confirm = messagebox.askyesno("Confirmation", f"Supprimer le membre ID {membre_id} ?")
        if confirm:
            try:
                self.biblio.supprimer_membre(membre_id)
                self.biblio.sauvegarder_membres()
                messagebox.showinfo("Succès", "Membre supprimé.")
                self.afficher_membres()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def afficher_membres(self):
        for i in self.tree_membres.get_children():
            self.tree_membres.delete(i)
        for membre in self.biblio.liste_membres:
            emprunts = ", ".join(membre.livres_empruntes) if hasattr(membre, "livres_empruntes") and membre.livres_empruntes else "-"
            self.tree_membres.insert('', 'end', values=(membre.id, membre.nom, emprunts))

    # --- Onglet Emprunts ---
    def construire_onglet_emprunts(self):
        frm = ttk.Frame(self.tab_emprunts)
        frm.pack(pady=20)

        ttk.Label(frm, text="ISBN du livre :").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.entry_isbn = ttk.Entry(frm, width=30)
        self.entry_isbn.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frm, text="ID du membre :").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.entry_id = ttk.Entry(frm, width=30)
        self.entry_id.grid(row=1, column=1, padx=5, pady=5)

        btn_emprunter = ttk.Button(frm, text="Emprunter", command=self.emprunter_livre)
        btn_emprunter.grid(row=2, column=0, pady=15, padx=10)

        btn_rendre = ttk.Button(frm, text="Retourner", command=self.retourner_livre)
        btn_rendre.grid(row=2, column=1, pady=15, padx=10)

    def emprunter_livre(self):
        isbn = self.entry_isbn.get().strip()
        id_membre = self.entry_id.get().strip()
        try:
            self.biblio.emprunter(isbn, id_membre)
            self.biblio.enregistrer_historique(isbn, id_membre, "emprunt")
            self.biblio.sauvegarder_donnees()
            messagebox.showinfo("Succès", f"Livre {isbn} emprunté par membre {id_membre}")
            self.afficher_livres()
            self.afficher_membres()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def retourner_livre(self):
        isbn = self.entry_isbn.get().strip()
        id_membre = self.entry_id.get().strip()
        try:
            self.biblio.retourner(isbn, id_membre)
            self.biblio.enregistrer_historique(isbn, id_membre, "retour")
            self.biblio.sauvegarder_donnees()
            messagebox.showinfo("Succès", f"Livre {isbn} retourné par membre {id_membre}")
            self.afficher_livres()
            self.afficher_membres()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # --- Onglet Statistiques ---
    def construire_onglet_stats(self):
        # Scrollable frame pour stats
        canvas = tk.Canvas(self.tab_stats)
        scrollbar = ttk.Scrollbar(self.tab_stats, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- 1. Statut des livres (barres) ---
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        statuses = [livre.statut for livre in self.biblio.liste_livres]
        counts_status = {stat: statuses.count(stat) for stat in set(statuses)}
        ax1.bar(counts_status.keys(), counts_status.values(), color=['#4e79a7', '#f28e2b', '#e15759'])
        ax1.set_title("Statut des livres", fontsize=16, fontweight='bold')
        ax1.set_ylabel("Nombre", fontsize=14)
        ax1.tick_params(axis='x', labelrotation=0, labelsize=12)
        ax1.tick_params(axis='y', labelsize=12)
        fig1.tight_layout()

        canvas1 = FigureCanvasTkAgg(fig1, master=scrollable_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(pady=15)

        # --- 2. Nombre de livres par genre (barres) ---
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        genres = [livre.genre for livre in self.biblio.liste_livres]
        counts_genre = {genre: genres.count(genre) for genre in set(genres)}
        couleurs = plt.cm.Paired.colors  # palette
        ax2.bar(counts_genre.keys(), counts_genre.values(), color=couleurs[:len(counts_genre)])
        ax2.set_title("Nombre de livres par genre", fontsize=16, fontweight='bold')
        ax2.set_ylabel("Nombre", fontsize=14)
        ax2.tick_params(axis='x', rotation=45, labelsize=12)
        ax2.tick_params(axis='y', labelsize=12)
        fig2.tight_layout()

        canvas2 = FigureCanvasTkAgg(fig2, master=scrollable_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(pady=15)

        # --- 3. Nombre de membres par nombre d'emprunts (barres) ---
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        emprunt_counts = {}
        for membre in self.biblio.liste_membres:
            n = len(membre.livres_empruntes) if hasattr(membre, "livres_empruntes") else 0
            emprunt_counts[n] = emprunt_counts.get(n, 0) + 1
        x = list(emprunt_counts.keys())
        y = list(emprunt_counts.values())
        ax3.bar(x, y, color='#59a14f')
        ax3.set_title("Nombre de membres par nombre d'emprunts", fontsize=16, fontweight='bold')
        ax3.set_xlabel("Nombre d'emprunts", fontsize=14)
        ax3.set_ylabel("Nombre de membres", fontsize=14)
        ax3.tick_params(axis='x', labelsize=12)
        ax3.tick_params(axis='y', labelsize=12)
        fig3.tight_layout()

        canvas3 = FigureCanvasTkAgg(fig3, master=scrollable_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(pady=15)

        # --- 4. Répartition des genres (camembert) ---
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        if counts_genre:
            ax4.pie(
                counts_genre.values(),
                labels=counts_genre.keys(),
                autopct='%1.1f%%',
                startangle=140,
                colors=plt.cm.Paired.colors[:len(counts_genre)],
                textprops={'fontsize': 13, 'weight':'bold'}
            )
            ax4.set_title("Répartition des genres", fontsize=16, fontweight='bold')
        else:
            ax4.text(0.5, 0.5, "Pas de données", ha='center', va='center', fontsize=14)

        fig4.tight_layout()

        canvas4 = FigureCanvasTkAgg(fig4, master=scrollable_frame)
        canvas4.draw()
        canvas4.get_tk_widget().pack(pady=15)

if __name__ == "__main__":
    from bibliotheque import Bibliotheque
    biblio = Bibliotheque()
    biblio.charger_livre()
    biblio.charger_membre()

    app = BibliothequeGUI(biblio)
    app.mainloop()
