import json
import mimetypes
import os
import time
import tempfile
from django.utils.encoding import smart_str
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from moviepy.editor import TextClip, VideoClip
from PIL import Image, ImageDraw, ImageFont

from .forms import TextForm

# Create your views here.


def ticker_app(text):
    """Приложение бегущей строки"""
    duration = 3
    width = 100
    height = 100

    def make_frame(t):
        """Создаёт один кадр"""
        img = Image.new("RGB", (width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Загружаем шрифт
        font_size = int(height / 2)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Рассчитываем положение текста
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

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        output_path = temp_video.name
        video.write_videofile(output_path, fps=30, codec="libx264")

    with open(output_path, "rb") as fs:
        response = HttpResponse(
            fs.read(), content_type=mimetypes.guess_type(output_path)[0]
        )
        response["Content-Disposition"] = "attachment; filename=%s" % smart_str(
            "output.mp4"
        )
        time.sleep(10)

        return response


def index(request):
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            return ticker_app(text)
    else:
        form = TextForm()

    return render(request, "main/index.html", {"form": form})
