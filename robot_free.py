import os
import numpy as np
import cv2
from gtts import gTTS
from moviepy.editor import AudioFileClip, VideoFileClip

CHANNELS_DATA = {
    1: {"char": "A", "word": "Asad", "color": (97, 111, 255)}, # OpenCV uses BGR (Redish Coral)
    2: {"char": "B", "word": "Batta", "color": (226, 144, 74)},
}

def create_video_opencv(episode_number):
    data = CHANNELS_DATA.get(episode_number)
    if not data:
        return

    char = data["char"]
    word = data["word"]
    bg_color = data["color"]

    # 1. توليد الصوت ونطق الحرف
    text_to_speak = f"Letter {char}... {word}... Follow Salmano Channel!"
    tts = gTTS(text=text_to_speak, lang='en', slow=False)
    audio_path = "temp_voice.mp3"
    tts.save(audio_path)

    # معرفة مدة الصوت
    audio_clip = AudioFileClip(audio_path)
    duration = int(audio_clip.duration) + 1
    fps = 24
    total_frames = duration * fps

    # 2. إنشاء الفيديو برمجياً بواسطة OpenCV كمصفوفات صور
    video_path = "temp_silent.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_path, fourcc, fps, (1080, 1920))

    for frame_num in range(total_frames):
        # خلفية ملونة ثابته
        frame = np.zeros((1920, 1080, 3), dtype=np.uint8)
        frame[:] = bg_color

        # تحريك العلامة المائية ببطء في الشاشة @salmano
        watermark_y = 200 + (frame_num % 300)
        cv2.putText(frame, "@salmano", (350, watermark_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4, cv2.LINE_AA)

        # النص المركزي (الحرف والكلمة)
        cv2.putText(frame, char, (450, 850), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10, cv2.LINE_AA)
        cv2.putText(frame, word, (350, 1100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 6, cv2.LINE_AA)

        # نص المتابعة والتفاعل في الأسفل
        cv2.putText(frame, "Like, Share, Follow @salmano", (150, 1700), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 255), 4, cv2.LINE_AA)

        video_writer.write(frame)

    video_writer.release()
    audio_clip.close()

    # 3. دمج الصوت مع الفيديو الصامت الناتج
    silent_video = VideoFileClip(video_path)
    audio_bg = AudioFileClip(audio_path)
    final_video = silent_video.set_audio(audio_bg)
    
    final_video.write_videofile(f"salmano_episode_{episode_number}.mp4", fps=fps, codec="libx264", audio_codec="aac")
    
    # تنظيف الملفات المؤقتة
    silent_video.close()
    audio_bg.close()
    os.remove(audio_path)
    os.remove(video_path)
    print("🟢 SUCCESS: Video created perfectly without fonts crash!")

if __name__ == "__main__":
    create_video_opencv(episode_number=1)
