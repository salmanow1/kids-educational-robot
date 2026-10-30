import os
import asyncio
import requests
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, VideoFileClip
import publisher

LANGUAGES = {
    "Arabic": {
        "voice": "ar-EG-SalmaNeural", 
        "text": "أهلاً بكم في تعلم مع سلمانو! أنا أعتز بلغتي العربية الجميلة، حرفي الأول هو الألف! أنا أحب لغتي الجميلة.",
        "image_prompt": "Hyper-realistic photograph of a happy 5-year-old Arab child wearing traditional elegant Arabic Thobe and Shemagh, singing and dancing joyfully, vibrant educational kids show background, 4k resolution"
    },
    "British": {
        "voice": "en-GB-SoniaNeural", 
        "text": "Welcome to learn with Salmanow! My first letter is A. I love my beautiful language!",
        "image_prompt": "Hyper-realistic photograph of a happy 5-year-old British child wearing traditional British royal attire, singing and dancing happily, school theme background, 4k resolution"
    },
    "French": {
        "voice": "fr-FR-DeniseNeural", 
        "text": "Bienvenue pour apprendre avec Salmanow! Ma première lettre est A. J'aime ma belle langue!",
        "image_prompt": "Hyper-realistic photograph of a happy 5-year-old French child in classic elegant Parisian attire, beret hat, singing and dancing joyfully, 4k resolution"
    },
    "Italian": {
        "voice": "it-IT-ElsaNeural", 
        "text": "Benvenuti a imparare con Salmanow! La minha prima letterae A. Amo la mia bella lingua!",
        "image_prompt": "Hyper-realistic photograph of a happy 5-year-old Italian child in traditional Italian festive clothing, singing and dancing, artistic background, 4k resolution"
    },
    "Chinese": {
        "voice": "zh-CN-XiaoxiaoNeural", 
        "text": "欢迎同 سلمانو 一起学习！我的第一个字母 carbon 是 A。我爱我美丽的 language！",
        "image_prompt": "Hyper-realistic photograph of a happy 5-year-old Chinese child wearing traditional Hanfu dress, singing and dancing enthusiastically, colorful background, 4k resolution"
    },
    "Korean": {
        "voice": "ko-KR-SunHiNeural", 
        "text": "سلمانو와 함께하는 학습에 오신 것을 환영합니다! 나의 첫 글자는 A입니다. 나는 나의 아름다운 언어를 사랑합니다!",
        "image_prompt": "Hyper-realistic photograph of a happy 5-year-old Korean child wearing traditional colorful Hanbok dress, singing and dancing, 4k resolution"
    },
    "Hindi": {
        "voice": "hi-IN-SwaraNeural", 
        "text": "سلمانو के साथ सीखने में आपका स्वागत है! मेरा पहला अक्षर A है। मुझे अपनी सुंदर भाषा से प्यार है!",
        "image_prompt": "Hyper-realistic photograph of a happy 5-year-old Indian child wearing traditional elegant Sherwani, singing and dancing happily, bright festive background, 4k resolution"
    }
}

async def main():
    print("🚀 انطلاق الروبوت: إنتاج ونشر تلقائي ومستمر بدون أي توقف...")
    
    os.makedirs("temp_audio", exist_ok=True)
    os.makedirs("temp_video", exist_ok=True)
    os.makedirs("images", exist_ok=True)
    
    video_segments = []
    
    for lang, data in LANGUAGES.items():
        audio_path = f"temp_audio/{lang}.mp3"
        segment_video_path = f"temp_video/{lang}.mp4"
        image_path = f"images/{lang}.png"
        
        # 1. توليد الصورة تلقائياً بالذكاء الاصطناعي مجاناً وبسرعة
        url = f"https://pollinations.ai{requests.utils.quote(data['image_prompt'])}?width=1080&height=1920&enhanced=true"
        img_data = requests.get(url).content
        with open(image_path, 'wb') as f:
            f.write(img_data)
            
        # 2. توليد الصوت البشري الفصيح الحماسي الغنائي
        communicate = edge_tts.Communicate(data["text"], data["voice"])
        await communicate.save(audio_path)
        
        # 3. المونتاج التلقائي (دمج الصوت والصورة مع إضافة حركة رقص مستمرة)
        audio_clip = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path).set_duration(audio_clip.duration)
        video_clip = image_clip.set_audio(audio_clip)
        video_clip = video_clip.resize(lambda t: 1 + 0.04 * (t % 1.5)) 
        video_clip.write_videofile(segment_video_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
        
        video_segments.append(segment_video_path)
    
    # 4. دمج كافة لغات العالم في الفيديو النهائي الموحد
    print("🎬 جاري تجميع مقاطع الأطفال وصناعة العمل المطلوب كاملاً...")
    clips = [VideoFileClip(vid) for vid in video_segments]
    final_output = "final_educational_robot_video.mp4"
    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(final_output, fps=24, codec="libx264", audio_codec="aac")
    
    # 5. النشر الفوري المباشر على المنصات (يوتيوب، تيك توك، فيسبوك، إنستغرام، كاوي)
    publisher.start_publishing_flow(final_output)
    print("🎉 تم العمل والنشر بنجاح تام!")

if __name__ == "__main__":
    asyncio.run(main())
