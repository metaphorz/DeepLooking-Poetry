"""
Generate poem-inspired images for The Mouth of the Lourmarin River (Guigou, 1867).
Each region gets an image generated from its poem excerpt.
"""
import os, io
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

poems = {
    "sky": """Thou on whose stream, mid the steep sky's commotion,
Loose clouds like earth's decaying leaves are shed,
Shook from the tangled boughs of Heaven and Ocean,""",

    "trees": """Poems are made by fools like me,
But only God can make a tree.""",

    "cliffs": """a huge Cliff,
As if with voluntary power instinct,
Upreared its head. I struck, and struck again,
And, growing still in stature, the huge cliff
Rose up between me and the stars, and still
With measured motion, like a living thing,
Strode after me.""",

    "meadow": """In the soft light couples pass,
Families wander, all serene.
On the horizon, over there,
Is Saint Louis' dusty keep;
High above the joyful affair,
The sun dazzles; meadows sleep.""",

    "river": """It is a green hollow where a river sings
Madly catching on the grasses
Silver rags; where the sun shines from the proud mountain:
It is a small valley which bubbles over with rays.""",

    "waterfall": """Sunlight streaming on Incense Stone kindles violet smoke;
far off I watch the waterfall plunge to the long river,
flying waters descending straight three thousand feet,
till I think the Milky Way has tumbled from the ninth height of Heaven.""",

    "travelers": """But the true travelers are those who go
Only to get away: hearts like balloons,
They never turn aside from their fatality
And without knowing why they always say: "Let's go!\"""",

    "bird": """A Bird came down the Walk —
He did not know I saw —
He bit an Angleworm in halves
And ate the fellow, raw,"""
}

print("Generating poem-inspired images for Lourmarin River...")
for keyword, poem_text in poems.items():
    outpath = f"images/lourmarin/lourmarin_{keyword}.png"
    prompt = f"Create a painterly artistic illustration inspired by this poem. Do not include any text in the produced image.\n{poem_text}"
    print(f"  Generating image for '{keyword}'...")
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE']
            )
        )
        for part in response.parts:
            if part.inline_data is not None:
                img_data = part.inline_data.data
                poem_img = Image.open(io.BytesIO(img_data))
                poem_img.save(outpath)
                print(f"  Saved {outpath}")
                break
        else:
            print(f"  No image in response for {keyword}")
    except Exception as e:
        print(f"  Error generating {keyword}: {e}")

print("\nDone. Poem images saved to images/lourmarin/")
