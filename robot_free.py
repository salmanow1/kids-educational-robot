import os
import random
import asyncio
import edge_tts
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip

# قاعدة بيانات الحروف التعليمية والترجمات مع الألوان الكرتونية للأطفال
DATA = {
    "أ": {"word": "أَرْنَبْ", "en": "Rabbit", "fr": "Lapin", "tr": "Tavşan", "color": "#FFDE59"},
    "ب": {"word": "بَقَرَةْ", "en": "Cow", "fr": "Vache", "tr": "İnek", "color": "#FF914D"},
    "ت": {"word": "تِمْسَاحْ", "en": "Crocodile", "fr": "Crocodile", "tr": "Timsah", "color": "#38B6FF"}
}

async def generate_voice(text, path):
    """توليد نطق ذكاء اصطناعي تفاعلي ومجاني تماماً للأطفال"""
    communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
    await communicate.save(path)

def create_cartoon_images(char, info):
    """رسم لوحة الفيديو الكرتونية والصورة المصغرة بحسابات رياضية دقيقة ودون خطأ"""
    # 1. إعداد صورة الفيديو الرأسي المبهج
    video_img = Image.new("RGB", (1080, 1920), info["color"])
    v_draw = ImageDraw.Draw(video_img)
    v_draw.rectangle([40, 40, 1040, 1880], outline="#FFFFFF", width=30)
    
    # إضافة نص العلامة المائية الثابتة salmanwo على الصورة كبديل أكثر استقراراً داخل Docker
    v_draw.text((100, 100), "salmanwo", fill="#FFFFFF")
    video_img.save("temp_bg.png")
    
    # 2. إعداد الصورة المصغرة (Thumbnail) لليوتيوب وفيسبوك 1280x720
    thumb_img = Image.new("RGB", (1280, 720), info["color"])
    t_draw = ImageDraw.Draw(thumb_img)
    t_draw.rectangle([20, 20, 1260, 700], outline="#FFFFFF", width=15)
    t_draw.text((50, 50), f"Letter {char}", fill="#FFFFFF")
    thumb_img.save("thumbnail.png")
    print("🎨 تم رسم لوحات الأنيميشن والصورة المصغرة برمجياً بنجاح!")

def build_video():
    # التحقق من ملف التتبع السحابي لمعرفة حرف اليوم
    if not os.path.exists("progress.txt"):
        with open("progress.txt", "w") as f: f.write("أ")
    
    with open("progress.txt", "r") as f:
        current_char = f.read().strip()
        
    if current_char not in DATA:
        current_char = "أ"
        
    info = DATA[current_char]
    print(f"🤖 الروبوت يصنع الآن سحابياً فيديو: حرف {current_char}")
    
    # صياغة النص التعليمي للذكاء الاصطناعي
    script = f"حرف اليوم هو {current_char}. {current_char} فتحة: {info['word']}. بالإنجليزية: {info['en']}. بالفرنسية: {info['fr']}. بالتركية: {info['tr']}."
    asyncio.run(generate_voice(script, "audio.mp3"))
    
    # توليد الصور
    create_cartoon_images(current_char, info)
    
    # رص المقطع ودمجه
    audio = AudioFileClip("audio.mp3")
    video_clip = ImageClip("temp_bg.png").set_duration(audio.duration).set_audio(audio)
    
    # حفظ الفيديو النهائي المتوافق تماماً مع بيئات لينكس والسيرفرات السحابية
    video_clip.write_videofile("output.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("🚀 تم إنتاج الفيديو التعليمي والصورة المصغرة بنجاح تام!")
    
    # تحديث الحرف لليوم التالي في السحاب تلقائياً
    alphabet_list = list(DATA.keys())
    next_index = (alphabet_list.index(current_char) + 1) % len(alphabet_list)
    with open("progress.txt", "w") as f:
        f.write(alphabet_list[next_index])

if __name__ == "__main__":
    build_video()
