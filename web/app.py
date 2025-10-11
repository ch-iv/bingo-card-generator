from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from services.base_64_encode_file_service import Base64EncodeFileService
from services.file_identity_service import FileIdentityService
from services.file_save_service import FileSaveService


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = "uploads"
    FileIdentityService.startup_hook()

    @app.route("/", methods=["GET", "POST"])
    def template_upload():
        return render_template("template_upload.html.jinja2")

    @app.route("/bingo-template-upload", methods=["POST"])
    def upload_bingo_template():
        if "bingo-card-template" not in request.files:
            return "No file", 400

        template = request.files["bingo-card-template"]
        template_name = secure_filename(template.filename or "")
        template_id = FileSaveService.call(template, template_name)

        return redirect(url_for("measure_template", template_id=template_id))

    @app.route("/measure-template")
    def measure_template():
        template_id = request.args.get("template_id")

        if not (template_path := FileIdentityService.lookup(template_id)):
            return "Template not found", 404

        base64_template_image_data = Base64EncodeFileService.call(template_path)

        return render_template(
            "measure_template.html.jinja2",
            base64_template_image_data=base64_template_image_data,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
