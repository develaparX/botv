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
import os

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

            # Set opsi Chrome dengan optimasi untuk RAM rendah
            options = webdriver.ChromeOptions()
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-plugins-discovery')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--window-size=800,600')  # Ukuran window lebih kecil
            options.add_argument('--disable-javascript')  # Disable JS jika memungkinkan
            options.add_argument('--incognito')  # Mode incognito untuk mengurangi cache
            options.add_argument('--single-process')  # Gunakan single process
            options.add_argument('--disk-cache-size=1')  # Batasi cache
            options.add_argument('--media-cache-size=1')  # Batasi media cache
            
            # Clear /tmp sebelum menjalankan Chrome
            os.system('rm -rf /tmp/*')
            
            # Inisialisasi WebDriver dengan opsi
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # Set page load timeout
            driver.set_page_load_timeout(30)
            
            # Kunjungi halaman web
            url ="https://investsocial.com/id/forum/area-diskusi-trading/percakapan-forex-secara-keseluruhan/jurnal-trading/14282605-asrifai-s-trading-journal?p=14374418#post14374418#post14374418"
            print(f"Iterasi ke-{i+1}: Mengunjungi halaman {url}...")
            driver.get(url)

            # Tunggu sampai halaman selesai dimuat dengan timeout lebih pendek
            wait = WebDriverWait(driver, 10)  # Kurangi timeout
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

            # Scroll ke bawah dengan interval lebih lama
            print(f"Iterasi ke-{i+1}: Menggulir halaman ke bawah selama 100 detik...")
            scroll_down(driver, interval=10, duration=100)  # Interval lebih lama

            print(f"Iterasi ke-{i+1}: Tema berhasil diganti dan halaman berhasil dimuat ulang!")
            success = True

        except Exception as e:
            print(f"Iterasi ke-{i+1}: Terjadi error: {e}. Mengulangi proses dari awal...")
        
        finally:
            # Tutup browser
            driver.quit()
            # Clear memory
            os.system('sync && echo 3 > /proc/sys/vm/drop_caches')
            print(f"Iterasi ke-{i+1}: Browser ditutup.\n")
            
            # Tambahkan delay antara iterasi
            time.sleep(5)
