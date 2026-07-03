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
    """توليد نطق ذكاء اصطناعي تفاعلي ومجاني تماماً للأطفال من مايكروسوفت"""
    communicate = edge_tts.Communicate(text, "ar-EG-ShakirNeural")
    await communicate.save(path)

def create_cartoon_image(char, info):
    """رسم لوحة تعليمية كرتونية مبهجة للفيديو بدون حقول فارغة لتفادي توقف الحاوية"""
    img = Image.new("RGB", (1080, 1920), info["color"])
    draw = ImageDraw.Draw(img)
    # رسم إطار كرتوني أبيض عريض محدد الإحداثيات بدقة [xmin, ymin, xmax, ymax]
    draw.rectangle([40, 40, 1040, 1880], outline="#FFFFFF", width=30)
    img.save("temp_bg.png")

def create_thumbnail_image(char, info):
    """رسم الصورة المصغرة (Thumbnail) تلقائياً بأبعاد اليوتيوب القياسية 1280x720 مجاناً وبألوان كرتونية جذابة للأطفال"""
    thumb = Image.new("RGB", (1280, 720), info["color"])
    draw = ImageDraw.Draw(thumb)
    
    # رسم إطار كرتوني مزدوج جذاب جداً للأطفال لزيادة المشاهدات والنقرات
    draw.rectangle([20, 20, 1260, 700], outline="#FFFFFF", width=15)
    draw.rectangle([45, 45, 1235, 675], outline="#FF5757", width=5)
    
    # رسم مربعات كرتونية برمجية في الخلفية لإعطاء طابع الأنيميشن الحيوي
    draw.rectangle([100, 100, 400, 600], fill="#FFFFFF", outline="#38B6FF", width=10)
    draw.rectangle([500, 150, 1150, 580], fill="#FFFFFF", outline="#7ED957", width=10)
    
    # حفظ الصورة المصغرة لتكون جاهزة للرفع مع الفيديو
    thumb.save("thumbnail.png")
    print("🎨 تم توليد الصورة المصغرة الكرتونية بنجاح باسم thumbnail.png")

def build_video():
    # التحقق من ملف التتبع السحابي لمعرفة حرف اليوم
    if not os.path.exists("progress.txt"):
        with open("progress.txt", "w") as f: f.write("أ")
    
    with open("progress.txt", "r") as f:
        current_char = f.read().strip()
        
    if current_char not in DATA:
        current_char = "أ"
        
    info = DATA[current_char]
    print(f"🤖 الروبوت يصنع الآن سحابياً فيديو وصورة مصغرة لـ: حرف {current_char}")
    
    # 1. صياغة النص التعليمي بالنطق والمحتوى اللغوي لتوليد الصوت
    script = f"حرف اليوم هو {current_char}. {current_char} فتحة: {info['word']}. بالإنجليزية: {info['en']}. بالفرنسية: {info['fr']}. بالتركية: {info['tr']}."
    asyncio.run(generate_voice(script, "audio.mp3"))
    
    # 2. توليد الرسوم الكرتونية للفيديو وللصورة المصغرة برمجياً ومجاناً
    create_cartoon_image(current_char, info)
    create_thumbnail_image(current_char, info)
    
    # 3. دمج المقطع ومحاذاة الصوت
    audio = AudioFileClip("audio.mp3")
    video_clip = ImageClip("temp_bg.png").set_duration(audio.duration).set_audio(audio)
    
    # 4. العلامة المائية المتحركة عشوائياً باسم حسابك salmanwo لحماية حقوقك ومنع السرقة
    def move_watermark(t):
        random.seed(int(t * 2)) # تتحرك وتتغير عشوائياً مرتين في كل ثانية
        return (random.randint(50, 650), random.randint(150, 1500))
    
    wm_img = Image.new("RGBA", (350, 90), (0, 0, 0, 0))
    wm_draw = ImageDraw.Draw(wm_img)
    wm_draw.text((15, 15), "salmanwo", fill=(255, 255, 255, 140))
    wm_img.save("wm.png")
    
    wm_clip = ImageClip("wm.png").set_duration(audio.duration).set_position(move_watermark)
    
    # 5. تصدير الفيديو النهائي بأبعاد الهواتف الذكية مع ضبط الـ Codec المتوافق مع السيرفر السحابي
    final_video = CompositeVideoClip([video_clip, wm_clip], size=(1080, 1920))
    final_video.write_videofile("output.mp4", fps=24, codec="libx264", audio_codec="aac")
    
    print("🚀 تم إنتاج الفيديو التعليمي والصورة المصغرة بنجاح تام!")
    
    # 6. تحديث الحرف لليوم التالي في السحاب تلقائياً
    alphabet_list = list(DATA.keys())
    next_index = (alphabet_list.index(current_char) + 1) % len(alphabet_list)
    with open("progress.txt", "w") as f:
        f.write(alphabet_list[next_index])

if __name__ == "__main__":
    build_video()
