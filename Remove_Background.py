#This app using rembg and onnxruntime (nvdia,cuda) source: https://github.com/danielgatis/rembg?tab=readme-ov-file

from PIL import Image, ImageTk, ExifTags                         #Náhľad obrázka v Tkinter - pillow library
from rembg import new_session, remove                            #new_session - nacitanie, remove - odstranuje bg
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Label
import subprocess                                               #for multiplatform use - fallback / Linux
from tkinterdnd2 import DND_FILES, TkinterDnD                   #drag&drop lib


VERSION = "1.2b"

# Model path - Kontrola dostupnosti modelu - vzdy pouziva cache ↓ cache home-folder presmerovany na folder Remote-Background
    # Cesta k lokálnemu modelu - ak sa nenachadza pod models, stiahne ho z githubu (funkcia rembg) do folderu models
os.environ["U2NET_HOME"] = os.path.join(os.path.dirname(__file__), "models")
local_model_path = os.path.join(os.environ["U2NET_HOME"], "u2net.onnx")
session = new_session(model_path=local_model_path)

# Colors, fonts
color_background = "#4a8dc9"
color_foreground = "#FFFCF7"
fonts = ("Cascadia Mono ExtraLight", 14, "bold")

class BackgroundRemoveApp(TkinterDnD.Tk):                   #TkinterDnD - drag&drop
    def __init__(self):
        super().__init__()
        #GUI
        self.title(f"Remove Background v{VERSION}")
        self.resizable(False, False)
        self.set_window_geometry(660, 415)

        # Zistenie absolútnej cesty k priečinku, v ktorom sa nachádza skript
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Icon
        try:
            icon_path = os.path.join(self.script_dir, "Remove-Background.ico")
            self.iconbitmap(icon_path)
        except Exception as e:
             messagebox.showwarning("Upozornenie", f"Ikona sa nepodarila načítať:\n{e}")
        
        # Background color
        self.configure(bg= color_background)

        # Vytvor menu
        self.create_menu()

        # Widgety
        self.create_widgets()

        # Drag & Drop registrácia
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.handle_drop)

        # klávesové skratky
        self.bind("<Control-n>", lambda e: self.load_image())
        self.bind("<Control-o>", lambda e: self.show_output_folder())
        self.bind("<Control-q>", lambda e: self.quit_app())
        self.bind("<F1>", lambda e: self.show_about())

    # Metódy
    # Drag & Drop
    def handle_drop(self, event):
        # fade effect animation
        self.animate_bg(
        self.processed_label,
        start=(74, 141, 201),
        end=(111, 168, 220)
        )
        self.after(300, lambda: self.animate_bg(
        self.processed_label,
        start=(111, 168, 220),
        end=(74, 141, 201)
        ))
        
        file_path = event.data.strip("{}")          #odstráni {} ak sú vo Windows
        if os.path.isfile(file_path):
            self.process_file(file_path)
    
    # po kliknuti na processed label otvori explorer a oznaci subor
    def open_and_select(self, path):
        subprocess.Popen(f'explorer /select,"{path}"')

    # --- Menu ---
    def create_menu(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        # 1. File
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Otvor súbor  Ctrl+N", command=self.load_image)
        file_menu.add_command(label="Výstupy         Ctrl+O", command=self.show_output_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Ukončiť         Ctrl+Q", command=self.quit_app)
        menu_bar.add_cascade(label="Súbor", menu=file_menu)
        
        # 2. Help
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="O programe   F1", command=self.show_about)
        menu_bar.add_cascade(label="Pomoc", menu=help_menu)

    # Funkcie menu
    def show_output_folder(self):
        # pass
        output_dir =  os.path.join(self.script_dir, "output")
        os.makedirs(output_dir, exist_ok=True)                     #ak folder neexistuje, vytvori sa

        try:
            # Windows – otvorí priečinok v Explorer
            os.startfile(output_dir)
        except AttributeError:
            # Linux/Mac fallback
            try:
                subprocess.Popen(["xdg-open", output_dir])
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodarilo sa otvoriť priečinok:\n{e}")

    def quit_app(self):
        self.quit()

    # About window
    def show_about(self):
        about_window = tk.Toplevel(self)
        about_window.title("About")
        about_window.resizable(False, False)
        about_window.configure(bg=color_background)

        # vycentrovanie about okna
        self.set_window_geometry(570, 280, about_window)

        # Nastavenie ikony aj pre About okno
        icon_path = os.path.join(self.script_dir, "Remove-Background.ico")
        if os.path.exists(icon_path):
            about_window.iconbitmap(icon_path)   # Windows (.ico)

        text = (
                "Aplikácia: Remove Background\n"
                f"Verzia: {VERSION}\n\n"
                "Autor: Igor Vitovský\n"
                "GitHub: github.com/igvisk\n\n"
                "Aplikácia využíva AI model U²Net\n"
                "na presné odstránenie pozadia.\n"
                "Všetko spracovanie prebieha offline."
        )

        about_label = Label(about_window, text=text, font= fonts, justify="left", bg= color_background, fg= color_foreground)
        about_label.pack(padx=20, pady=20)
        # Skratka pre about_window
        about_window.bind("<Escape>", lambda e: about_window.destroy())

    #Metody (set window geometry. widgets, load_image, show_preview):
    
        # Window geometry - Open app in the center of the screen         
    def set_window_geometry(self, width, height, window=None):       
        
        # ak nepošleš window, použije sa hlavné okno (self)
        if window is None:
            window = self
        # Obtain Screen resolution
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

         # Position calculation of the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set position of the window to center 
        window.geometry(f"{width}x{height}+{x}+{y}")

        # Widgets
    def create_widgets(self):   
        # Tlačidlo na výber obrázku
        btn = tk.Button(self, text="Vybrať alebo presunúť obrázok",
                        command=self.load_image, 
                        bg=color_background, 
                        fg=color_foreground, 
                        font=fonts,
                        cursor="trek")      # sailboat if blue bg
        btn.pack(pady=15, padx=5, fill="x")

        # naviazanie hover efektu
        btn.bind("<Enter>", self.on_enter)
        btn.bind("<Leave>", self.on_leave)

        # Frame - Rámček na náhľady obrázkov
        self.preview_frame = tk.Frame(self, bg=color_background)
        self.preview_frame.pack(pady=0)

        # Label - Pôvodný obrázok
        self.original_label = tk.Label(self.preview_frame, borderwidth=4, relief="flat", bg= color_background)       #pred nacitanim obrazku su labely bez reliefov / da sa zabezpecit aj vynechanim relief-u
        self.original_label.pack(side=tk.LEFT, padx=5)

        # Label - Upravený obrázok
        self.processed_label = tk.Label(self.preview_frame, borderwidth=4, relief="flat", bg= color_background, cursor="trek")
        self.processed_label.pack(side=tk.RIGHT, padx=5)

        # klik na processed label otvorí priečinok s výstupom
        self.processed_label.bind("<Button-1>", lambda e: self.open_and_select(self.output_path))

        # Hover pre processed_label
        self.processed_label.bind("<Enter>", lambda e: self.animate_bg(self.processed_label, 
            start=(74, 141, 201),   # #4a8dc9
            end=(111, 168, 220)     # #6fa8dc
            )
        )

        self.processed_label.bind("<Leave>", lambda e: self.animate_bg(self.processed_label,
                start=(111, 168, 220),
                end=(74, 141, 201)
                )
        )

        # --- Hover efekty pre tlačidlá ---
    def on_enter(self, e):
        self.animate_bg(
        e.widget,
        start=(74, 141, 201),   # pôvodná farba #4a8dc9
        end=(111, 168, 220)     # hover farba #6fa8dc
        )
        e.widget['foreground'] = '#ffffff'

    def on_leave(self, e):
        self.animate_bg(
        e.widget,
        start=(111, 168, 220),
        end=(74, 141, 201)
        )
        e.widget['foreground'] = '#FFFCF7'

        # Universal background color animation (used for hover + highlight) -- #time if steps are 10 - 250ms, if steps=30 -> 900ms
    def animate_bg(self, widget, start, end, steps=10, step=0):
        # start/end sú RGB tuple, napr. (74, 141, 201)
        if step > steps:
            return

        r = int(start[0] + (end[0] - start[0]) * (step / steps))
        g = int(start[1] + (end[1] - start[1]) * (step / steps))
        b = int(start[2] + (end[2] - start[2]) * (step / steps))

        color = f"#{r:02x}{g:02x}{b:02x}"
        widget.configure(bg=color)

        widget.after(35, lambda: self.animate_bg(widget, start, end, steps, step + 1))      #fade effect time widget.after(time of step, )
    
        # Load file
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Obrázky", "*.png *.jpg *.jpeg")])
        if file_path:
            # animovaný fade effect processed_label
            self.animate_bg(
                self.processed_label,
                start=(74, 141, 201),   # pôvodná farba #4a8dc9
                end=(111, 168, 220)     # hover farba #6fa8dc
            )

            self.after(300, lambda: self.animate_bg(
                self.processed_label,
                start=(111, 168, 220),
                end=(74, 141, 201)
            ))
            
            self.process_file(file_path)

        # Process file
    def process_file(self, file_path):
        try:
            # Zobraz pôvodný obrázok
            self.show_preview(file_path, self.original_label)

            # Načítanie a spracovanie
            with open(file_path, "rb") as input_file:
                input_data = input_file.read()

            output_data = remove(input_data, session=session)                     #pouzije lokalny model alebo v cache ktory sa nachadza napr c:\Users\IGN\.u2net\u2net.onnx
  
            # Vytvor priečinok output
            output_dir = os.path.join(self.script_dir, "output")
            os.makedirs(output_dir, exist_ok=True)

            # Rozdelenie názvu súboru na meno + príponu
            base_name, ext = os.path.splitext(os.path.basename(file_path))
            output_file_name = f"{base_name} -BG_removed{ext}"
            self.output_path = os.path.join(output_dir, output_file_name)

            # Uloženie výsledku
            with open(self.output_path, "wb") as output_file:
                output_file.write(output_data)

            # Zobraz upravený obrázok
            self.show_preview(self.output_path, self.processed_label)

            # Message window after successful image processing - hidden for now (annoying)
            # messagebox.showinfo("Hotovo", f"Pozadie odstránené!\n\nUložené do:\n{self.output_path}\n\nPre otvorenie lokality súboru stlač Ctrl+O alebo klikni na spracovaný obrázok")

            # --- Jemný pulz processed_label po spracovaní obrázka (2x) ---
            # 1. pulz – zosvetlenie
            self.animate_bg(
                self.processed_label,
                start=(74, 141, 201),
                end=(111, 168, 220),
                steps=25
            )

            # 1. pulz – návrat
            self.after(700, lambda: self.animate_bg(
                self.processed_label,
                start=(111, 168, 220),
                end=(74, 141, 201),
                steps=25
            ))

            # 2. pulz – zosvetlenie
            self.after(1400, lambda: self.animate_bg(
                self.processed_label,
                start=(74, 141, 201),
                end=(111, 168, 220),
                steps=25
            ))

            # 2. pulz – návrat
            self.after(2100, lambda: self.animate_bg(
                self.processed_label,
                start=(111, 168, 220),
                end=(74, 141, 201),
                steps=25
            ))

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
        
        # Zmenšenie preview obrázka
        image.thumbnail((300, 300))

        # Konverzia z objektu PIL.Image na format Tkinter (PhotoImage) -Uloženie referencie, aby obrázok nezmizol + uprava okna po načítaní obrázku
        tk_image = ImageTk.PhotoImage(image)
        target_label.image = tk_image                                            #Ulozenie referencie na obrazok do atributu labelu, inak by sa vymazal
        target_label.config(image=tk_image, relief="raised", borderwidth=4)      #tkinter relief options: ridge, groove, raised, sunken, flat(none)


if __name__ == "__main__":
    app = BackgroundRemoveApp()
    app.mainloop()