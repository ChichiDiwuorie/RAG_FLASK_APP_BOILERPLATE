from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)

# Azure configuration
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")
OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")
AZ_SEARCH_API_VERSION = "2021-04-30-Preview"
AZ_OPENAI_CHAT_API_VER = "2023-03-15-preview"

def check_configuration():
    """Check if all required Azure configurations are present"""
    configs = {
        "Azure Search Endpoint": SEARCH_ENDPOINT,
        "Azure Search Key": SEARCH_KEY,
        "Azure Search Index": SEARCH_INDEX,
        "Azure OpenAI Endpoint": OPENAI_ENDPOINT,
        "Azure OpenAI Key": OPENAI_KEY,
        "Azure OpenAI Deployment": OPENAI_DEPLOYMENT
    }
    
    status = {}
    all_configured = True
    
    for name, value in configs.items():
        if value:
            status[name] = {"status": "✅ Configured", "class": "success"}
        else:
            status[name] = {"status": "❌ Missing", "class": "error"}
            all_configured = False
    
    return status, all_configured

@app.route('/')
def index():
    print('Request for index page received')
    config_status, all_configured = check_configuration()
    return render_template('index.html', 
                         config_status=config_status, 
                         all_configured=all_configured)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)