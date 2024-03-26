from PIL import Image

FILE_CHARACTER = 'char.txt'
OUTPUT_FILE = 'output.txt'
MAX_WIDTH = 100
EMPTY_CHAR = '　'
# 按像素占比的字符串
CHARACTERS = EMPTY_CHAR + '丶乁夕冘甘拐甬胃霞瞢'
# 按笔画的字符串
CHARACTERS_type2 = EMPTY_CHAR + '丶乁丫仌氺屰災泬浐紗參叅剼滲槮襂縿繠鏒齡鬖鰺戀鸂灣灤飝癴纞癵灩灪爩龖齾齉靐龘'


def get_char(r, g, b, alpha=256):
    """rgb值转字符"""
    if alpha == 0:
        return EMPTY_CHAR
    # 计算模拟灰度
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    # 翻转灰度值（使得白色为空）
    gray = 256 - gray
    # 灰度值转对应区间的字符
    length = len(CHARACTERS)
    unit = (256 + 1) / length
    return CHARACTERS[int(gray / unit)]


def image2char(image):
    """将图片转换为字符串文本"""
    img = Image.open(image)
    old_height = img.height
    old_width = img.width
    new_width = MAX_WIDTH if MAX_WIDTH < old_width else old_width
    new_height = int(old_height / old_width * new_width)
    img = img.resize((new_width, new_height))
    char_text = ''
    for i in range(img.height):
        for j in range(img.width):
            char_text += get_char(*img.getpixel((j, i)))
        char_text += '\n'

    return char_text


def main():
    while True:
        print('-' * 50)
        image = input('输入图片路径：')
        # 转字符串文本
        char_text = image2char(image)
        # 字符画输出到本地文件
        print(char_text)
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(char_text)


if __name__ == '__main__':
    main()
