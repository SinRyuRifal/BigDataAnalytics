import os
import cv2
import numpy as np

folder_data = '/home/bda/data_raw'


def buat_folder_baru(folder_awal, nama_file):
    folder_baru = os.path.join(folder_awal, f"{nama_file}_imageProcessing")
    if not os.path.exists(folder_baru):
        os.makedirs(folder_baru)
    return folder_baru

def cek_file_ada(folder_baru, nama_file, filter_tipe):
    return os.path.exists(os.path.join(folder_baru, f"{nama_file}_{filter_tipe}.jpg"))

def proses_gambar(jalur_file, folder_baru, nama_file):
    img_cv = cv2.imread(jalur_file, cv2.IMREAD_GRAYSCALE)

    if img_cv is not None:
        if not cek_file_ada(folder_baru, nama_file, 'canny_1'):
            canny_edges_1 = cv2.Canny(img_cv, 50, 150)
            cv2.imwrite(os.path.join(folder_baru, f"{nama_file}_canny_1.jpg"), canny_edges_1)

        if not cek_file_ada(folder_baru, nama_file, 'canny_3'):
            canny_edges_3 = cv2.Canny(img_cv, 100, 200)
            cv2.imwrite(os.path.join(folder_baru, f"{nama_file}_canny_3.jpg"), canny_edges_3)

        if not cek_file_ada(folder_baru, nama_file, 'roberts'):
            roberts_kernel_x = np.array([[1, 0], [0, -1]], dtype="int")
            roberts_kernel_y = np.array([[0, 1], [-1, 0]], dtype="int")
            roberts_edges_x = cv2.filter2D(img_cv, -1, roberts_kernel_x)
            roberts_edges_y = cv2.filter2D(img_cv, -1, roberts_kernel_y)
            roberts_edges = cv2.addWeighted(np.abs(roberts_edges_x), 0.5, np.abs(roberts_edges_y), 0.5, 0)
            cv2.imwrite(os.path.join(folder_baru, f"{nama_file}_roberts.jpg"), roberts_edges)

        if not cek_file_ada(folder_baru, nama_file, 'sobel'):
            sobel_edges_x = cv2.Sobel(img_cv, cv2.CV_64F, 1, 0, ksize=3)
            sobel_edges_y = cv2.Sobel(img_cv, cv2.CV_64F, 0, 1, ksize=3)
            sobel_edges = cv2.magnitude(sobel_edges_x, sobel_edges_y)
            sobel_edges = np.uint8(sobel_edges)
            cv2.imwrite(os.path.join(folder_baru, f"{nama_file}_sobel.jpg"), sobel_edges)

for root, dirs, files in os.walk(folder_data):
    for file in files:
        ekstensi_file = os.path.splitext(file)[1].lower()
        if ekstensi_file in ['.jpg', '.jpeg', '.png', '.heic']:
            jalur_file = os.path.join(root, file)
            folder_baru = buat_folder_baru(os.path.dirname(jalur_file), os.path.splitext(file)[0])
            proses_gambar(jalur_file, folder_baru, os.path.splitext(file)[0])

print("Pemrosesan gambar selesai.")
