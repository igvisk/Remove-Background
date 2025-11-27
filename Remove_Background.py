#This app using rembg and onnxruntime (nvdia,cuda) source: https://github.com/danielgatis/rembg?tab=readme-ov-file
#1. pip install rembg
# Usage as a cli

# After the installation step you can use rembg just typing rembg in your terminal window.

# The rembg command has 4 subcommands, one for each input type:

#     i for files
#     p for folders
#     s for http server
#     b for RGB24 pixel binary stream

#Su potrebne kniznice 3: 
# pip install rembg
# pip install pillow
#treba skusit nainportovat 'onnxruntime' - pip install onnxruntime
#!!pozn pri prvom spusteni sa stiahol cely model do cache file, v buducnosti bude potrebne ho asi zahrnut do exe suboru, nachadza sa: c:\Users\IGN\.u2net\u2net.onnx - vyskusal som spustit skript bez inetu a funguje, takze takto isto treba preverit ci to pojde po vytvoreni .exe, ak nie treba ten subor pridat do instalatora nejak


# TBD: 1. automatizacia cesty k folderu

from PIL import Image, ImageTk, ExifTags                         #Náhľad obrázka v Tkinter
from rembg import new_session, remove                            #new_session - nacitanie, remove - odstranuje bg
import os
import tkinter as tk
from tkinter import filedialog, messagebox


VERSION = "0.4"

# Farby
color_background = "#4a8dc9"
fonts = ("Brush Script MT", 14, "bold")

# Kontrola dostupnosti modelu - vzdy pouziva cache ↓ cache home-folder presmerovany na folder Remote-Background
    # Cesta k lokálnemu modelu - ak sa nenachadza pod models, stiahne ho z githubu (funkcia rembg) do folderu models
os.environ["U2NET_HOME"] = os.path.join(os.path.dirname(__file__), "models")
local_model_path = os.path.join(os.environ["U2NET_HOME"], "u2net.onnx")

session = new_session(model_path=local_model_path)

class BackgroundRemoveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        #GUI
        self.title(f"Remove Background v.{VERSION}")
        self.resizable(False, False)
        self.set_window_geometry(670, 400)

        # Zistenie absolútnej cesty k priečinku, v ktorom sa nachádza skript
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Výstupný súbor sa uloží do podpriečinka "output"
        self.output_path = os.path.join(self.script_dir, "output", "obrazok_remBG.png")

        self.configure(bg= color_background)

        self.create_widgets()

    #Metody:
        # Open app in the center of the screen         
    def set_window_geometry(self, width, height):
        # Obtain Screen resolution
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

         # Position calculation of the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set position of the window to center 
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):   
        # Tlačidlo na výber obrázku
        tk.Button(self, text="Vyber obrázok na odstránenie pozadia:", command=self.load_image, bg= color_background, fg="white", font= fonts).pack(pady=10)

        # tk.Button(self, text="testovacie").pack(side=tk.LEFT, padx=25, pady=5)        #skusobne tlacitko
        
        # Frame - Rámček na náhľady obrázkov
        preview_frame = tk.Frame(self, bg= color_background)
        preview_frame.pack(pady=10)

        # Label - Pôvodný obrázok
        self.original_label = tk.Label(preview_frame, borderwidth=4, relief="flat", bg= color_background)       #pred nacitanim obrazku su labely bez reliefov / da sa zabezpecit aj vynechanim relief-u
        self.original_label.pack(side=tk.LEFT, padx=10)

        # Label - Upravený obrázok
        self.processed_label = tk.Label(preview_frame, borderwidth=4, relief="flat", bg= color_background)
        self.processed_label.pack(side=tk.RIGHT, padx=10)

        # Tlačidlo na ukončenie aplikácie
        # tk.Button(self, text="Ukončiť", command=self.quit).pack(side=tk.BOTTOM, pady=20)


    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Obrázky", "*.png *.jpg *.jpeg")])
        if not file_path:
            return
        try:
            # Zobraz pôvodný obrázok
            self.show_preview(file_path, self.original_label)

            # Načítanie a spracovanie
            with open(file_path, "rb") as input_file:
                input_data = input_file.read()

            output_data = remove(input_data, session=session)                     #pouzije lokalny model alebo v cache ktory sa nachadza napr c:\Users\IGN\.u2net\u2net.onnx

            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

            with open(self.output_path, "wb") as output_file:
                output_file.write(output_data)

            # Zobraz upravený obrázok
            self.show_preview(self.output_path, self.processed_label)

            messagebox.showinfo("Hotovo", f"Pozadie odstránené!\nUložené do:\n{self.output_path}")
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodarilo sa spracovať obrázok:\n{e}")


        #Zobrazenie obrazka v okne
    def show_preview(self, file_path, target_label):
        image = Image.open(file_path)

        # Korekcia orientácie podľa EXIF
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = image._getexif()
            if exif is not None:
                orientation_value = exif.get(orientation)
                if orientation_value == 3:
                    image = image.rotate(180, expand=True)
                elif orientation_value == 6:
                    image = image.rotate(270, expand=True)
                elif orientation_value == 8:
                    image = image.rotate(90, expand=True)
        except Exception as e:
            print("EXIF orientácia sa nepodarila načítať:", e)
        
        # Zmenšenie obrázka
        image.thumbnail((300, 300))

        # Konverzia z objektu PIL.Image na format Tkinter (PhotoImage) -Uloženie referencie, aby obrázok nezmizol + uprava okna po načítaní obrázku
        tk_image = ImageTk.PhotoImage(image)
        target_label.image = tk_image                                            #Ulozenie referencie na obrazok do atributu labelu, inak by sa vymazal
        target_label.config(image=tk_image, relief="raised", borderwidth=4)      #tkinter relief options: ridge, groove, raised, sunken, flat(none)



if __name__ == "__main__":
    app = BackgroundRemoveApp()
    app.mainloop()


#dalsie pouzitie kniznice PIL:
# from PIL import Image

# # Načítaj obrázok
# img = Image.open("obrazok.jpg")

# # Zmeň veľkosť
# img_resized = img.resize((300, 300))

# # Ulož nový obrázok
# img_resized.save("obrazok_zmenseny.jpg")
