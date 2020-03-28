import os

from darktower.constants.dt_color import DTColor
from darktower.views.base_view import FONTS

DEFAULT_FONT = os.path.join(FONTS, 'Roboto-Regular.ttf')
CLOCK_FONT = os.path.join(FONTS, 'alarm clock.ttf')
DEFAULT_FONT_SIZE = 35
DEFAULT_FONT_COLOR = DTColor.BLACK