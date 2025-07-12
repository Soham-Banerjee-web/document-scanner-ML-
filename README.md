📄 Intelligent Document Scanner with LLM & Gradio
A smart, multi-page document scanner that allows you to:

✅ Extract structured data from scanned documents
✅ Use flexible field definitions (e.g., Name, DOB, ID No.)
✅ Upload multiple files at once
✅ Choose between traditional OCR or LLM-powered extraction
✅ Interactively correct extracted results via JSON editor
✅ Download outputs as JSON

🔧 Features
🧠 LLM Support (toggleable): Smart text understanding using simulated or actual LLMs (like GPT)

📎 Multi-file Upload: Process multiple scanned images in one go

✍️ Editable Output: Modify extracted data via live JSON editor

📤 Downloadable Output: Export structured data for use in apps or pipelines

⚙️ Built with Python, Gradio, OpenCV, Tesseract, Pandas

🚀 How to Run
Install Dependencies

bash
Copy
Edit
pip install gradio opencv-python pytesseract pandas
Install Tesseract

Ubuntu: sudo apt install tesseract-ocr

Windows: Download here

Run the App

bash
Copy
Edit
python document_scanner_gradio.py
📂 File Upload Guide
Supported formats: .jpg, .png, .jpeg

Upload single or multiple scanned pages

Enter fields to extract like:
Name, Date of Birth, Address

🧠 LLM Mode (Optional)
The Use LLM checkbox simulates large language model extraction. You can later connect this to:

OpenAI GPT-4 / GPT-3.5

Local LLMs (LLaMA, Mistral, Claude via API)

🛠️ Roadmap
 Integrate GPT-4 for actual semantic field extraction

 Export to CSV or database

 Highlight fields visually on image

 Build drag-and-drop web version

📜 License
MIT License. Free to use for academic, commercial, or personal projects.

🙌 Contributions Welcome!
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub Repo stars](https://img.shields.io/github/stars/Soham-Banerjee-web/Bolt-app?style=social)
![Last Commit](https://img.shields.io/github/last-commit/Soham-Banerjee-web/Bolt-app)
