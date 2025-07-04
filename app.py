import os
import gradio as gr
import replicate
import tempfile
from PIL import Image
import requests
from dotenv import load_dotenv

# Load the REPLICATE_API_TOKEN from environment variables
load_dotenv()
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

def enhance_face(image_list):
    enhanced_images = []

    for image in image_list:
        # Save the uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            image.save(temp_file.name)
            with open(temp_file.name, "rb") as file:
                # Call the Replicate API
                output_url = replicate.run(
                    "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
                    input={"img": file}
                )

        # Download the enhanced image
        response = requests.get(output_url)
        enhanced_temp_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
        with open(enhanced_temp_path, "wb") as out_file:
            out_file.write(response.content)

        # Open the enhanced image with PIL and add to result list
        enhanced_image = Image.open(enhanced_temp_path)
        enhanced_images.append(enhanced_image)

    return enhanced_images

# Gradio interface
iface = gr.Interface(
    fn=enhance_face,
    inputs=gr.File(file_types=["image"], label="Upload 1–5 Face Images", multiple=True),
    outputs=gr.Gallery(label="Enhanced Images").style(grid=2),
    title="Face Enhancer using GFPGAN",
    description="Upload images to enhance faces using GFPGAN via Replicate.",
)

# Launch
iface.launch()
