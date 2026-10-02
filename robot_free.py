import os
import cv2
import numpy as np
from gtts import gTTS
import subprocess

CHANNELS_DATA = {
    1: {"char": "A", "word": "Asad", "color": (97, 111, 255)},
}

def create_video_pure_opencv(episode_number):
    data = CHANNELS_DATA.get(episode_number)
    if not data:
        return

    char = data["char"]
    word = data["word"]
    bg_color = data["color"]

    # 1. توليد الصوت
    text_to_speak = f"Letter {char}... {word}... Follow Salmano!"
    tts = gTTS(text=text_to_speak, lang='en', slow=False)
    audio_path = "temp_voice.mp3"
    tts.save(audio_path)

    # 2. إنشاء الفيديو الصامت (10 ثوانٍ)
    video_silent_path = "temp_silent.mp4"
    fps = 24
    total_frames = 10 * fps
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_silent_path, fourcc, fps, (1080, 1920))

    for frame_num in range(total_frames):
        frame = np.zeros((1920, 1080, 3), dtype=np.uint8)
        frame[:] = bg_color

        # حركة العلامة المائية
        watermark_y = 200 + (frame_num % 300)
        cv2.putText(frame, "@salmano", (350, watermark_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4, cv2.LINE_AA)
        
        # النص المركزي
        cv2.putText(frame, char, (450, 850), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10, cv2.LINE_AA)
        cv2.putText(frame, word, (350, 1100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 6, cv2.LINE_AA)
        
        # نص التفاعل
        cv2.putText(frame, "Like, Share, Follow @salmano", (150, 1700), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 255), 4, cv2.LINE_AA)

        video_writer.write(frame)

    video_writer.release()

    # 3. الدمج المباشر عبر موجه أوامر النظام (FFmpeg Command) لتفادي انهيار المكاتب
    output_final = f"salmano_episode_{episode_number}.mp4"
    ffmpeg_cmd = f"ffmpeg -y -i {video_silent_path} -i {audio_path} -c:v libx264 -c:a aac -strict experimental {output_final}"
    
    subprocess.run(ffmpeg_cmd, shell=True, check=True)

    # تنظيف
    os.remove(audio_path)
    os.remove(video_silent_path)
    print("🟢 SUCCESS: Video created perfectly on headless server!")

if __name__ == "__main__":
    create_video_pure_opencv(episode_number=1)
