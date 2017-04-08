# Based on: https://github.com/embeddedartists/gratis/blob/cd84c4497093a96bc41517e1f1b87f5a8c5ca6a6/PlatformWithOS/demo/Clock27.py
import sys
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import time
from EPD import EPD

WHITE = 1
BLACK = 0

# fonts are in different places on Raspbian/Angstrom so search
possible_fonts = [
    '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',            # Debian B.B
    '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf',   # Debian B.B
    '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono-Bold.ttf',   # R.Pi
    '/usr/share/fonts/truetype/freefont/FreeMono.ttf',                # R.Pi
    '/usr/share/fonts/truetype/LiberationMono-Bold.ttf',              # B.B
    '/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf',              # B.B
    '/usr/share/fonts/TTF/FreeMonoBold.ttf',                          # Arch
    '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf'                        # Arch
]


FONT_FILE = ''
for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break

if '' == FONT_FILE:
    raise 'no font file found'

CLOCK_FONT_SIZE = 100
DATE_FONT_SIZE  = 42
WEEKDAY_FONT_SIZE  = 42

# time
X_OFFSET = 5
Y_OFFSET = 3
COLON_SIZE = 5
COLON_GAP = 10

# date
DATE_X = 10
DATE_Y = 90

WEEKDAY_X = 10
WEEKDAY_Y = 130

DAYS = [
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
    "SUNDAY"
]

def main(argv):
    """main program - draw HH:MM clock on 2.70" size panel"""

    epd = EPD()

    print('panel = {p:s} {w:d} x {h:d}  version={v:s}  cog={g:d}'.format(p=epd.panel, w=epd.width, h=epd.height, v=epd.version, g=epd.cog))

    if 'EPD 2.7' != epd.panel:
        print('incorrect panel size')
        sys.exit(1)

    epd.clear()

    demo(epd)


def demo(epd):
    """simple partial update demo - draw draw a clock"""

    # initially set all white background
    image = Image.new('1', epd.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    width, height = image.size

    clock_font = ImageFont.truetype(FONT_FILE, CLOCK_FONT_SIZE)
    date_font = ImageFont.truetype(FONT_FILE, DATE_FONT_SIZE)
    weekday_font = ImageFont.truetype(FONT_FILE, WEEKDAY_FONT_SIZE)

    # clear the display buffer
    draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
    previous_day = 0

    first_start = True

    while True:
        while True:
            now = datetime.today()
            if now.second == 0 or first_start:
                first_start = False
                break
            time.sleep(0.5)

        if now.day != previous_day:
            # draw.rectangle((1, 1, width - 1, height - 1), fill=WHITE, outline=BLACK)
            # draw.rectangle((2, 2, width - 2, height - 2), fill=WHITE, outline=BLACK)
            draw.text((DATE_X, DATE_Y), '{y:04d}-{m:02d}-{d:02d}'.format(y=now.year, m=now.month, d=now.day), fill=BLACK, font=date_font)
            draw.text((WEEKDAY_X, WEEKDAY_Y), '{w:s}'.format(w=DAYS[now.weekday()]), fill=BLACK, font=weekday_font)
            previous_day = now.day
        else:
            draw.rectangle((X_OFFSET, Y_OFFSET, width - X_OFFSET, DATE_Y - 1), fill=WHITE, outline=WHITE)

        #draw.text((X_OFFSET, Y_OFFSET), '{h:02d}:{m:02d}'.format(h=now.hour, m=now.minute), fill=BLACK, font=clock_font)

        # draw.text((X_OFFSET, Y_OFFSET), '{h:02d}'.format(h=now.hour), fill=BLACK, font=clock_font)

        # colon_x1 = width / 2 - COLON_SIZE
        # colon_x2 = width / 2 + COLON_SIZE
        # colon_y1 = CLOCK_FONT_SIZE / 2 + Y_OFFSET - COLON_SIZE
        # colon_y2 = CLOCK_FONT_SIZE / 2 + Y_OFFSET + COLON_SIZE
        # draw.rectangle((colon_x1, colon_y1 - COLON_GAP, colon_x2, colon_y2 - COLON_GAP), fill=BLACK, outline=BLACK)
        # draw.rectangle((colon_x1, colon_y1 + COLON_GAP, colon_x2, colon_y2 + COLON_GAP), fill=BLACK, outline=BLACK)

        # draw.text((X_OFFSET + width / 2, Y_OFFSET), '{m:02d}'.format(m=now.minute), fill=BLACK, font=clock_font)

        # display image on the panel
        epd.display(image)
        epd.update()

# main
if "__main__" == __name__:
    if len(sys.argv) < 1:
        sys.exit('usage: {p:s}'.format(p=sys.argv[0]))

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass