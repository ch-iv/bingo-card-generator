from pathlib import Path

file_save_path = Path(__file__).parent / "runtime" / "uploads"
if not file_save_path.exists():
    file_save_path.mkdir(parents=True, exist_ok=True)

file_identity_db_path = Path(__file__).parent / "runtime" / "file_identity.db"
generated_cards_path = Path(__file__).parent / "runtime" / "generated_cards"
fonts_path = Path(__file__).parent / "web" / "static" / "fonts"
card_templates_path = Path(__file__).parent / "web" / "static" / "card_templates"
web_assets_path = Path(__file__).parent / "web"