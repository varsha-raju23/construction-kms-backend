from flask import Blueprint, request, jsonify
from services.cosmos_service import search_documents, get_document

search_bp = Blueprint("search", __name__)


@search_bp.route("/documents", methods=["GET"])
def search_all_documents():
    try:
        keyword = request.args.get("keyword", "")
        category = request.args.get("category", "")

        results = search_documents(keyword, category)

        return jsonify({
            "success": True,
            "count": len(results),
            "documents": results
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@search_bp.route("/document/<document_id>", methods=["GET"])
def get_single_document(document_id):
    try:
        document = get_document(document_id)

        if not document:
            return jsonify({
                "success": False,
                "error": "Document not found"
            }), 404

        return jsonify({
            "success": True,
            "document": document
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500