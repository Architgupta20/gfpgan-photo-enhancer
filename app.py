import os
import replicate
import gradio as gr
import tempfile
import requests
import zipfile
from PIL import Image
from dotenv import load_dotenv
from base64 import b64encode

# Load API token
load_dotenv()
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

# GFPGAN Model Version
MODEL_VERSION = "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c"

def enhance_faces(images):
    zip_path = os.path.join(tempfile.gettempdir(), "enhanced_faces.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        gallery = []

        for image_file in images:
            try:
                # Save temp image
                input_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")

                # Read image file properly from path
                with open(image_file.name, "rb") as src:
                    content = src.read()
                    input_temp.write(content)
                    input_temp.flush()

                # Convert to base64
                encoded_image = b64encode(content).decode("utf-8")
                data_uri = f"data:image/jpeg;base64,{encoded_image}"

                # Replicate inference
                output_url = replicate.run(
                    MODEL_VERSION,
                    input={"img": data_uri}
                )

                # Download enhanced image
                response = requests.get(output_url)
                if response.status_code != 200:
                    raise Exception("Failed to download enhanced image")

                output_temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                with open(output_temp_path, "wb") as f:
                    f.write(response.content)

                # Add to ZIP
                zipf.write(output_temp_path, arcname=os.path.basename(output_temp_path))
                gallery.append(Image.open(output_temp_path))

            except Exception as e:
                print(f"Error processing image: {e}")

    return gallery, zip_path

# Gradio UI
demo = gr.Interface(
    fn=enhance_faces,
    inputs=gr.File(label="Upload Images", file_types=["image"], file_count="multiple"),
    outputs=[
        gr.Gallery(label="Enhanced Faces"),
        gr.File(label="Download All as ZIP")
    ],
    title="GFPGAN Face Enhancer",
    description="Upload 5–20 face images. They will be enhanced using GFPGAN (via Replicate) and zipped for download.",
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch(share=True)
