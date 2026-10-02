import os
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

# قاموس الحلقات اليومي: الحرف، الكلمة بالعربية، والكلمة بالإنجليزية للبحث عن صورتها
CHANNELS_DATA = {
    1: {"char": "أ", "word_ar": "أَسَد", "search_keyword": "lion cartoon"},
    2: {"char": "ب", "word_ar": "بَطَّة", "search_keyword": "duck cartoon"},
    3: {"char": "ت", "word_ar": "تِمْسَاح", "search_keyword": "crocodile cartoon"},
    4: {"char": "و", "word_ar": "وَلَد", "search_keyword": "boy cartoon"},
}

def download_free_image(keyword):
    print(f"🔍 الروبوت يتصل بمخزن الصور للبحث عن: {keyword}...")
    url = f"https://unsplash.com?{keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        with open("downloaded_bg.png", "wb") as f:
            f.write(response.content)
        print("📥 تم تحميل الصورة الخلفية المناسبة بنجاح من الإنترنت!")
        return "downloaded_bg.png"
    else:
        raise Exception("❌ فشل الاتصال بموقع الصور الخارجي.")

def build_multilang_video(episode_number):
    data = CHANNELS_DATA.get(episode_number)
    if not data:
        print("🏁 تم إنهاء السلسلة بالكامل!")
        return

    char = data["char"]
    word_ar = data["word_ar"]
    
    bg_image = download_free_image(data["search_keyword"])

    arabic_speech = f"حرف {char}. {char} فتحة. {word_ar}."
    english_speech = f"Letter {char} in Arabic means {data['search_keyword'].split()[0]}."
    full_speech = f"{arabic_speech} ... {english_speech} ... Please Follow Salmano!"

    print("🔊 جاري توليد الصوت البشري بالتشكيل...")
    tts = gTTS(text=full_speech, lang='ar', slow=False)
    audio_path = "temp_voice.mp3"
    tts.save(audio_path)

    audio_clip = AudioFileClip(audio_path)
    video_duration = audio_clip.duration
    video_clip = ImageClip(bg_image).set_duration(video_duration)

    # العلامة المائية المتحركة لحماية حقوقك باسم سلمانو
    watermark = TextClip("@salmano", fontsize=40, color='white')
    watermark = watermark.set_position(lambda t: ('center', 100 + int(t * 15))).set_duration(video_duration)

    # نصوص الترجمة التلقائية متعددة اللغات لأسفل الشاشة لجميع أطفال العالم
    sub_text = f"عربي: {word_ar} | English: {data['search_keyword'].split()[0].capitalize()}"
    subtitle_clip = TextClip(sub_text, fontsize=35, color='yellow', bg_color='black')
    subtitle_clip = subtitle_clip.set_position(('center', 1600)).set_duration(video_duration)

    # دعوة التفاعل والمتابعة في نهاية الفيديو
    cta = TextClip("لا تنسوا الاعجاب و المتابعة والمشاركة \n Follow @salmano", fontsize=38, color='cyan')
    cta = cta.set_position(('center', 1750)).set_duration(video_duration)

    final_video = CompositeVideoClip([video_clip, watermark, subtitle_clip, cta])
    final_video = final_video.set_audio(audio_clip)

    output_name = f"salmano_episode_{episode_number}.mp4"
    final_video.write_videofile(output_name, fps=24, codec="libx264", audio_codec="aac")
    
    os.remove(audio_path)
    os.remove(bg_image)
    print(f"🟢 تم إنتاج الحلقة {episode_number} بنجاح تام!")

if __name__ == "__main__":
    build_multilang_video(episode_number=1)
