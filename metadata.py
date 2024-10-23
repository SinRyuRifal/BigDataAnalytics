import os
import pandas as pd
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import cv2

folder_data = '/home/bda/data_raw'
daftar_metadata = []


def dapatkan_metadata_file(jalur_file):
    nama_file = os.path.basename(jalur_file)
    ukuran_file = os.path.getsize(jalur_file)
    waktu_modifikasi = os.path.getmtime(jalur_file)
    waktu_modifikasi = datetime.fromtimestamp(waktu_modifikasi).strftime('%Y-%m-%d %H:%M:%S')
    ekstensi_file = os.path.splitext(nama_file)[1].lower()

    metadata = {
        'filename': nama_file,
        'Ukuran File (bytes)': ukuran_file,
        'Waktu Modifikasi': waktu_modifikasi,
        'Ekstensi File': ekstensi_file,
        'Jalur File': jalur_file
    }
    
    if ekstensi_file in ['.csv', '.xlsx']:
        try:
            if ekstensi_file == '.csv':
                df = pd.read_csv(jalur_file)
            elif ekstensi_file == '.xlsx':
                df = pd.read_excel(jalur_file)
            metadata['Jumlah Baris'] = df.shape[0]
            metadata['Jumlah Kolom'] = df.shape[1]
            data_teks = df.astype(str).apply(lambda x: ' '.join(x), axis=1)
            teks_tergabung = ' '.join(data_teks.tolist())
            metadata['Jumlah Karakter'] = len(teks_tergabung)
            metadata['Jumlah Kata'] = len(teks_tergabung.split())
            metadata['Jumlah Kata Unik'] = len(set(teks_tergabung.split()))
        except Exception as e:
            metadata['Kesalahan'] = f'Kesalahan membaca file: {e}'
    
    elif ekstensi_file in ['.json']:
        try:
            df = pd.read_json(jalur_file)
            metadata['Jumlah Kunci'] = len(df.keys())
            data_json = df.astype(str).apply(lambda x: ' '.join(x), axis=1)
            teks_tergabung = ' '.join(data_json.tolist())
            metadata['Jumlah Karakter'] = len(teks_tergabung)
            metadata['Jumlah Kata'] = len(teks_tergabung.split())
            metadata['Jumlah Kata Unik'] = len(set(teks_tergabung.split()))
        except Exception as e:
            metadata['Kesalahan'] = f'Kesalahan membaca file: {e}'
    
    elif ekstensi_file in ['.jpg', '.jpeg', '.png', '.heic']:
        try:
            img = Image.open(jalur_file)
            metadata['Ukuran Gambar'] = img.size
            metadata['Mode Gambar'] = img.mode
            metadata['Format Gambar'] = img.format
            metadata['Info Gambar'] = img.info
            

            img_cv = cv2.imread(jalur_file)
            if img_cv is not None:
                metadata['Shape Gambar'] = img_cv.shape

            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    metadata[tag] = value
                metadata['Merek Kamera'] = exif_data.get(271)
                metadata['Model Kamera'] = exif_data.get(272)
                metadata['Waktu Eksposur'] = exif_data.get(33434)
                metadata['F-Number'] = exif_data.get(33437)
                metadata['ISO'] = exif_data.get(34855)
                metadata['Panjang Fokus'] = exif_data.get(37386)
                metadata['Tanggal Pengambilan'] = exif_data.get(36867)

                if 'GPSInfo' in exif_data:
                    gps_info = exif_data[34853]
                    metadata['GPS Lintang'] = gps_info.get(GPSTAGS.get(2))
                    metadata['GPS Bujur'] = gps_info.get(GPSTAGS.get(4))
                
                metadata['Orientasi'] = exif_data.get(274)
                metadata['White Balance'] = exif_data.get(41987)
                metadata['Flash Digunakan'] = exif_data.get(37385)
                metadata['Mode Metering'] = exif_data.get(37383)
                metadata['Program Eksposur'] = exif_data.get(34850)

            metadata['Profil Warna'] = img.info.get('icc_profile', 'N/A')
            metadata['Kata Kunci'] = img.info.get('keywords', 'N/A')
            metadata['Hak Cipta'] = img.info.get('copyright', 'N/A')
            
        except Exception as e:
            metadata['Kesalahan'] = f'Kesalahan membaca gambar: {e}'
    
    elif ekstensi_file in ['.mp4', '.avi', '.mov']:
        try:
            video = cv2.VideoCapture(jalur_file)
            if not video.isOpened():
                metadata['Kesalahan'] = 'Video tidak dapat dibuka atau tidak didukung'
                return metadata
            
            lebar = video.get(cv2.CAP_PROP_FRAME_WIDTH)
            tinggi = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = video.get(cv2.CAP_PROP_FPS)
            jumlah_frame = video.get(cv2.CAP_PROP_FRAME_COUNT)
            durasi = jumlah_frame / fps if fps > 0 else 0
            codec_pixel_format = video.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT)
            exposure = video.get(cv2.CAP_PROP_AUTO_EXPOSURE)
            channel_audio_total = video.get(cv2.CAP_PROP_AUDIO_TOTAL_CHANNELS)
            contrast = video.get(cv2.CAP_PROP_CONTRAST)
            saturation = video.get(cv2.CAP_PROP_SATURATION)
            speed = video.get(cv2.CAP_PROP_SPEED)
            
            metadata['Resolusi'] = f'{int(lebar)}x{int(tinggi)}'
            metadata['FPS'] = fps
            metadata['Jumlah Frame'] = jumlah_frame
            metadata['Durasi (detik)'] = durasi
            metadata['Format Codec Pixel'] = codec_pixel_format
            metadata['Exposure'] = exposure
            metadata['Audio Total Channel'] = channel_audio_total
            metadata['Contrast'] = contrast
            metadata['Saturation'] = saturation
            metadata['Speed'] = speed

            ret, frame = video.read()
            if ret and frame is not None:
                metadata['Shape Video Frame'] = frame.shape

        except Exception as e:
            metadata['Kesalahan'] = f'Kesalahan membaca video: {e}'
    
    return metadata

for root, dirs, files in os.walk(folder_data):
    for file in files:
        jalur_file = os.path.join(root, file)
        metadata_file = dapatkan_metadata_file(jalur_file)
        daftar_metadata.append(metadata_file)

df_metadata = pd.DataFrame(daftar_metadata)
jalur_csv_metadata = os.path.join(folder_data, 'metadata_summary.csv')
df_metadata.to_csv(jalur_csv_metadata, index=False)

print(f"Metadata berhasil disimpan ke: {jalur_csv_metadata}")
