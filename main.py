from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import random

def scroll_down(driver, interval, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(interval)

for i in range(86):
    success = False
    while not success:
        try:
            # Inisialisasi UserAgent
            ua = UserAgent()
            user_agent = ua.random

            # Set opsi Chrome dengan UserAgent palsu
            options = webdriver.ChromeOptions()
            options.add_argument(f'user-agent={user_agent}')

            # Inisialisasi WebDriver dengan opsi
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # Set ukuran dan posisi jendela yang acak
            width = random.randint(800, 1200)  # Lebar acak antara 800 dan 1200 piksel
            height = random.randint(600, 900)  # Tinggi acak antara 600 dan 900 piksel
            x_position = random.randint(0, 300)  # Posisi X acak antara 0 dan 300 piksel
            y_position = random.randint(0, 200)  # Posisi Y acak antara 0 dan 200 piksel

            driver.set_window_size(width, height)
            driver.set_window_position(x_position, y_position)

            # Kunjungi halaman web
            url = "https://investsocial.com/id/forum/area-diskusi-trading/percakapan-forex-secara-keseluruhan/jurnal-trading/14282605-asrifai-s-trading-journal/page2#post14291345"
            driver.get(url)

            # Tunggu sampai halaman selesai dimuat
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Tunggu sampai tombol tutup iklan muncul dan kemudian tutup iklan
            close_ad_button = wait.until(EC.element_to_be_clickable((By.ID, "pb-btn-close")))
            close_ad_button.click()

            # Tunggu sampai elemen div yang diinginkan dapat diklik
            div_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.js-stylechooser.cursor-pointer.ml-2")))

            # Gulir ke elemen div agar terlihat
            driver.execute_script("arguments[0].scrollIntoView();", div_element)

            # Temukan elemen <a> di dalam elemen div dan klik elemen tersebut
            style_chooser = div_element.find_element(By.CSS_SELECTOR, "a.flex.items-center.h-full.hover\\:text-white.focus\\:text-white.cursor-pointer")
            style_chooser.click()

            # Tunggu sampai halaman selesai memuat data setelah klik elemen
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Scroll ke bawah selagi menunggu selama 60 detik
            scroll_down(driver, interval=5, duration=200)

            print(f"Tema berhasil diganti dan halaman berhasil dimuat ulang! Iterasi ke-{i+1}")
            success = True
        
        except Exception as e:
            print(f"Terjadi error: {e}. Mengulangi proses dari awal...")
        
        finally:
            # Tutup browser
            driver.quit()
