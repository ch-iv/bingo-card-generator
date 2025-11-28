from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename, send_from_directory

from paths import card_templates_path, web_assets_path, generated_cards_path
from services.addons.warm_and_fuzzy_addon import WarmAndFuzzyAddon
from services.card_templates_service import CardTemplatesService
from services.cell_content.cell_content_generator import CellContentGenerator
from services.cell_content.definitions.american_bingo_cell_content_definition import AmericanBingoCellContentDefinition
from services.detect_image_cells_service import DetectImageCellsService
from services.fill_bingo_card_service import FillBingoCardService
from services.base_64_encode_file_service import Base64EncodeFileService
from services.file_identity_service import FileIdentityService
from services.file_save_service import FileSaveService


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = "uploads"
    FileIdentityService.startup_hook()

    @app.route("/", methods=["GET", "POST"])
    def template_upload():
        # card_templates = list(map(
        #     lambda p: p.relative_to(generated_cards_path),
        #     card_templates_path.iterdir()
        # ))

        card_templates = CardTemplatesService().get_available_templates()

        return render_template(
            "template_upload.html.jinja2",
            card_templates=card_templates
        )

    @app.route("/pre-fill-template")
    def pre_fill_template():
        card_template_name = request.args.get("card_template")
        card_template = CardTemplatesService().get_template_by_name(card_template_name)

        return render_template(
            "pre_fill_template.html.jinja2",
            card_template=card_template
        )

    @app.route("/bingo-template-upload", methods=["POST"])
    def upload_bingo_template():
        if "bingo-card-template" not in request.files:
            return "No file", 400

        template = request.files["bingo-card-template"]
        template_name = secure_filename(template.filename or "")
        template_id = FileSaveService.call(template, template_name)

        return redirect(url_for("measure_template", template_id=template_id))

    @app.post("/fill-card")
    def fill_card():
        card_template_name = request.json.get("card_template")
        card_template = CardTemplatesService().get_template_by_name(card_template_name)

        cells = DetectImageCellsService.call(card_template.path)
        generator = CellContentGenerator(AmericanBingoCellContentDefinition())
        result = FillBingoCardService.call(card_template.path, cells, generator)
        return jsonify({"card": str(result.relative_to(generated_cards_path))})

    @app.route("/filled-card/<path:card>")
    def filled_card(card):
        return send_from_directory(generated_cards_path, card, request.environ)

    return app
