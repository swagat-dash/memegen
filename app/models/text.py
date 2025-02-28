from dataclasses import dataclass

from sanic.log import logger
from spongemock import spongemock

from .. import settings
from ..types import Dimensions, Point


@dataclass
class Text:

    style: str = "upper"
    color: str = "white"
    font: str = settings.DEFAULT_FONT

    anchor_x: float = 0.0
    anchor_y: float = 0.0

    angle: float = 0

    scale_x: float = 1.0
    scale_y: float = 0.2

    @classmethod
    def get_preview(cls) -> "Text":
        return cls(
            color="#80808060",
            anchor_x=0.075,
            anchor_y=0.05,
            angle=10,
            scale_x=0.75,
            scale_y=0.75,
        )

    @classmethod
    def get_watermark(cls) -> "Text":
        return cls(color="#FFFFFF85")

    def get_anchor(self, image_size: Dimensions, watermark: str = "") -> Point:
        image_width, image_height = image_size
        anchor = int(image_width * self.anchor_x), int(image_height * self.anchor_y)
        if watermark and self.anchor_x <= 0.1 and self.anchor_y >= 0.8:
            anchor = anchor[0], anchor[1] - settings.WATERMARK_HEIGHT // 3
        return anchor

    def get_size(self, image_size: Dimensions) -> Dimensions:
        image_width, image_height = image_size
        size = int(image_width * self.scale_x), int(image_height * self.scale_y)
        return size

    def get_stroke(self, width: int, color: str = "black") -> tuple[int, str]:
        if self.color == "black":
            width = 1
            color = "#FFFFFF85"
        elif "#" in self.color:
            width = 1
            color = "#000000" + self.color[-2:]
        return width, color

    def stylize(self, text: str, **kwargs) -> str:
        lines = [line for line in kwargs.get("lines", [text]) if line.strip()]

        if self.style == "none":
            return text

        if self.style == "default":
            text = text.capitalize() if all(line.islower() for line in lines) else text
            return text

        if self.style == "mock":
            return spongemock.mock(text, diversity_bias=0.75, random_seed=0)

        method = getattr(text, self.style or self.__class__.style, None)
        if method:
            return method()

        logger.warning(f"Unsupported text style: {self.style}")
        return text
