from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector




class MyApp:
    def __init__(self, root):
        self.db = None
        self.cursor = None
        self.connect_to_database()
        self.root = root
        self.root.title("GTI-UM6P")
        self.root.geometry("700x900")
        self.bg_color ="#556efc"
        self.fg_color = "white"
        self.frame_color = "#4E6575" #a67a70 #4E6575
        
        self.root.configure(bg='#e28a7a')
        
        self.title_label = Label(root, text="TABLEAU DE BORD LIGNE PRESSES", font=("Arial", 22, "bold"), bg=self.bg_color,
                                 fg=self.fg_color)
        self.title_label.pack(fill=X)

        
        self.subtitle_label_presse = Label(root, text="Données Temps Réel par presse", font=("Arial", 18, "bold"),
                                           bg=self.bg_color, fg=self.fg_color)
        self.subtitle_label_presse.pack(pady=5, padx=110, anchor="w")  

        
        self.table_frame_presse = Frame(root, bg=self.bg_color)
        self.table_frame_presse.pack(pady=5, padx=10, anchor='w')  

        
        self.columns_presse = ("Presse", "TRS", "Total pièces bonnes", "Consommation matière", "Cumul temps arrêt")
        self.treeview_presse = ttk.Treeview(self.table_frame_presse, columns=self.columns_presse, show="headings", height=3)

        
        for col in self.columns_presse:
            self.treeview_presse.heading(col, text=col, anchor="center")
            self.treeview_presse.column(col, width=120)

        self.treeview_presse.pack(expand=YES, fill=BOTH)

        
        self.subtitle_label_ligne = Label(root, text="Données de la ligne Temps Réel", font=("Arial", 18, "bold"),
                                          bg=self.bg_color, fg=self.fg_color)
        self.subtitle_label_ligne.pack(pady=5, padx=110, anchor='w')  

        
        self.table_frame_ligne = Frame(root, bg=self.bg_color)
        self.table_frame_ligne.pack(pady=10, padx=10, anchor='w')  

        
        self.columns_ligne = ("TRS Globale", "Total pièces bonnes", "Consommation matière", "Cumul temps arrêt")
        self.treeview_ligne = ttk.Treeview(self.table_frame_ligne, columns=self.columns_ligne, show="headings", height=1)

        
        for col in self.columns_ligne:
            self.treeview_ligne.heading(col, text=col, anchor="center")
            self.treeview_ligne.column(col, width=150)

        self.treeview_ligne.pack(expand=YES, fill=BOTH)

        
        self.subtitle_label_periode = Label(root, text="Données par période", font=("Arial", 18, "bold"),
                                            bg=self.bg_color, fg=self.fg_color)
        self.subtitle_label_periode.pack(pady=5, padx=110, anchor='w')  

        
        self.entry_frame = Frame(root, bg=self.bg_color)
        self.entry_frame.pack(pady=10, padx=10, anchor='w')  

        
        self.label_debut = Label(self.entry_frame, text="Période début:", font=("Arial", 11, "bold"), bg=self.bg_color,
                                 fg=self.fg_color)
        self.label_debut.grid(row=0, column=0, padx=10)

        self.entry_debut = DateEntry(self.entry_frame, font=("Arial", 11), date_pattern="yyyy-mm-dd")
        self.entry_debut.grid(row=0, column=1, padx=10)

    
        self.label_fin = Label(self.entry_frame, text="Période fin:", font=("Arial", 11, "bold"), bg=self.bg_color,
                          fg=self.fg_color)
        self.label_fin.grid(row=0, column=2, padx=10)

        self.entry_fin = DateEntry(self.entry_frame,  font=("Arial", 11),date_pattern="yyyy-mm-dd")
        self.entry_fin.grid(row=0, column=3, padx=10)
        # ====

        self.subtitle_label_ligne = Label(root, text="Données par presse pour la période", font=("Arial", 18, "bold"),
                                          bg=self.bg_color, fg=self.fg_color)
        self.subtitle_label_ligne.pack(pady=5, padx=110, anchor='w')  
        
        self.table3_frame = Frame(root, bg=self.bg_color)
        self.table3_frame.pack(pady=10, padx=10, anchor='w')  


        self.columns_table3 = ("Presse", "TRS", "Total pièces bonnes", "Consommation matière", "Cumul temps arrêt")
        self.treeview_table3 = ttk.Treeview(self.table3_frame, columns=self.columns_table3, show="headings", height=3)

        
        for col in self.columns_table3:
            self.treeview_table3.heading(col, text=col, anchor="center")
            self.treeview_table3.column(col, width=120)

        self.treeview_table3.pack(expand=YES, fill=BOTH)
        self.subtitle_label_ligne = Label(root, text="Données globale pour la période", font=("Arial", 18, "bold"),
                                          bg=self.bg_color, fg=self.fg_color)
        self.subtitle_label_ligne.pack(pady=5, padx=110, anchor='w')  

        
        self.table4_frame = Frame(root, bg=self.bg_color)
        self.table4_frame.pack(pady=10, padx=10, anchor='w')  

        
        self.columns_table4 = ("TRS Globale", "Total pièces bonnes", "Consommation matière", "Cumul temps arrêt")
        self.treeview_table4 = ttk.Treeview(self.table4_frame, columns=self.columns_table4, show="headings", height=1)

        
        for col in self.columns_table4:
            self.treeview_table4.heading(col, text=col, anchor="center")
            self.treeview_table4.column(col, width=150)

        self.treeview_table4.pack(expand=YES, fill=BOTH)
        
        self.treeview_presse.insert("", "end", values=["", "", "", "", ""])
        self.treeview_ligne.insert("", "end", values=["", "", "", ""])
        
        update_button = Button(root, text="Mise à jour", font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.fg_color,
                               command=self.update_values)
        update_button.pack(pady=10)  

        self.update_values()
    
        

        
        
       
        
    

    def connect_to_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost", user="root", password="    ", database="projet_TP5"
            )
            self.cursor = self.db.cursor(buffered=True)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            
            exit()   
    def clear_treeview(self, treeview):
     for item in treeview.get_children():
        treeview.delete(item)
     treeview.update()
    
    def update_values(self):
        
        
        sigmaPieceBonneP1 = None
        sigmaPieceBonneP2 = None
        sigmaPieceBonneP3= None
        consumptionMaterialP1= None
        consumptionMaterialP2 = None
        cumulArretP1= None
        cumulArretP2 = None
        periode_debut = self.entry_debut.get_date()
        periode_fin = self.entry_fin.get_date()
        self.clear_treeview(self.treeview_presse)
        self.clear_treeview(self.treeview_ligne)
        self.clear_treeview(self.treeview_table3) 
        self.clear_treeview(self.treeview_table4) 

        
        try:
           if not self.db.is_connected():
              self.connect_to_database()

    # --------------#
           cursor1 = self.db.cursor()
           cursor1.execute("SELECT Presse1_PieceBonne_Value * 100 / "
                    "(Presse1_PieceBonne_Value + Presse1_PieceMauvaise_Value) "
                    "FROM Presse1 ORDER BY DateAndTime DESC LIMIT 1")
           trsPresse1 = cursor1.fetchone()
           print(trsPresse1)
           trsPresse11 = "{:.2f}%".format(trsPresse1[0])

           cursor1.execute("SELECT SUM(presse1_PieceBonne_Value) FROM presse1 WHERE presse1_MachineEnMarche_Value = 1")
           sigmaPieceBonneP1 = cursor1.fetchone()

           cursor1.execute("SELECT presse1_ConsommationMatiere_Value FROM presse1 ORDER BY DateAndTime DESC LIMIT 1")
           consumptionMaterialP1 = cursor1.fetchone()

           cursor1.execute("SELECT COUNT(*) * 100 FROM presse1 WHERE presse1_MachineEnMarche_Value  =0")
           y = cursor1.fetchone()

           cursor1.execute("SELECT COUNT(*) FROM presse1")
           x = cursor1.fetchone()

           cumulArretP1 = tuple(ele1 / ele2 for ele1, ele2 in zip(y, x))
           cumulArretP11 = "{:.2f}%".format(cumulArretP1[0])

           cursor1.close()

            #------------#
           cursor2 = self.db.cursor()
           cursor2.execute("SELECT Presse2_PieceBonne_Value * 100 / "
                            "(Presse2_PieceBonne_Value + Presse2_PieceMauvaise_Value) "
                            "FROM Presse2 ORDER BY DateAndTime DESC LIMIT 1")
           trsPresse2 = cursor2.fetchone()
           print(trsPresse2)
           trsPresse22 = "{:.2f}%".format(trsPresse2[0])

           cursor2.execute("SELECT SUM(presse2_PieceBonne_Value) FROM presse2 WHERE presse2_MachineEnMarche_Value = 1")
           sigmaPieceBonneP2 = cursor2.fetchone()

           cursor2.execute("SELECT presse2_ConsommationMatiere_Value FROM presse2 ORDER BY DateAndTime DESC LIMIT 1")
           consumptionMaterialP2 = cursor2.fetchone()
           print(consumptionMaterialP2)

           cursor2.execute("SELECT COUNT(*) * 100 FROM presse2 WHERE presse2_MachineEnMarche_Value  =0")
           var1 = cursor2.fetchone()

           cursor2.execute("SELECT COUNT(*) FROM presse2")
           var2 = cursor2.fetchone()

           cumulArretP2 = tuple(ele1 / ele2 for ele1, ele2 in zip(var1, var2))
           cumulArretP22 = "{:.2f}%".format(cumulArretP2[0])

           cursor2.close()
           #----------#
           cursor3 = self.db.cursor()
           cursor3.execute("SELECT Presse3_PieceBonne_Value * 100 / "
                            "(Presse3_PieceBonne_Value + Presse3_PieceMauvaise_Value) "
                            "FROM Presse3 ORDER BY DateAndTime DESC LIMIT 1")
           trsPresse3 = cursor3.fetchone()
           
           trsPresse33 = "{:.2f}%".format(trsPresse3[0])

           cursor3.execute("SELECT SUM(presse3_PieceBonne_Value) FROM presse3 WHERE presse3_MachineEnMarche_Value = 1")
           sigmaPieceBonneP3 = cursor3.fetchone()

           cursor3.execute("SELECT presse3_ConsommationMatiere_Value FROM presse3 ORDER BY DateAndTime DESC LIMIT 1")
           consumptionMaterialP3 = cursor3.fetchone()
           print(consumptionMaterialP3)

           cursor3.execute("SELECT COUNT(*) * 100 FROM presse3 WHERE presse3_MachineEnMarche_Value  =0")
           var1 = cursor3.fetchone()

           cursor3.execute("SELECT COUNT(*) FROM presse3")
           var2 = cursor3.fetchone()

           cumulArretP3 = tuple(ele1 / ele2 for ele1, ele2 in zip(var1, var2))
           cumulArretP33 = "{:.2f}%".format(cumulArretP3[0])

           cursor3.close()

           #------- data pour une période donnée:
            #--- pour la presse1
           cursor4=self.db.cursor()
           cursor4.execute("""
           SELECT AVG(Presse1_PieceBonne_Value * 100 / 
               (Presse1_PieceBonne_Value + Presse1_PieceMauvaise_Value + presse1_rebutDeclare_value))
           FROM Presse1
           WHERE DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           trsPresse1P=cursor4.fetchone()
           print(trsPresse1P)
           cursor4.execute("""
           SELECT SUM(presse1_PieceBonne_Value)
           FROM presse1
           WHERE presse1_MachineEnMarche_Value = 1
           AND DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           sigmaPieceBonneP1P=cursor4.fetchone()
           cursor4.execute("""
           SELECT SUM(presse1_ConsommationMatiere_Value)
           FROM presse1
           WHERE presse1_MachineEnMarche_Value = 1
           AND DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           consumptionMaterialP1P=cursor4.fetchone()
           cursor4.execute("""
           SELECT COUNT(*) * 100
           FROM presse1
           WHERE presse1_MachineEnMarche_Value = 0
           AND DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           var1 = cursor4.fetchone()

           cursor4.execute("""
           SELECT COUNT(*)
           FROM presse1
           WHERE DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           var2 = cursor4.fetchone()
           cumulArretP1P = tuple(ele1 / ele2 for ele1, ele2 in zip(var1, var2))
           #--------- presse 2 
           cursor4=self.db.cursor()
           cursor4.execute("""
           SELECT AVG(Presse2_PieceBonne_Value * 100 / 
               (Presse2_PieceBonne_Value + Presse2_PieceMauvaise_Value + presse2_rebutDeclare_value))
           FROM Presse2
           WHERE DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           trsPresse2P=cursor4.fetchone()
           
           cursor4.execute("""
           SELECT SUM(presse2_PieceBonne_Value)
           FROM presse2
           WHERE presse2_MachineEnMarche_Value = 1
           AND DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           sigmaPieceBonneP2P=cursor4.fetchone()
           cursor4.execute("""
           SELECT SUM(presse2_ConsommationMatiere_Value)
           FROM presse2
           WHERE presse2_MachineEnMarche_Value = 1
           AND DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           consumptionMaterialP2P=cursor4.fetchone()
           cursor4.execute("""
           SELECT COUNT(*) * 100
           FROM presse2
           WHERE presse2_MachineEnMarche_Value = 0
           AND DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           var1 = cursor4.fetchone()

           cursor4.execute("""
           SELECT COUNT(*)
           FROM presse2
           WHERE DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           var2 = cursor4.fetchone()
           cumulArretP2P = tuple(ele1 / ele2  for ele1, ele2 in zip(var1, var2))
           #------------ presse3 ------
           cursor4=self.db.cursor()
           cursor4.execute("""
           SELECT AVG(Presse3_PieceBonne_Value * 100 / 
               (Presse3_PieceBonne_Value + Presse3_PieceMauvaise_Value + presse3_rebutDeclare_value))
           FROM Presse3
           WHERE DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           trsPresse3P=cursor4.fetchone()
           
           cursor4.execute("""
           SELECT SUM(presse3_PieceBonne_Value)
           FROM presse3
           WHERE presse3_MachineEnMarche_Value = 1
           AND DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           sigmaPieceBonneP3P=cursor4.fetchone()
           cursor4.execute("""
           SELECT SUM(presse3_ConsommationMatiere_Value)
           FROM presse3
           WHERE presse3_MachineEnMarche_Value = 1
           AND DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           consumptionMaterialP3P=cursor4.fetchone()
           cursor4.execute("""
           SELECT COUNT(*) * 100
           FROM presse3
           WHERE presse3_MachineEnMarche_Value = 0
           AND DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           var1 = cursor4.fetchone()

           cursor4.execute("""
           SELECT COUNT(*)
           FROM presse3
           WHERE DATE(DateAndTime) BETWEEN '{}' AND '{}'
           """.format(periode_debut, periode_fin))
           var2 = cursor4.fetchone()
           cumulArretP3P = tuple(ele1 / ele2  for ele1, ele2 in zip(var1, var2))
            #--------- données globale pour la période 
           trsGlobaleP=sum(trsPresse1P+trsPresse2P+trsPresse3P)/3
           sigmaPieceBonneGP=sum(sigmaPieceBonneP1P+sigmaPieceBonneP2P+sigmaPieceBonneP3P)
           consumptionMGP=sum(consumptionMaterialP1P+consumptionMaterialP2P+consumptionMaterialP3P)
           cumulArretGP=(sum(cumulArretP1P+cumulArretP2P+cumulArretP3P))/3
           #---- formattage data pour affichage
           trsPresse1P = "{:.2f}%".format(trsPresse1P[0])
           trsPresse2P = "{:.2f}%".format(trsPresse2P[0])
           trsPresse3P = "{:.2f}%".format(trsPresse3P[0])
           cumulArretP1P = "{:.2f}%".format(cumulArretP1P[0])
           cumulArretP2P = "{:.2f}%".format(cumulArretP2P[0])
           cumulArretP3P = "{:.2f}%".format(cumulArretP3P[0])
           trsGlobaleP="{:.2f}%".format(trsGlobaleP)
           cumulArretGP="{:.2f}%".format(cumulArretGP)
           




        except Exception as e:
           print(f"Error: {e}")
        self.db.commit()
       

        #finally:
            #if self.cursor is not None and self.cursor.is_connected():
                #self.cursor.close()

        values_RT = [
            {"Presse": "1", "TRS": trsPresse11, "Total pièces bonnes": sigmaPieceBonneP1,
             "Consommation matière": consumptionMaterialP1,
             "Cumul temps arrêt": cumulArretP11},
            {"Presse": "2", "TRS": trsPresse22, "Total pièces bonnes": sigmaPieceBonneP2,
             "Consommation matière": consumptionMaterialP2,
             "Cumul temps arrêt": cumulArretP22},
            {"Presse": "3", "TRS": trsPresse33, "Total pièces bonnes": sigmaPieceBonneP3, "Consommation matière": consumptionMaterialP3,
             "Cumul temps arrêt": cumulArretP33},
        ]
        trsGlobale= (trsPresse1[0]+trsPresse2[0]+trsPresse3[0])/3
        trsGlobaleGG= "{:.2f}%".format(trsGlobale)
        sigmaPieceBonneG=sum(sigmaPieceBonneP1+sigmaPieceBonneP2+sigmaPieceBonneP3)
        consumptionMG=sum(consumptionMaterialP1+consumptionMaterialP2+consumptionMaterialP3)
        cumulArretG=(sum(cumulArretP1+cumulArretP2+cumulArretP3)/3)
        cumulArretG="{:.2f}%".format(cumulArretG)
        valuesGRT = [
            {"TRS Globale": trsGlobaleGG, "Total pièces bonnes": sigmaPieceBonneG, "Consommation matière": consumptionMG,
             "Cumul temps arrêt": cumulArretG }
        ]

        values_PRT = [
            {"Presse": "1", "TRS": trsPresse1P, "Total pièces bonnes": sigmaPieceBonneP1P,
             "Consommation matière": consumptionMaterialP1P,
             "Cumul temps arrêt": cumulArretP1P},
            {"Presse": "2", "TRS": trsPresse2P, "Total pièces bonnes": sigmaPieceBonneP2P,
             "Consommation matière": consumptionMaterialP2P,
             "Cumul temps arrêt": cumulArretP2P},
            {"Presse": "3", "TRS": trsPresse3P, "Total pièces bonnes": sigmaPieceBonneP3P, "Consommation matière": consumptionMaterialP3P,
             "Cumul temps arrêt": cumulArretP3P},
        ]
        values_GP = [
            {"TRS Globale": trsGlobaleP, "Total pièces bonnes": sigmaPieceBonneGP, "Consommation matière": consumptionMGP,
             "Cumul temps arrêt": cumulArretGP }
        ]
        
        
        for value in values_RT:
            self.treeview_presse.insert("", "end", values=list(value.values()))

        for value in valuesGRT:
            self.treeview_ligne.insert("", "end", values=list(value.values()))
        for value in values_PRT:
            self.treeview_table3.insert("", "end", values=list(value.values()))
        for value in values_GP:
            self.treeview_table4.insert("", "end", values=list(value.values()))

        self.treeview_presse.update()
        self.treeview_ligne.update()
        self.treeview_table3.update()
        self.treeview_table4.update()
        

    
    

        

if __name__ == "__main__":
    root = Tk()
    app = MyApp(root)
    root.mainloop()
