# 🖼️ GFPGAN Bulk Face Image Enhancer

This is a web-based application that allows users to upload and enhance multiple low-quality face images using the powerful **GFPGAN** model (via Replicate API). It automatically processes 5–20 photos at once and returns enhanced, clean, and realistic results with visibly improved facial details.

---

## 📌 Features

- Upload multiple images at once (supports JPG, PNG)
- Uses **GFPGAN** for face restoration
- Download enhanced images individually or all as a `.zip`
- Clean and responsive interface using **Gradio**
- Replicate API integrated for high-quality inference
- Ready for deployment on **Render**, **Hugging Face**, or other platforms

---

## 🗂️ Folder Structure

```
gfpgan-photo-enhancer/
├── Original_images/          # Original user-uploaded images
│   ├── Face1.jpg
│   ├── Face2.png
│   └── ...
├── enhanced_faces/           # Auto-generated enhanced images
│   ├── enhanced_Face1.jpg
│   └── ...
├── app.py                    # Main Gradio app logic
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .env.example              # Replicate API template
└── venv/                     # (optional) Local virtual environment
```

---

## 🚀 How to Run Locally

### 1. Clone this Repository

```bash
git clone https://github.com/Architgupta20/gfpgan-photo-enhancer.git
cd gfpgan-photo-enhancer
```

### 2. Set Up Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add Your Replicate API Key

Create a `.env` file and add your API token:

```env
REPLICATE_API_TOKEN=your_replicate_api_token_here
```

> Get your token at: https://replicate.com/account

### 4. Run the App

```bash
python app.py
```

Then open: http://127.0.0.1:7860

---

## 🌍 Deploying to Render (Free Hosting)

### 1. Push code to GitHub

Ensure `.env` is listed in `.gitignore`.

### 2. Deploy to Render

- Go to: https://render.com
- Create new "Web Service"
- Connect your GitHub repo
- **Build Command:**  
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**  
  ```
  python app.py
  ```
- **Environment Variables:**  
  `REPLICATE_API_TOKEN = your_replicate_api_token`

---

## 📦 Download Options

After enhancement:

- Preview enhanced images in gallery
- Click "Download All as ZIP" to save results

---

## 📸 Powered By

- [GFPGAN](https://github.com/TencentARC/GFPGAN) – Face restoration model
- [Replicate](https://replicate.com/) – Hosted model API
- [Gradio](https://gradio.app/) – UI framework

---

## 📄 License

This project is for educational and demonstration purposes only.
