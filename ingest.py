import re
import json
import os
from langchain_community.document_loaders import PyPDFLoader

def clean_text(text):
    # Remove source tags using double quotes to prevent syntax errors
    text = re.sub(r'\\', '', text)
    # Remove page headers
    text = re.sub(r"--- PAGE \d+ ---", "", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def semantic_split(text):
    # Regex to find "Article" (المادة)
    pattern = r"(المادة\s+[\w\d]+)"
    
    parts = re.split(pattern, text)
    chunks = []
    
    current_article = ""
    
    for part in parts:
        if "المادة" in part:
            current_article = part.strip()
        elif current_article:
            content = clean_text(part)
            if len(content) > 20:
                chunks.append(f"{current_article} : {content}")
            current_article = ""
            
    return chunks

def main():
    pdf_file = "d2c1f270-7d6e-4efb-bfe5-548e0c267781_code_travail.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"Error: PDF {pdf_file} not found.")
        return

    print("Loading PDF...")
    try:
        loader = PyPDFLoader(pdf_file)
        pages = loader.load()
        full_text = "\n".join([p.page_content for p in pages])
        
        print("Processing articles...")
        articles = semantic_split(full_text)
        
        with open("data_clean.json", "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)
            
        print(f"Success! Saved {len(articles)} articles to data_clean.json")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
