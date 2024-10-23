import os
import cv2

folder_data = '/home/bda/data_raw'

def extract_frames(video_path):
    dir_name, file_name = os.path.split(video_path)
    file_base_name = os.path.splitext(file_name)[0]
    frames_folder = os.path.join(dir_name, f"{file_base_name}_frames")

    if os.path.exists(frames_folder):
        print(f"Folder '{frames_folder}' sudah ada. Pemisahan frames tidak dilakukan.")
        return

    os.makedirs(frames_folder)
    
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Tidak dapat membuka video '{video_path}'")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps 

    interval = 30 if duration < 3600 else 120 

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0: 
            frame_file_path = os.path.join(frames_folder, f"{file_base_name}_frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_file_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"Total {saved_count} frames disimpan di '{frames_folder}'")

def process_videos_in_directory(folder_data):
    for root, dirs, files in os.walk(folder_data):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_path = os.path.join(root, file)
                print(f"Memproses video: {video_path}")
                extract_frames(video_path)

process_videos_in_directory(folder_data)
