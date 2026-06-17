from flask import Flask
from flask_cors import CORS

from routes.upload import upload_bp
from routes.search import search_bp
from routes.chat import chat_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(upload_bp, url_prefix="/api/upload")
app.register_blueprint(search_bp, url_prefix="/api/search")
app.register_blueprint(chat_bp, url_prefix="/api/chat")

@app.route("/")
def home():
    return {"message": "Construction KMS Backend Running"}

if __name__ == "__main__":
    app.run(debug=True, port=8080)