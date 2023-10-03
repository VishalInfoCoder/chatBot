from flask import Blueprint, send_from_directory

# Create a Blueprint for static files
static_bp = Blueprint('static', __name__)

@static_bp.route('/assets/images/<path:filename>')
def serve_static(filename):
    return send_from_directory('assets/images', filename)