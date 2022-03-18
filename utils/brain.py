import random
from enum import Enum
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import InputFile, InputMediaPhoto
from io import BytesIO


class Difficult(Enum):
    easy = 5
    medium = 7
    hard = 9


colors = ['cadetblue', 'sienna', 'brown', 'violet', 'red', 'green',
          'rebeccapurple', 'rosybrown', 'maroon', 'orange', 'midnightblue']
BASE_SIZE = 100


async def brain_make(difficult):
    number_count = Difficult[difficult].value
    size = int(BASE_SIZE * number_count)
    img = Image.new(mode='RGB', size=(size,size), color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('fonts/K2D-Medium.TTF', size=25)
    rl = list(range(1,number_count**2 +1))
    random.shuffle(rl)
    numbers = list(rl)

    for i in range(1, number_count):
        x = int(BASE_SIZE * i)
        draw.line((x, 0, x, size), width=3, fill='black')
        draw.line((0, x, size, x), width=3, fill='black')

    for x in range(number_count):
        for y in range(number_count):
            number = str(numbers.pop(0))
            w, h = draw.textsize(number, font=font)
            X = x * BASE_SIZE + (BASE_SIZE - w)/2
            Y = y * BASE_SIZE + (BASE_SIZE - h)/2
            color = random.choice(colors)
            draw.text((X,Y), number, fill=color, align='center', font=font)

    bytes_img = BytesIO()
    img.save(bytes_img, format='PNG')
    bytes_img.seek(0)
    image = InputFile(bytes_img)
    return image
