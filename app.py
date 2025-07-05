"""
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
|"""
import os
import gradio as gr
import replicate
from PIL import Image
import uuid

def enhance_faces(uploaded_images, user_token):
    if not user_token:
        return ["Error: You must provide a Replicate API token."]

    os.environ["REPLICATE_API_TOKEN"] = user_token

    enhanced_images = []

    for img in uploaded_images:
        try:
            # Load the image
            image = Image.open(img.name)

            # Call Replicate GFPGAN
            output_url = replicate.run(
                "tencentarc/gfpgan",
                input={"img": image}
            )

            # Save the result locally
            image_data = Image.open(replicate.files.download(output_url))
            os.makedirs("enhanced_faces", exist_ok=True)
            filename = f"enhanced_faces/enhanced_{uuid.uuid4().hex[:8]}.png"
            image_data.save(filename)

            enhanced_images.append(filename)

        except Exception as e:
            enhanced_images.append(f"Error processing image: {e}")

    return enhanced_images


iface = gr.Interface(
    fn=enhance_faces,
    inputs=[
        gr.File(file_types=["image"], label="Upload 1–5 Face Images", file_count="multiple"),
        gr.Textbox(label="Replicate API Token", type="password")
    ],
    outputs=gr.Gallery(label="Enhanced Faces"),
    title="GFPGAN Face Enhancer",
    description="Enhance face images using GFPGAN via Replicate API"
)

iface.launch(share=True)  # <== Enables public Gradio link
