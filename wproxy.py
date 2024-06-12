from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import requests
import time
import random

# Fungsi untuk membaca proxy dari file
def read_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

# Fungsi untuk menulis ulang proxy yang valid ke file
def write_proxies(file_path, proxies):
    with open(file_path, 'w') as file:
        for proxy in proxies:
            file.write(f"{proxy}\n")

# Fungsi untuk mengecek apakah proxy berfungsi
def check_proxy(proxy):
    url = "http://httpbin.org/ip"
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }

    try:
        response = requests.get(url, proxies=proxy_dict, timeout=1000)
        if response.status_code == 200:
            print(f"Proxy {proxy} berfungsi dengan baik. IP: {response.json()['origin']}")
            return True
        else:
            print(f"Proxy {proxy} tidak berfungsi. Status kode: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Proxy {proxy} tidak berfungsi. Error: {e}")
        return False

# File path ke proxy.txt
proxy_file_path = 'proxy.txt'

# Membaca daftar proxy dari file
proxies = read_proxies(proxy_file_path)

def scroll_down(driver, interval, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(interval)

# Daftar proxy yang valid
valid_proxies = []

for i in range(100):
    success = False
    while not success:
        proxy = None
        driver = None
        try:
            # Memilih proxy secara acak
            proxy = random.choice(proxies)
            print(f"Menggunakan proxy: {proxy}")

            # Cek apakah proxy berfungsi
            if not check_proxy(proxy):
                proxies.remove(proxy)
                continue

            # Inisialisasi UserAgent
            ua = UserAgent()
            user_agent = ua.random

            # Set opsi Chrome dengan UserAgent palsu dan proxy
            options = webdriver.ChromeOptions()
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument(f'--proxy-server=http://{proxy}')

            # Inisialisasi WebDriver dengan opsi
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # Kunjungi halaman web
            url = "https://investsocial.com/id/forum/area-diskusi-trading/percakapan-forex-secara-keseluruhan/jurnal-trading/14185943-arunikax-s-trading-journal?goto=newpost"
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
            if proxy:
                proxies.remove(proxy)

        finally:
            if driver:
                driver.quit()

# Menyimpan proxy yang valid kembali ke file
write_proxies(proxy_file_path, proxies)

print(f"Selesai! Proxy yang valid disimpan kembali ke {proxy_file_path}.")
