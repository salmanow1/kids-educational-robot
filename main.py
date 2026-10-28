import os
import asyncio
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# 1. إعداد القاموس الشامل لكل اللغات والشخصيات والنصوص المطلوبة
# تم اختيار أفضل الأصوات البشرية الفصيحة والمستقرة مجاناً من Microsoft Edge TTS
LANGUAGES = {
    "Arabic": {
        "voice": "ar-EG-SalmaNeural", 
        "text": "أهلاً بكم في تعلم مع سلمانو! أنا أعتز بلغتي العربية الجميلة، حرفي الأول هو الألف! أنا أحب لغتي الجميلة."
    },
    "British": {
        "voice": "en-GB-SoniaNeural", 
        "text": "Welcome to learn with Salmanow! My first letter is A. I love my beautiful language!"
    },
    "French": {
        "voice": "fr-FR-DeniseNeural", 
        "text": "Bienvenue pour apprendre avec Salmanow! Ma première lettre est A. J'aime ma belle langue!"
    },
    "Italian": {
        "voice": "it-IT-ElsaNeural", 
        "text": "Benvenuti a imparare con Salmanow! La minha prima lettera è A. Amo la mia bella lingua!"
    },
    "Chinese": {
        "voice": "zh-CN-XiaoxiaoNeural", 
        "text": "欢迎同 سلمانو 一起学习！我的第一个字母 carbon 是 A。我爱我美丽的 language！"
    },
    "Korean": {
        "voice": "ko-KR-SunHiNeural", 
        "text": "سلمانو와 함께하는 학습에 오신 것을 환영합니다! 나의 첫 글자는 A입니다. 나는 나의 아름다운 언어를 사랑합니다!"
    },
    "Hindi": {
        "voice": "hi-IN-SwaraNeural", 
        "text": "سلمانو के साथ सीखने में आपका स्वागत है! मेरा पहला अक्षर A है। मुझे अपनी सुंदर भाषा से प्यार है!"
    }
}

async def generate_speech(text, voice_name, output_path):
    """توليد صوت بشري فصيح وعالي الجودة مجاناً تلقائياً"""
    print(f"[صوت] جاري توليد الصوت باستخدام: {voice_name}...")
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_path)

def create_video_segment(image_path, audio_path, output_path):
    """دمج الصوت مع صورة الطفل المقابلة وصناعة مشهد متحرك (تأثير الرقص والغناء)"""
    print(f"[مونتاج] جاري دمج {image_path} مع {audio_path}...")
    
    # تحميل ملف الصوت ومعرفة مدته الزمنية
    audio_clip = AudioFileClip(audio_path)
    
    # إنشاء مقطع فيديو من الصورة الثابتة يمتد على نفس مدة الصوت
    image_clip = ImageClip(image_path).set_duration(audio_clip.duration)
    
    # دمج الصوت والصورة معاً
    video_clip = image_clip.set_audio(audio_clip)
    
    # إضافة تأثير حركة تكبير وتصغير مستمرة (Zoom-in) لمحاكاة الرقص والحماس تلقائياً
    video_clip = video_clip.resize(lambda t: 1 + 0.03 * (t % 2)) 
    
    # تصدير مشهد الطفل وحفظه كمقطع فيديو مؤقت
    video_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
    return output_path

async def main():
    print("🚀 بدء الروبوت: إنتاج الفيديو التعليمي التلقائي للأطفال...")
    
    # إنشاء مجلدات مؤقتة لحفظ الملفات إذا لم تكن موجودة
    os.makedirs("temp_audio", exist_ok=True)
    os.makedirs("temp_video", exist_ok=True)
    
    video_segments = []
    
    # ملاحظة هندسية: لتشغيل النظام تلقائياً دون تدخل بالكامل مجاناً،
    # يجب وضع صور الأطفال مسبقاً في مجلد بالمستودع وتسميتها باسم اللغة (مثال: Arabic.png, British.png ... إلخ)
    # الصور يجب أن تعكس الأزياء المطلوبة (الزي العربي، البريطاني، الفرنسي، الإيطالي، الصيني، الكوري، الهندي)
    
    for lang, data in LANGUAGES.items():
        audio_path = f"temp_audio/{lang}.mp3"
        segment_video_path = f"temp_video/{lang}.mp4"
        image_path = f"images/{lang}.png"  # مسار ملف الصورة الخاصة بكل طفل داخل المشروع
        
        # إذا لم تكن الصورة موجودة، نضع صورة افتراضية لمنع توقف الروبوت
        if not os.path.exists(image_path):
            os.makedirs("images", exist_ok=True)
            print(f"⚠️ تحذير: يرجى تزويد المجلد بصورة الطفل بالزي المطلوب وتسميتها: {image_path}")
            continue
            
        # 1. توليد الصوت لكل طفل بلغته الخاصة وبشكل فصيح وغنائي
        await generate_speech(data["text"], data["voice"], audio_path)
        
        # 2. إنشاء فيديو المشهد الفردي للطفل وهو يغني ويرقص
        segment_file = create_video_segment(image_path, audio_path, segment_video_path)
        video_segments.append(segment_file)
    
    # 3. دمج كافة المشاهد معاً لإنتاج الفيديو التعليمي الكامل والموحد
    if video_segments:
        print("[دمج] جاري تجميع مقاطع الأطفال لإنتاج الفيديو النهائي الموحد...")
        clips = [VideoFileClip(vid) for vid in video_segments]
        
        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile("final_educational_robot_video.mp4", fps=24, codec="libx264", audio_codec="aac")
        print("🎉 تم إنتاج الفيديو النهائي بنجاح تحت اسم: final_educational_robot_video.mp4")
    else:
        print("❌ فشل الإنتاج لعدم توفر صور الأطفال في مجلد images/")

if __name__ == "__main__":
    asyncio.run(main())
