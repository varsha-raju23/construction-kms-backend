from flask import Blueprint, request, jsonify
from services.storage_service import upload_file
from services.cosmos_service import save_document

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/document", methods=["POST"])
def upload_document():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "File name is empty"}), 400

        upload_result = upload_file(file)

        document_data = {
            "title": request.form.get("title", ""),
            "description": request.form.get("description", ""),
            "category": request.form.get("category", ""),
            "project_name": request.form.get("project_name", ""),
            "tags": request.form.get("tags", "").split(","),
            "file_name": upload_result["file_name"],
            "file_url": upload_result["file_url"],
            "extracted_text": ""
        }

        document_id = save_document(document_data)

        return jsonify({
            "success": True,
            "document_id": document_id,
            "file_url": upload_result["file_url"]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500