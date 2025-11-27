from PIL import Image, ImageDraw, ImageFont
import textwrap

from paths import fonts_path


def draw_text_in_rectangle(
    image: Image.Image,
    text,
    rect_x,
    rect_y,
    rect_width,
    rect_height,
    font_size=60,
    text_color="black",
):
    draw = ImageDraw.Draw(image)

    current_font_size = font_size

    while current_font_size > 8:
        font = ImageFont.truetype(fonts_path / "lora.ttf", font_size)

        test_char = "A"
        char_width = draw.textbbox((0, 0), test_char, font=font)[2]
        chars_per_line = max(1, rect_width // char_width)

        wrapped_lines = []
        words = text.split()
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            line_width = draw.textbbox((0, 0), test_line, font=font)[2]

            if line_width <= rect_width:
                current_line = test_line
            else:
                if current_line:
                    wrapped_lines.append(current_line)
                    current_line = word
                else:
                    wrapped_lines.extend(textwrap.wrap(word, width=chars_per_line))
                    current_line = ""

        if current_line:
            wrapped_lines.append(current_line)

        line_height = draw.textbbox((0, 0), "A", font=font)[3] + 2
        total_text_height = len(wrapped_lines) * line_height

        if total_text_height <= rect_height:
            break

        current_font_size -= 2

    start_y = rect_y + (rect_height - total_text_height) // 2

    for i, line in enumerate(wrapped_lines):
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_width = line_bbox[2] - line_bbox[0]

        x = rect_x + (rect_width - line_width) // 2
        y = start_y + i * line_height

        draw.text(
            (x, y),
            line,
            fill="white",
            font=font,
            stroke_width=7,
            stroke_fill="black",
        )

    return image
