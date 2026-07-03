import os
import random
import requests
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip

# 1. روابط تحميل ملفاتك المباشرة من Google Drive
# استبدل كلمة FILE_ID بالمعرّف الخاص بملفك من رابط المشاركة في الدرايف
DRIVE_LINKS = {
    "sonic_music": "https://google.com",
    "أ": {
        "img": "https://google.com",
        "voice": "https://google.com",
        "color": "#FFDE59"
    },
    "ب": {
        "img": "https://google.com",
        "voice": "https://google.com",
        "color": "#FF914D"
    }
}

def download_file_from_drive(url, output_path):
    """دالة برمجية تسحب ملفاتك من جوجل درايف سحابياً فوراً وبسرعة فائقة"""
    print(f"📥 جاري سحب الملف سحابياً من الدرايف: {output_path}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk: f.write(chunk)
    else:
        print(f"⚠️ فشل السحب! تأكد أن رابط الملف على الدرايف مضبوط على (أي شخص لديه الرابط - Anyone with the link)")

def build_perfect_video():
    # تتبع تقدم الحروف اليومي
    if not os.path.exists("progress.txt"):
        with open("progress.txt", "w") as f: f.write("أ")
    with open("progress.txt", "r") as f:
        current_char = f.read().strip()
    if current_char not in DRIVE_LINKS:
        current_char = "أ"
        
    info = DRIVE_LINKS[current_char]
    print(f"🤖 الروبوت يبدأ إنتاج فيديو حرف اليوم: {current_char}")
    
    # 2. تحميل ملفات اليوم من الدرايف إلى خادم المعالجة آلياً
    download_file_from_drive(DRIVE_LINKS["sonic_music"], "sonic.mp3")
    download_file_from_drive(info["img"], "user_img.png")
    download_file_from_drive(info["voice"], "user_voice.mp3")
    
    # 3. الهندسة الصوتية المطابقة للمرح (قص الأغنية لتنتهي مع نهاية صوتك بدقة)
    voice_clip = AudioFileClip("user_voice.mp3")
    video_duration = voice_clip.duration # تحديد مدة الفيديو الكلية بناءً على مدة صوتك
    
    # قص أغنية السونك لتبدأ مع ثانية 0 وتنتهي مع نهاية نطقك تماماً وخفض مستواها لتبرز نبرتك
    music_clip = AudioFileClip("sonic.mp3").subclip(0, video_duration).volumex(0.18)
    
    # دمج مسار صوتك وموسيقى السونك التفاعلية ليصبحا مقطعاً واحداً مفعماً بالمرح للأطفال
    final_audio = CompositeAudioClip([voice_clip, music_clip])
    
    # 4. بناء إطار الفيديو باستخدام صورتك الكرتونية المرفوعة
    video_clip = ImageClip("user_img.png").set_duration(video_duration).set_audio(final_audio)
    
    # 5. تركيب العلامة المائية المتحركة عشوائياً salmanwo
    def move_watermark(t):
        random.seed(int(t * 2)) # تتنقل وتتحرك عشوائياً مرتين في كل ثانية لحماية حقوقك
        return (random.randint(50, 600), random.randint(150, 1400))
        
    wm_img = Image.new("RGBA", (350, 90), (0, 0, 0, 0))
    wm_draw = ImageDraw.Draw(wm_img)
    wm_draw.text((15, 15), "salmanwo", fill=(255, 255, 255, 130))
    wm_img.save("wm.png")
    wm_clip = ImageClip("wm.png").set_duration(video_duration).set_position(move_watermark)
    
    # 6. تصدير المقطع والصورة المصغرة النهائية
    final_video = CompositeVideoClip([video_clip, wm_clip], size=(1080, 1920))
    final_video.write_videofile("output.mp4", fps=24, codec="libx264", audio_codec="aac")
    
    # رسم غلاف الصورة المصغرة لليوتيوب
    thumb = Image.open("user_img.png").resize((500, 500))
    bg = Image.new("RGB", (1280, 720), info["color"])
    bg.paste(thumb, (700, 110))
    ImageDraw.Draw(bg).rectangle(, outline="#FFFFFF", width=15)
    bg.save("thumbnail.png")
    
    print("🚀 تم دمج المقطع الصوتي وموسيقاك التفاعلية وإنتاج الفيديو بنجاح ساحق!")
    
    # تحديث حرف الغد
    alphabet_list = list(DRIVE_LINKS.keys())
    alphabet_list.remove("sonic_music")
    next_index = (alphabet_list.index(current_char) + 1) % len(alphabet_list)
    with open("progress.txt", "w") as f:
        f.write(alphabet_list[next_index])

if __name__ == "__main__":
    build_perfect_video()
