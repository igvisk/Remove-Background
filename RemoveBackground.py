#This app using rembg and onnxruntime (nvdia,cuda) source: https://github.com/danielgatis/rembg?tab=readme-ov-file
#1. pip install rembg
# Usage as a cli

# After the installation step you can use rembg just typing rembg in your terminal window.

# The rembg command has 4 subcommands, one for each input type:

#     i for files
#     p for folders
#     s for http server
#     b for RGB24 pixel binary stream

#treba skusit nainportovat 'onnxruntime'

from rembg import remove
from PIL import Image
import io

# Načítaj obrázok
with open("vstupny_obrazok.png", "rb") as input_file:
    input_data = input_file.read()

# Odstráň pozadie
output_data = remove(input_data)

# Ulož výsledok
with open("vystupny_obrazok.png", "wb") as output_file:
    output_file.write(output_data)
