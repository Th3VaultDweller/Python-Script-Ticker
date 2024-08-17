from django import forms

class TextForm(forms.Form):
    text = forms.CharField(label='Введите текст для генерации видео', max_length=200)