import requests

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

# Fungsi untuk mengecek proxy
def check_proxy(proxy):
    url = "http://httpbin.org/ip"  # Situs untuk mengecek IP
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

# List untuk menyimpan proxy yang valid
valid_proxies = []

# Mengecek setiap proxy dalam daftar
for proxy in proxies:
    if check_proxy(proxy):
        valid_proxies.append(proxy)

# Menulis ulang daftar proxy yang valid ke file
write_proxies(proxy_file_path, valid_proxies)

print(f"Selesai! {len(valid_proxies)} proxy yang valid disimpan kembali ke {proxy_file_path}.")
