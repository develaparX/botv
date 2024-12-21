from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from tqdm import tqdm
import time
import random

def scroll_down(driver, interval, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(interval)

# Jumlah iterasi untuk progress bar
total_iterations = 86

for i in tqdm(range(total_iterations), desc="Processing Iterations"):
    success = False
    while not success:
        try:
            print(f"Iterasi ke-{i+1}: Inisialisasi browser...")
            
            # Inisialisasi UserAgent
            ua = UserAgent()
            user_agent = ua.random

            # Set opsi Chrome dengan UserAgent palsu dan mode headless
            options = webdriver.ChromeOptions()
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument('--headless')  # Menjalankan Chrome dalam mode headless
            options.add_argument('--disable-gpu')  # Opsi tambahan yang direkomendasikan
            options.add_argument('--window-size=1920,1080')  # Set ukuran jendela untuk mode headless
            options.add_argument('--no-sandbox')  # Mengatasi beberapa masalah saat dijalankan di lingkungan tanpa GUI
            options.add_argument('--disable-dev-shm-usage')  # Mengatasi masalah memori bersama

            # Inisialisasi WebDriver dengan opsi
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # Kunjungi halaman web
            url ="https://investsocial.com/id/forum/area-diskusi-trading/percakapan-forex-secara-keseluruhan/jurnal-trading/14282605-asrifai-s-trading-journal?p=14374418#post14374418#post14374418"
            print(f"Iterasi ke-{i+1}: Mengunjungi halaman {url}...")
            driver.get(url)

            # Tunggu sampai halaman selesai dimuat
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print(f"Iterasi ke-{i+1}: Halaman berhasil dimuat.")

            # Tunggu sampai tombol tutup iklan muncul dan kemudian tutup iklan
            print(f"Iterasi ke-{i+1}: Menunggu tombol tutup iklan...")
            close_ad_button = wait.until(EC.element_to_be_clickable((By.ID, "pb-btn-close")))
            close_ad_button.click()
            print(f"Iterasi ke-{i+1}: Iklan berhasil ditutup.")

            # Tunggu sampai elemen div yang diinginkan dapat diklik
            print(f"Iterasi ke-{i+1}: Menunggu elemen div dapat diklik...")
            div_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.js-stylechooser.cursor-pointer.ml-2")))

            # Gulir ke elemen div agar terlihat
            driver.execute_script("arguments[0].scrollIntoView();", div_element)
            print(f"Iterasi ke-{i+1}: Elemen div ditemukan dan digulir ke tampilan.")

            # Temukan elemen <a> di dalam elemen div dan klik elemen tersebut
            style_chooser = div_element.find_element(By.CSS_SELECTOR, "a.flex.items-center.h-full.hover\\:text-white.focus\\:text-white.cursor-pointer")
            style_chooser.click()
            print(f"Iterasi ke-{i+1}: Elemen div berhasil diklik.")

            # Tunggu sampai halaman selesai memuat data setelah klik elemen
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Scroll ke bawah selagi menunggu selama 100 detik
            print(f"Iterasi ke-{i+1}: Menggulir halaman ke bawah selama 100 detik...")
            scroll_down(driver, interval=5, duration=100)

            print(f"Iterasi ke-{i+1}: Tema berhasil diganti dan halaman berhasil dimuat ulang!")
            success = True
        
        except Exception as e:
            print(f"Iterasi ke-{i+1}: Terjadi error: {e}. Mengulangi proses dari awal...")
        
        finally:
            # Tutup browser
            driver.quit()
            print(f"Iterasi ke-{i+1}: Browser ditutup.\n")
