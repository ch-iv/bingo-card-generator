from models.card_template import CardTemplate
from paths import card_templates_path


class CardTemplatesService:
    def __init__(self):
        self.card_templates_path = card_templates_path

    def get_available_templates(self) -> list[CardTemplate]:
        templates = []

        for template_file in self.card_templates_path.glob("*.png"):
            template_name = template_file.stem.replace("_", " ").title()
            templates.append(CardTemplate(name=template_name, path=template_file))

        return templates

    def get_template_by_name(self, name: str) -> CardTemplate | None:
        for template in self.get_available_templates():
            if template.name == name:
                return template

        return None