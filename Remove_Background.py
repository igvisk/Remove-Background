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

from rembg import remove
from PIL import Image, ImageTk, ExifTags                         #Náhľad obrázka v Tkinter
import io
import os
import tkinter as tk
from tkinter import filedialog, messagebox

VERSION = "0.2"

class BackgroundRemoveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        #GUI
        self.title(f"Remove Background v.{VERSION}")
        self.resizable(False, False)
        self.set_window_geometry(800, 400)

        # Zistenie absolútnej cesty k priečinku, v ktorom sa nachádza skript
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Výstupný súbor sa uloží do podpriečinka "output"
        self.output_path = os.path.join(self.script_dir, "output", "obrazok_remBG.png")

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
        tk.Button(self, text="Vyber obrázok na odstránenie pozadia:", command=self.load_image).pack(pady=10)

        # tk.Button(self, text="testovacie").pack(side=tk.LEFT, padx=25, pady=5)        #skusobne tlacitko
        
        # Frame - Rámček na náhľady obrázkov
        preview_frame = tk.Frame(self)
        preview_frame.pack(pady=10)

        # Label - Pôvodný obrázok
        self.original_label = tk.Label(preview_frame)
        self.original_label.pack(side=tk.LEFT, padx=10)

        # Label - Upravený obrázok
        self.processed_label = tk.Label(preview_frame)
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

            output_data = remove(input_data)

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

        # Konverzia pre Tkinter -Uloženie referencie, aby sa obrázok nezmizol
        tk_image = ImageTk.PhotoImage(image)
        target_label.image = tk_image
        target_label.config(image=tk_image)




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
