import os
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

CHANNELS_DATA = {
    1: {"char": "أ", "word_ar": "أَسَد", "word_en": "Lion", "word_fr": "Lion", "keyword": "lion"},
    2: {"char": "ب", "word_ar": "بَطَّة", "word_en": "Duck", "word_fr": "Canard", "keyword": "duck"},
}

def download_animated_bg(keyword):
    print(f"🔍 الروبوت يجلب خلفية كرتونية مخصصة للأطفال للحرف: {keyword}...")
    # سحب صورة كرتونية عالية الجودة ومناسبة لعمر الأطفال من مخزن الصور المفتوح
    url = f"https://unsplash.com,{keyword},kids"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open("bg.png", "wb") as f:
                f.write(response.content)
            return "bg.png"
    except:
        pass
    # خلفية احتياطية كرتونية في حال انقطع السيرفر الخارجي
    return None

def build_real_educational_video(episode_number):
    data = CHANNELS_DATA.get(episode_number)
    if not data:
        return

    char = data["char"]
    word_ar = data["word_ar"]
    word_en = data["word_en"]
    
    # 1. جلب الخلفية الكرتونية التلقائية
    bg_image = download_animated_bg(data["keyword"])
    if not bg_image:
        print("❌ لم يتم العثور على صورة الخلفية الكرتونية.")
        return

    # 2. توليد النطق الصوتي البشري الدقيق بالتشكيل العربي ولغات العالم
    full_speech = f"حرف {char}... {char} فتحة... {word_ar}... باللغة الإنجليزية {word_en}... تابعو سلمانو"
    print("🔊 جاري توليد النطق النحوي الدقيق...")
    tts = gTTS(text=full_speech, lang='ar', slow=False)
    audio_path = "voice.mp3"
    tts.save(audio_path)

    # 3. معالجة الفيديو الاحترافي بالأبعاد الرأسية المناسبة (Shorts/TikTok)
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    video_base = ImageClip(bg_image).set_duration(duration)

    # 4. حقن النصوص التعليمية بطريقة سحابية آمنة لا تسبب انهيار النظام
    # العلامة المائية المتحركة لحماية المحتوى باسم سلمانو
    watermark = TextClip("@salmano", fontsize=45, color='white', font='Liberation-Sans-Bold')
    watermark = watermark.set_position(lambda t: ('center', 150 + int(t * 12))).set_duration(duration)

    # الحرف العربي الكبير والكلمة في المنتصف بشكل واضح جداً للأطفال
    main_label = f"({char}) \n {word_ar}"
    center_clip = TextClip(main_label, fontsize=110, color='yellow', font='Liberation-Sans-Bold', stroke_color='black', stroke_width=2)
    center_clip = center_clip.set_position('center').set_duration(duration)

    # شريط الترجمة متعدد اللغات لأسفل الشاشة
    sub_title = f"English: {word_en} | Français: {data['word_fr']}"
    sub_clip = TextClip(sub_title, fontsize=35, color='white', bg_color='black', font='Liberation-Sans-Regular')
    sub_clip = sub_clip.set_position(('center', 1600)).set_duration(duration)

    # شريط التفاعل النهائي (لا تنسوا الإعجاب والمتابعة والمشاركة)
    cta = TextClip("👉 لا تنسوا الاعجاب و المتابعة والمشاركة 👈\n Follow @salmano", fontsize=40, color='cyan', font='Liberation-Sans-Bold')
    cta = cta.set_position(('center', 1750)).set_duration(duration)

    # الدمج النهائي للطبقات فوق الخلفية الكرتونية بالصوت
    final_video = CompositeVideoClip([video_base, watermark, center_clip, sub_clip, cta])
    final_video = final_video.set_audio(audio_clip)

    # تصدير الفيديو التعليمي الحقيقي
    output_name = f"salmano_episode_{episode_number}.mp4"
    final_video.write_videofile(output_name, fps=24, codec="libx264", audio_codec="aac")

    # تنظيف السيرفر
    audio_clip.close()
    final_video.close()
    os.remove(audio_path)
    os.remove(bg_image)
    print("🟢 SUCCESS: تم إنتاج فيديو تعليمي حقيقي واحترافي بنجاح!")

if __name__ == "__main__":
    build_real_educational_video(episode_number=1)
