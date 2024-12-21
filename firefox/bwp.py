from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from tqdm import tqdm
from yaspin import yaspin
from yaspin.spinners import Spinners
import time
import os
import subprocess
import shutil
import stat

def ensure_driver_not_busy(driver_path):
    """Memastikan driver tidak sedang digunakan"""
    try:
        # Ubah permission agar bisa dihapus
        os.chmod(driver_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        
        # Coba hapus file lama jika ada
        if os.path.exists(driver_path):
            os.remove(driver_path)
            
        # Tunggu sebentar
        time.sleep(2)
    except Exception as e:
        print(f"Warning: Failed to handle driver file: {e}")

def cleanup_environment():
    """Membersihkan environment sebelum memulai"""
    try:
        # Kill proses Firefox dan Geckodriver
        if os.name == 'posix':  # Linux/Unix
            os.system('pkill firefox')
            os.system('pkill geckodriver')
            time.sleep(2)
            os.system('killall -9 firefox')
            os.system('killall -9 geckodriver')
        elif os.name == 'nt':  # Windows
            os.system('taskkill /f /im firefox.exe')
            os.system('taskkill /f /im geckodriver.exe')
        
        # Hapus cache geckodriver
        geckodriver_cache = os.path.expanduser('~/.wdm/drivers/geckodriver')
        if os.path.exists(geckodriver_cache):
            shutil.rmtree(geckodriver_cache, ignore_errors=True)
        
        # Tunggu proses cleanup selesai
        time.sleep(3)
    except Exception as e:
        print(f"Warning: Cleanup failed: {e}")

def scroll_down(driver, interval, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(interval)

# Bersihkan environment sebelum memulai
cleanup_environment()

# Jumlah iterasi untuk progress bar
total_iterations = 73

# Download geckodriver sekali di awal
geckodriver_path = GeckoDriverManager().install()
ensure_driver_not_busy(geckodriver_path)

for i in tqdm(range(total_iterations), desc="Processing Iterations"):
    success = False
    driver = None
    while not success:
        with yaspin(Spinners.moon, text="Processing...") as spinner:
            try:
                print(f"Iterasi ke-{i+1}: Inisialisasi browser...")

                # Pastikan driver tidak sibuk
                ensure_driver_not_busy(geckodriver_path)

                # Inisialisasi UserAgent
                ua = UserAgent()
                user_agent = ua.random

                # Set opsi Firefox
                options = Options()
                options.set_preference('general.useragent.override', user_agent)
                options.add_argument('-headless')
                
                # Konfigurasi tambahan
                options.set_preference('marionette', True)
                options.set_preference('marionette.port', 0)  # Biarkan sistem memilih port
                options.set_preference('browser.cache.disk.enable', False)
                options.set_preference('browser.cache.memory.enable', False)
                options.set_preference('browser.cache.offline.enable', False)
                options.set_preference('network.http.use-cache', False)
                
                # Inisialisasi service
                service = Service(
                    executable_path=geckodriver_path,
                    log_path=os.devnull
                )

                # Inisialisasi WebDriver
                driver = webdriver.Firefox(
                    service=service,
                    options=options
                )

                # Set timeout
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(20)

                # Kunjungi halaman web
                url = "https://investsocial.com/id/forum/area-diskusi-trading/ensiklopedia-forex-kontes-jawaban-terbaik/63629-apa-itu-wppe-dalam-istilah-bei?p=14339617#post14339617#post14339617"
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

                # Scroll ke bawah selagi menunggu selama 150 detik
                print(f"Iterasi ke-{i+1}: Menggulir halaman ke bawah selama 60 detik...")
                scroll_down(driver, interval=5, duration=60)

                print(f"Iterasi ke-{i+1}: Tema berhasil diganti dan halaman berhasil dimuat ulang!")
                success = True
                spinner.ok("✔️")
            except Exception as e:
                print(f"Iterasi ke-{i+1}: Terjadi error: {e}. Mengulangi proses dari awal...")
                spinner.fail("💥")
                # Tunggu sebentar sebelum mencoba lagi
                time.sleep(5)
            finally:
                if driver:
                    try:
                        driver.quit()
                    except Exception as e:
                        print(f"Error saat menutup browser: {e}")
                    print(f"Iterasi ke-{i+1}: Browser ditutup.\n")
                    time.sleep(2)  # Tunggu sebentar sebelum iterasi berikutnya
