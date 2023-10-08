from PIL import Image
from colorama import init, Style
import argparse

# Инициализация библиотеки colorama для цветного вывода
init(autoreset=True)

parser = argparse.ArgumentParser(description='Конвертер изображения в цветной ASCII art с BBCode.')
parser.add_argument('input_image', help='Путь к входному изображению')
parser.add_argument('--diff', type=int, default=49, help='На сколько искать разницу в пикселях')
args = parser.parse_args()

# Загрузка изображения

img = Image.open(args.input_image)

# Максимальная ширина строки в символах (без учета bbcode)
max_width = 40
max_height = 26

# Символ, из которого будет строиться ASCII-арт
ascii_char = '█'

# Функция для преобразования цвета HEX в ANSI код цвета
def hex_to_ansi(hex_color):
    return f"\033[38;2;{int(hex_color[1:3], 16)};{int(hex_color[3:5], 16)};{int(hex_color[5:7], 16)}m"

# Ограничение на количество символов в текстовом файле с учетом табуляций и строк bbcode
max_chars = 5000

# Получение размеров изображения
width, height = img.size

# Рассчитываем коэффициент масштабирования для соответствия максимальной ширине
scale_factor = max_width / width
hscale_factor = max_height / height

# Масштабируем изображение
new_width = int(width * scale_factor)
new_height = int(height * hscale_factor)
img = img.resize((new_width, new_height))

# Открываем файл для записи ASCII-арта с BBCode и цветами HEX
output_file_bbcode = 'ascii_art_with_bbcode.txt'

# Открываем файл для записи ASCII-арта с цветами, которые выводятся в окне PowerShell
output_file_powershell_colors = 'ascii_art_with_powershell_colors.txt'

# Создаем список строк для хранения строк ASCII-арта с BBCode и цветами HEX
ascii_lines_bbcode = []
ascii_lines_powershell_colors = []

# Предел разницы цветов для объединения символов
color_difference_threshold = args.diff

# Цикл по пикселям изображения
for y in range(new_height):
    line_bbcode = ''
    line_powershell_colors = ''
    prev_hex_color = None  # Хранит предыдущий цвет символа
    prev_char = None  # Хранит предыдущий символ
    for x in range(new_width):
        pixel = img.getpixel((x, y))
        hex_color = "#{:02x}{:02x}{:02x}".format(*pixel[:3])

        # Если цвет символа изменился, добавляем цвет в формате HEX с помощью BBCode
        if prev_char is not None:
            if prev_hex_color is not None and (
                abs(int(prev_hex_color[1:3], 16) - int(hex_color[1:3], 16)) <= color_difference_threshold and
                abs(int(prev_hex_color[3:5], 16) - int(hex_color[3:5], 16)) <= color_difference_threshold and
                abs(int(prev_hex_color[5:7], 16) - int(hex_color[5:7], 16)) <= color_difference_threshold
            ):
                line_bbcode += ascii_char
                line_powershell_colors += ascii_char
            else:
                if len(line_bbcode) + len(ascii_char) + len(hex_color) + len("[/color]") <= max_chars:
                    line_bbcode += f"[color={hex_color}]{ascii_char}"
                if len(line_powershell_colors) + len(ascii_char) + len(hex_color) + len(Style.RESET_ALL) <= max_chars:
                    line_powershell_colors += hex_to_ansi(hex_color) + ascii_char

        # Если символ первый в строке, добавляем его без сравнения
        else:
            if len(line_bbcode) + len(ascii_char) + len(hex_color) + len("[/color]") <= max_chars:
                line_bbcode += f"[color={hex_color}]{ascii_char}"
            if len(line_powershell_colors) + len(ascii_char) + len(hex_color) + len(Style.RESET_ALL) <= max_chars:
                line_powershell_colors += hex_to_ansi(hex_color) + ascii_char

        prev_char = ascii_char
        prev_hex_color = hex_color

    # Добавляем закрывающую команду [/color] в BBCode строку

    ascii_lines_bbcode.append(line_bbcode)
    ascii_lines_powershell_colors.append(line_powershell_colors)

# Сохраняем цветной ASCII-арт с BBCode и цветами HEX в файл
with open(output_file_bbcode, 'w', encoding='utf-8') as f:
    for line in ascii_lines_bbcode:
        f.write(line + '\n')



# Выводим ASCII-арт с цветами, которые выводятся в окне PowerShell
for line in ascii_lines_powershell_colors:
    print(line)

# Сохраняем ASCII-арт с цветами, которые выводятся в окно PowerShell, в файл
with open(output_file_powershell_colors, 'w', encoding='utf-8') as f:
    for line in ascii_lines_powershell_colors:
        f.write(line + '\n')

print(f'Цветной ASCII-арт с BBCode и цветами HEX сохранен в файл {output_file_bbcode}')

# Открываем файл для чтения (замените 'file.txt' на путь к вашему файлу)
with open(output_file_bbcode, 'r', encoding='utf-8') as file:
    # Читаем содержимое файла в строку
    text = file.read()

# Считаем количество символов в строке
character_count = len(text)

# Выводим результат
if character_count >= 5000:
    print(f'Количество символов в файле: {character_count}. Может не вставиться в бумагу. Попробуй увеличить шакальство')
else:
    print(f'Количество символов в файле: {character_count}. Должно быть ок')
