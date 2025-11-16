Remove Background
This desktop application allows users to remove the background from images using the U²-Net deep learning model. It is built with Python, Tkinter, and rembg, and supports previewing both the original and processed image side by side.
Features
- Select image via file dialog
- Preview original and background-removed image
- Offline support (no internet required after first run)
- Uses local ONNX model for fast processing

Model Information
This app uses the U²-Net model (u2net.onnx) for background removal. The model is included locally in the models/ folder and loaded via rembg's new_session() method.
- Model source: U²-Net GitHub
- License: Apache License 2.0
- Original paper: U²-Net: Going Deeper with Nested U-Structure for Salient Object Detection
The U²-Net model is used in accordance with the Apache 2.0 license. You are free to use, modify, and distribute this application, including the model, as long as proper attribution is maintained.


