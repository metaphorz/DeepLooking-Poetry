"""
Generate segmentation mask for The Mouth of the Lourmarin River (Paul Camille Guigou, 1867).
Just the mask — no poem images yet.
"""
import os
from google import genai
from google.genai import types
from PIL import Image

# Load API key
with open(os.path.expanduser("~/.env")) as f:
    for line in f:
        if line.startswith("VITE_GEMINI_API_KEY="):
            api_key = line.strip().split("=", 1)[1]
            break

client = genai.Client(api_key=api_key)

# Load artwork image
im = Image.open("images/LourmarinRiver/IMG_0606.WEBP")
w, h = im.size
print(f"Artwork size: {w} x {h}")

# --- PROMPT 1: Generate segmentation mask (image only) ---
prompt1 = "Create detailed segmentation of this image. Use flat solid colors only. Do not include any text in the produced image."

print("PROMPT 1: Requesting segmentation mask...")
response1 = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt1, im],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE']
    )
)

import io
mask_saved = False
for part in response1.parts:
    if part.inline_data is not None:
        img_data = part.inline_data.data
        mask_image = Image.open(io.BytesIO(img_data))
        print(f"  Mask is {mask_image.size}")
        if mask_image.size != (w, h):
            print(f"  Resizing to {w}x{h}")
            mask_image = mask_image.resize((w, h), Image.NEAREST)
        mask_image.save("outputs/lourmarin/segmentation_mask_v3.png")
        print(f"  Saved outputs/lourmarin/segmentation_mask_v3.png")
        mask_saved = True
        break

if not mask_saved:
    print("  ERROR: No image in response")
    exit(1)

# --- PROMPT 2: Ask about the segmentation (text only, same conversation) ---
prompt2 = """For the last segmentation map you produced, provide:
(1) The RGB color range for each segment
(2) A text description/label of each segment"""

print("\nPROMPT 2: Requesting color metadata about the segmentation...")
response2 = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        prompt1, im,          # original prompt + image
        response1.candidates[0].content,  # Gemini's mask response
        prompt2               # follow-up question
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT']
    )
)

print("\n--- Text Response ---")
text_output = ""
for part in response2.parts:
    if part.text:
        print(part.text)
        text_output += part.text + "\n"

with open("outputs/lourmarin/segmentation_metadata.txt", "w") as f:
    f.write(text_output)
print("\nSaved to outputs/lourmarin/segmentation_metadata.txt")

print("\nDone.")
