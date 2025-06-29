import gradio as gr
import pytesseract
import cv2
import numpy as np
import pandas as pd
import tempfile
import json
import os

# Simulate an LLM extraction (replace with real API if needed)
def extract_fields_llm(text, fields):
    extracted = {}
    for field in fields:
        # Fake logic: find field name and next word
        idx = text.lower().find(field.lower())
        if idx != -1:
            after = text[idx + len(field):].split(" ", 3)
            extracted[field] = after[1] if len(after) > 1 else "Unknown"
        else:
            extracted[field] = "Not found"
    return extracted

def extract_text_with_positions(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DATAFRAME)
    data = data.dropna(subset=["text"])
    return data

def match_fields(ocr_df, user_fields):
    results = {}
    for field in user_fields:
        for idx, row in ocr_df.iterrows():
            if field.lower() in row['text'].lower():
                neighbors = ocr_df[(ocr_df['top'] - row['top']).abs() < 30]
                value_index = idx + 1
                if value_index < len(ocr_df):
                    value = " ".join(ocr_df.iloc[value_index:value_index+3]['text'].tolist())
                    results[field] = value
                break
        if field not in results:
            results[field] = "Not found"
    return results

def process_documents(fields_str, image_files, use_llm):
    user_fields = [f.strip() for f in fields_str.split(",") if f.strip()]
    all_results = {}

    for file_obj in image_files:
        file_bytes = np.frombuffer(file_obj.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        ocr_df = extract_text_with_positions(image)
        text = " ".join(ocr_df["text"].astype(str).tolist())

        if use_llm:
            result = extract_fields_llm(text, user_fields)
        else:
            result = match_fields(ocr_df, user_fields)

        all_results[file_obj.name] = result

    json_str = json.dumps(all_results, indent=4)
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w')
    tmpfile.write(json_str)
    tmpfile.close()

    return all_results, tmpfile.name

def correct_result_editor(result):
    # Render editable dictionary as JSON text
    return json.dumps(result, indent=4)

def update_json(text):
    try:
        corrected = json.loads(text)
        return corrected
    except:
        return {"error": "Invalid JSON"}

with gr.Blocks() as demo:
    gr.Markdown("## 🧾 Multi-Document Scanner with LLM and Manual Correction")

    with gr.Row():
        fields_input = gr.Textbox(label="Enter Fields (comma separated)", placeholder="Name, Date of Birth, ID")
        use_llm_checkbox = gr.Checkbox(label="Use LLM for Extraction", value=False)

    image_input = gr.File(label="Upload Documents", file_types=[".png", ".jpg", ".jpeg"], file_count="multiple")
    submit_button = gr.Button("Extract Data")

    result_output = gr.JSON(label="Extracted Results")
    download_link = gr.File(label="Download JSON")

    gr.Markdown("### ✍️ Interactive Correction")
    editable_json = gr.Code(label="Edit JSON", language="json")
    update_button = gr.Button("Update Output")
    final_output = gr.JSON(label="Updated Result")

    submit_button.click(
        fn=process_documents,
        inputs=[fields_input, image_input, use_llm_checkbox],
        outputs=[result_output, download_link]
    )

    result_output.change(fn=correct_result_editor, inputs=result_output, outputs=editable_json)
    update_button.click(fn=update_json, inputs=editable_json, outputs=final_output)

if __name__ == "__main__":
    demo.launch()
