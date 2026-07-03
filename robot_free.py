import os
import random
import asyncio
import edge_tts
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

# قاعدة بيانات الحروف والكلمات الشاملة والترجمات مع الألوان الكرتونية المبهجة للأطفال
DATA = {
    "أ": {"word": "أَرْنَبْ", "en": "Rabbit", "fr": "Lapin", "tr": "Tavşan", "color": "#FFDE59"},
    "ب": {"word": "بَقَرَةْ", "en": "Cow", "fr": "Vache", "tr": "İnek", "color": "#FF914D"},
    "ت": {"word": "تِمْسَاحْ", "en": "Crocodile", "fr": "Crocodile", "tr": "Timsah", "color": "#38B6FF"},
    "ث": {"word": "ثَعْلَبْ", "en": "Fox", "fr": "Renard", "tr": "Tilki", "color": "#FF5757"},
    "ج": {"word": "جَمَلْ", "en": "Camel", "fr": "Chameau", "tr": "Deve", "color": "#7ED957"}
}

async def generate_voice(text, path):
    """توليد نطق ذكاء اصطناعي تفاعلي ومجاني تماماً للأطفال"""
    communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
    await communicate.save(path)

def create_cartoon_image(char, info):
    """رسم لوحة تعليمية كرتونية بألوان مبهجة وبدون استخدام خطوط خارجية لتفادي أخطاء السيرفر"""
    img = Image.new("RGB", (1080, 1920), info["color"])
    draw = ImageDraw.Draw(img)
    # رسم إطار كرتوني أبيض عريض للفيديو
    draw.rectangle([40, 40, 1040, 1880], outline="#FFFFFF", width=25)
    img.save("temp_bg.png")

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
    
    # صياغة النص التعليمي بالنطق والمحتوى اللغوي والنحوي لتوليد الصوت
    script = f"حرف اليوم هو {current_char}. {current_char} فتحة: {info['word']}. بالإنجليزية: {info['en']}. بالفرنسية: {info['fr']}. بالتركية: {info['tr']}."
    asyncio.run(generate_voice(script, "audio.mp3"))
    
    create_cartoon_image(current_char, info)
    
    audio = AudioFileClip("audio.mp3")
    video_clip = ImageClip("temp_bg.png").set_duration(audio.duration).set_audio(audio)
    
    # العلامة المائية المتحركة عشوائياً باسم حسابك salmanwo لمنع السرقة وحماية حقوقك
    def move_watermark(t):
        random.seed(int(t * 2)) # تتحرك وتتغير عشوائياً مرتين في كل ثانية
        return (random.randint(50, 650), random.randint(150, 1500))
    
    wm_img = Image.new("RGBA", (350, 90), (0,0,0,0))
    wm_draw = ImageDraw.Draw(wm_img)
    wm_draw.text((15, 15), "salmanwo", fill=(255, 255, 255, 140))
    wm_img.save("wm.png")
    
    wm_clip = ImageClip("wm.png").set_duration(audio.duration).set_position(move_watermark)
    
    # تصدير الفيديو النهائي بأبعاد الهواتف الذكية وتيك توك وريلز وشورتس واختيار معالجات أساسية لتجنب أخطاء لينكس
    final_video = CompositeVideoClip([video_clip, wm_clip], size=(1080, 1920))
    final_video.write_videofile("output.mp4", fps=24, codec="libx264", audio_codec="aac")
    
    print("🚀 تم إنتاج الفيديو التعليمي بنجاح تام!")
    
    # تحديث الحرف لليوم التالي في السحاب تلقائياً
    alphabet_list = list(DATA.keys())
    next_index = (alphabet_list.index(current_char) + 1) % len(alphabet_list)
    with open("progress.txt", "w") as f:
        f.write(alphabet_list[next_index])

if __name__ == "__main__":
    build_video()
