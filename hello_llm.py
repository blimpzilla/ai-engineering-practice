from dotenv import load_dotenv
import os
from openai import OpenAI

def main():
    # Load .env values into environment variables
    load_dotenv()

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Ask user for input
    brief = input("Describe what you want copy for: ")

    # Make API call to generate text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative marketing copywriter."},
            {"role": "user", "content": f"Write 3 short headline ideas for: {brief}"}
        ]
    )

    # Print result
    print("\nGenerated copy:\n")
    print(response.choices[0].message.content.strip())

if __name__ == "__main__":
    main()
