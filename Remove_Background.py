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
from PIL import Image
import io
from tkinter import *
import os

version = 0.1

#GUI
window = Tk()
window.title(f"Remove Background v.{version}")
window.resizable(False,False)

window_width = 500
window_height = 800
    
    # Open app in the center of the screen 
        # Obrain Screen resolution
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

    # Position calculation of the window
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
    # Set position of the window to center 
window.geometry(f"{window_width}x{window_height}+{x}+{y}")



# OS - adresar urcenie + Ikona Dynamicky zisti cestu k súboru
script_dir = os.path.dirname(os.path.abspath(__file__))       #zistenie absolútnej cesty k priečinku, v ktorom sa nachádza sputený Python skript

output_dir = os.path.join(script_dir, "obrazok_remBG.png")              #momentalne vystupny subor ulozi do adresara kde je skript

# icon_path = os.path.join(script_dir, "Remote-Background.ico")     #vytvorí kompletnú cestu k súboru s ikonou, ktorý sa nachádza v rovnakom priečinku ako skript


# Načítaj obrázok
with open(r"c:\py\my_projects\Remove-Background\20250816_151440.jpg", "rb") as input_file:           #TBD zautomatizovat cez os aby vzdy nahodilo cestu
    input_data = input_file.read()

# Odstráň pozadie
output_data = remove(input_data)

# Ulož výsledok
with open(output_dir, "wb") as output_file:         #TBD zautomatizovat cez os aby vzdy nahodilo cestu - 1.tam kde je script, 2.popripade dat moznost kde sa ma ulozit
    output_file.write(output_data)



window.mainloop()



#dalsie pouzitie kniznice PIL:
# from PIL import Image

# # Načítaj obrázok
# img = Image.open("obrazok.jpg")

# # Zmeň veľkosť
# img_resized = img.resize((300, 300))

# # Ulož nový obrázok
# img_resized.save("obrazok_zmenseny.jpg")
