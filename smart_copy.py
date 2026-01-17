from dotenv import load_dotenv
from openai import OpenAI
import os

BRANDS = {
	"1": {
		"name": "God's Country",
		"description": "Clothing brand rooted in rebellion, isolation, and rugged beauty. Visual language blends Americana, biker, trailer park, and trashy motifs.",
		"tone": "Rebelious, trashy, rugged, anti-pretentious"
	},
}

CONTENT_TYPES = {
	"1": "Homepage hero: Heading & Subheadline",
	"2": "Instagram caption",
	"3": "Short tagline"
}


def select_brand():
    print("\nSelect a brand:\n")
    for key, data in BRANDS.items():
        print(f"[{key}] {data['name']}")
    
    choice = input("\nEnter number: ").strip()
    while choice not in BRANDS:
        choice = input("Invalid choice. Try again: ").strip()

    return BRANDS[choice]

def select_content_type():
    print("\nSelect content type:\n")
    for key, label in CONTENT_TYPES.items():
        print(f"[{key}] {label}")
    
    choice = input("\nEnter number: ").strip()
    while choice not in CONTENT_TYPES:
        choice = input("Invalid choice. Try again: ").strip()

    return CONTENT_TYPES[choice]


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
