import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip

def ticker(text, duration=3, width=100, height=100):
    def make_frame(t):
        img = Image.new("RGB", (width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Загружаем шрифт
        font_size = int(height / 2)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Считаем позицию
        text_width, text_height = draw.textsize(text, font=font)
        x = width - (width + text_width) * t / duration
        y = (height - text_height) // 2

        # Рисуем текст
        draw.text((x, y), text, font=font, fill=(255, 255, 255))

        return np.array(img)

    # Создаём видео
    video = VideoClip(make_frame, duration=duration)
    
    # Устанавливаем частоту кадров в секунду
    video = video.set_fps(30)
    
    # Записываем результат
    video.write_videofile("ticker.mp4", codec="libx264")

if __name__ == "__main__":
    user_text = input("Введите ваш текст: ")
    ticker(user_text)