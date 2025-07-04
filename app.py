import gradio as gr
import replicate
import os
from dotenv import load_dotenv
from PIL import Image
import tempfile

# Load environment variables (especially REPLICATE_API_TOKEN)
load_dotenv()

# Ensure the Replicate API token is set
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

# Function to enhance a single image
def enhance_image(image):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
        image.save(temp.name)
        output_url = replicate.run(
            "tencentarc/gfpgan:0fbacf7afc6c144e5be9767cff80f25aff23e52b0708f17e20f9879b2f21516c",
            input={"img": open(temp.name, "rb")}
        )
    response = requests.get(output_url)
    enhanced_image_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    with open(enhanced_image_path, "wb") as f:
        f.write(response.content)
    return Image.open(enhanced_image_path)

# Gradio interface
interface = gr.Interface(
    fn=enhance_image,
    inputs=gr.Image(type="pil", label="Upload a face image"),
    outputs=gr.Image(type="pil", label="Enhanced image"),
    title="GFPGAN Face Enhancer",
    description="Upload a facial photo to enhance using the GFPGAN model.",
)

# IMPORTANT: Bind to 0.0.0.0 and dynamic port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    interface.launch(server_name="0.0.0.0", server_port=port)
