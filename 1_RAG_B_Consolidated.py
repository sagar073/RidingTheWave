import os
import requests
import fitz  # PyMuPDF
import numpy as np
import mysql.connector
import tiktoken
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
#from langchain.runnables import RunnableSequence  # Updated import for RunnableSequence
from keybert import KeyBERT
import re

# === 1️⃣ Setup OpenAI API Key ===
#os.environ["OPENAI_API_KEY"] = "Open_API_key"  # Replace with actual OpenAI API key

# === 2️⃣ Flask App Setup ===
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for frontend access

# === 3️⃣ Tokenization Helpers ===
def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))

def truncate_text(text, max_tokens=4000):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    return encoding.decode(tokens[:max_tokens])

# === 4️⃣ Web Scraping (Requests & BeautifulSoup) ===
def scrape_webpage(url):
    try:
        headers = {'User-Agent': 'Chrome/129.0.0.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = ' '.join([p.get_text() for p in soup.find_all('p')])  # Extract all paragraph text
        return truncate_text(text.strip(), 4000)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# === 5️⃣ PDF Text Extraction ===
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text")
        return truncate_text(text.strip(), 4000)
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

# === 6️⃣ SDG Classification using LangChain ===
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
sdg_prompt = PromptTemplate.from_template(
    """Analyze the following text and determine which of the 17 UN Sustainable Development Goals (SDGs) it aligns with. 
    Provide the goal number, goal name, and a short explanation within 20 words. Give details of all the SDG goals mentioned in the text. Do not left any of the goal which is mentioned.\n\nText: {text}"""
)

# Updated to use RunnableSequence
classification_chain = sdg_prompt | llm

def classify_sdg(text):
    truncated_text = truncate_text(text, 4000)
    response = classification_chain.invoke({"text": truncated_text})
    # Use regular expression to extract content part after 'content='
    match = re.search(r"content='(.*?)'", str(response))
    if match:
        sdg_result_text = match.group(1)  # Extract the content between 'content=' and the closing quote
    else:
        sdg_result_text = "No content found"  # Default if no match is found
    return sdg_result_text

# === 7️⃣ Keyword Extraction using KeyBERT ===
kw_model = KeyBERT()

def extract_keywords(text):
    return [kw[0] for kw in kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)]

# === 8️⃣ Text Embedding (OpenAI) ===
embedding_model = OpenAIEmbeddings()

def generate_embedding(text):
    truncated_text = truncate_text(text, 8000)
    return np.array(embedding_model.embed_query(truncated_text))

# === 9️⃣ MySQL Database Integration ===
conn = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="password",  
    database="sdg_tracking"
)
cursor = conn.cursor()


def store_classification(text, keywords, sdg_result):
    sql = "INSERT INTO sdg_results (text, keywords, sdg_classification) VALUES (%s, %s, %s)"
    values = (text, ', '.join(keywords), sdg_result)
    cursor.execute(sql, values)
    conn.commit()
    print("\n✅ Classification stored in MySQL database.")


def retrieve_classifications():
    cursor.execute("SELECT sdg_classification FROM sdg_results where id in (select max(id) from sdg_results)")
    return cursor.fetchall()

# === 10️⃣ Flask Routes ===
@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    web_text = scrape_webpage(url)
    if not web_text:
        return jsonify({"error": "Failed to fetch the webpage"}), 500
    
    return jsonify({"extracted_text": web_text}), 200

@app.route('/classify', methods=['POST'])
def classify():
    input_text = request.json.get('text')
    if not input_text:
        return jsonify({"error": "Text is required for classification"}), 400

    classification_result = classify_sdg(input_text)
    return jsonify({"classification_result": classification_result}), 200

@app.route('/extract_keywords', methods=['POST'])
def extract_keywords_route():
    input_text = request.json.get('text')
    if not input_text:
        return jsonify({"error": "Text is required for keyword extraction"}), 400

    keywords = extract_keywords(input_text)
    return jsonify({"keywords": keywords}), 200

@app.route('/store_classification', methods=['POST'])
def store_classification_route():
    input_text = request.json.get('text')
    keywords = request.json.get('keywords')
    sdg_result = request.json.get('sdg_result')

    if not input_text or not keywords or not sdg_result:
        return jsonify({"error": "Text, keywords, and SDG result are required"}), 400

    store_classification(input_text, keywords, sdg_result)
    return jsonify({"message": "Classification stored successfully"}), 200

@app.route('/retrieve_classifications', methods=['GET'])
def retrieve_classifications_route():
    stored_data = retrieve_classifications()
    return jsonify({"stored_data": stored_data}), 200


@app.route('/analyze', methods=['GET'])
def analyze_page():
    return '''
        <html>
            <head>
                <title>Analyze URL or PDF</title>
            </head>
            <body>
                <h1>Analyze URL or Upload PDF</h1>
                <form action="/analyze" method="POST" enctype="multipart/form-data">
                    <label for="url">Enter URL:</label><br>
                    <input type="text" id="url" name="url" placeholder="Enter URL"><br><br>
                    
                    <label for="pdf">Upload PDF:</label><br>
                    <input type="file" id="pdf" name="pdf" accept=".pdf"><br><br>

                    <input type="submit" value="Analyze">
                </form>
            </body>
        </html>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    pdf_file = request.files.get('pdf')
    extracted_text = None

    if url:
        extracted_text = scrape_webpage(url)
    elif pdf_file:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)  # Ensure upload directory exists

        pdf_path = os.path.join(upload_dir, pdf_file.filename)
        pdf_file.save(pdf_path)

        extracted_text = extract_text_from_pdf(pdf_path)
        os.remove(pdf_path)  # Delete file after processing

    # **✅ Fix: Check if extracted_text is valid**
    if not extracted_text:
        return jsonify({"error": "No text extracted from the URL or PDF"}), 400

    # Process classification
    sdg_result = classify_sdg(extracted_text)
    keywords = extract_keywords(extracted_text)
    store_classification(extracted_text, keywords, sdg_result)

    # Retrieve latest results
    stored_data = retrieve_classifications()

    # Return response as an HTML page
    return f'''
        <html>
            <body>
                <h1>Analysis Results</h1>
                <h2>Extracted Text:</h2>
                <p>{truncate_text(extracted_text, 400)}</p>
                <h2>Keywords:</h2>
                <p>{', '.join(keywords)}</p>
                <h2>SDG Classification:</h2>
                <p>{sdg_result}</p>
                <h2>Stored Data:</h2>
                <p>{stored_data}</p>
                <br><br>
                <a href="/analyze">Back to Analyze</a>
            </body>
        </html>
    '''




# === 11️⃣ Run Flask App ===
if __name__ == '__main__':
    app.run(debug=True)
