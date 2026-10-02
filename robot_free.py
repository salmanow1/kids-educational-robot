import os
from gtts import gTTS
from moviepy.editor import ColorClip, AudioFileClip, TextClip, CompositeVideoClip

# قاموس الحلقات اليومي: الحرف، والكلمة بالعربية، واللون المفضل للخلفية
CHANNELS_DATA = {
    1: {"char": "أ", "word_ar": "أَسَد", "bg_color": (255, 111, 97)},    # لون مرجاني حيوي
    2: {"char": "ب", "word_ar": "بَطَّة", "bg_color": (74, 144, 226)},   # لون أزرق لطيف
    3: {"char": "ت", "word_ar": "تِمْسَاح", "bg_color": (80, 227, 194)},  # لون فيروزي مهدئ
    4: {"char": "و", "word_ar": "وَلَد", "bg_color": (245, 166, 35)},    # لون برتقالي دافئ
}

def build_multilang_video(episode_number):
    data = CHANNELS_DATA.get(episode_number)
    if not data:
        print("🏁 تم إنهاء السلسلة بالكامل!")
        return

    char = data["char"]
    word_ar = data["word_ar"]
    bg_color = data["bg_color"]

    # 1. توليد الصوت والنطق النحوي بالتشكيل
    arabic_speech = f"حرف {char}. {char} فتحة. {word_ar}."
    english_speech = f"Follow Salmano channel for more updates!"
    full_speech = f"{arabic_speech} ... {english_speech}"

    print("🔊 جاري توليد الصوت البشري بالتشكيل...")
    tts = gTTS(text=full_speech, lang='ar', slow=False)
    audio_path = "temp_voice.mp3"
    tts.save(audio_path)

    # 2. تحميل الصوت وتوليد الخلفية الملونة برمجياً بالأبعاد الرأسية 1080x1920
    audio_clip = AudioFileClip(audio_path)
    video_duration = audio_clip.duration
    
    # توليد شاشة ملونة كاملة برمجياً للأطفال وبأبعاد تيك توك وشورتس
    video_clip = ColorClip(size=(1080, 1920), color=bg_color, duration=video_duration)

    # 3. العلامة المائية المتحركة لحماية حقوقك باسم سلمانو
    watermark = TextClip("@salmano", fontsize=50, color='white')
    watermark = watermark.set_position(lambda t: ('center', 200 + int(t * 15))).set_duration(video_duration)

    # نص الحرف والكلمة في منتصف الشاشة بحجم كبير جداً وواضح للأطفال
    center_text = f"{char}\n{word_ar}"
    center_clip = TextClip(center_text, fontsize=120, color='white')
    center_clip = center_clip.set_position('center').set_duration(video_duration)

    # دعوة التفاعل والمتابعة في نهاية الفيديو
    cta = TextClip("لا تنسوا الاعجاب و المتابعة والمشاركة \n Follow @salmano", fontsize=40, color='yellow')
    cta = cta.set_position(('center', 1650)).set_duration(video_duration)

    # دمج كل الطبقات فوق الخلفية الملونة
    final_video = CompositeVideoClip([video_clip, watermark, center_clip, cta])
    final_video = final_video.set_audio(audio_clip)

    # تصدير الملف النهائي سحابياً
    output_name = f"salmano_episode_{episode_number}.mp4"
    final_video.write_videofile(output_name, fps=24, codec="libx264", audio_codec="aac")
    
    os.remove(audio_path)
    print(f"🟢 تم إنتاج الحلقة {episode_number} بنجاح تام وهي جاهزة في السيرفر!")

if __name__ == "__main__":
    # تشغيل الحلقة الأولى (حرف الألف)
    build_multilang_video(episode_number=1)
