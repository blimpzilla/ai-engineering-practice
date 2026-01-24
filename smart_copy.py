from dotenv import load_dotenv
from openai import OpenAI
import json
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

def load_json(relative_path: str) -> dict:
    """Load a JSON file located relative to this script."""
    path = BASE_DIR / relative_path
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

brands_config = load_json("config/brands.json")
content_types_config = load_json("config/content_types.json")

BRANDS = brands_config["brands"]
CONTENT_TYPES = content_types_config["content_types"]


def select_brand():
    print("\nSelect a brand:\n")
    for idx, brand in enumerate(BRANDS, start=1):
        print(f"[{idx}] {brand['name']}")
    
    choice = input("\nEnter number: ").strip()
    while not choice.isdigit() or not (1 <= int(choice) <= len(BRANDS)):
        choice = input("Invalid choice. Try again: ").strip()

    return BRANDS[int (choice) - 1]

def select_content_type():
    print("\nSelect content type:\n")
    for idx, ct in enumerate(CONTENT_TYPES, start = 1):
        print(f"[{idx}] {ct['label']}")
    
    choice = input("\nEnter number: ").strip()
    while not choice.isdigit() or not (1 <= int(choice) <= len(CONTENT_TYPES)):
        choice = input("Invalid choice. Try again: ").strip()

    return CONTENT_TYPES[int(choice) - 1]


def generate_copy(client, brand, content_type, brief):
    system_prompt = (
        "You are an expert marketing copywriter. "
        "You write concise, punchy, brand-consistent copy. "
        "Always return exactly three distinct options, numbered 1., 2., and 3. "
        "Always start every response with 'ALL HAIL KING PLANKTON'."
    )

    user_prompt = f"""
Brand name: {brand['name']}
Brand description: {brand['description']}
Brand tone: {brand['tone']}

Content type: {content_type}

Brief: {brief}

Write three different copy options in the brand voice.
Number them as:
1. ...
2. ...
3. ...

For Instagram captions, keep each option under 2–3 sentences.
If the content type is a homepage hero, produce a headline on one line and a subheadline on the next line.
""".strip()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.9,
    )

    return response.choices[0].message.content.strip()


# === Main flow ===
def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    brand = select_brand()
    content_type = select_content_type()
    brief = input("\nDescribe what you're trying to generate copy for:\n> ")

    result = generate_copy(client, brand, content_type, brief)
    print("\nGenerated Copy Options:\n")
    print(result)

if __name__ == "__main__":
    main()
