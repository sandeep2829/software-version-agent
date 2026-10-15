import csv
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import getpass

load_dotenv()
client = genai.Client()

def check_latest_versions():
    csv_file = "requiredsoftwares.csv"
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} file not found!")
        return

    softwares = []
    with open(csv_file, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if any(row.values()):
                softwares.append(row)

    if not softwares:
        print("Error: No data found in the CSV file!")
        return

    # Utilizing model tools configuration for live web retrieval
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""Find the latest versions and official 
        download URLs for: {softwares}. Return as a markdown table with 
        columns: sno, name, version, url. with Structured tabular format and dont show any other details""",
        config=types.GenerateContentConfig(
            tools=[{"google_search": {}}]
        ),
    )

    print("\n" + response.text.strip())
    
def get_autherName():
    fileCreayedBy = getpass.getuser()
    print(f"File created by: {fileCreayedBy}")

if __name__ == "__main__":
    check_latest_versions()
    get_autherName()