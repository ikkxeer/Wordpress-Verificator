import requests
import concurrent.futures
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def check_wordpress(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, "html.parser")

            if "wp-content" in content or "wp-includes" in content:
                return True
            if "wp-login.php" in content or "wp-admin" in content:
                return True

            generator_meta = soup.find("meta", {"name": "generator"})
            if generator_meta and "WordPress" in generator_meta.get("content", "").lower():
                return True
            if soup.find("link", {"rel": "stylesheet", "href": "/wp-content/"}):
                return True
            if soup.find("link", {"rel": "stylesheet", "href": "/wp-includes/"}):
                return True
    except requests.RequestException:
        pass
    return False

def check_wordpress_gui():
    url_to_check = url_entry.get()
    result_label.config(text="Verificando...", fg="black")
    check_button.config(state="disabled")

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(check_wordpress, url_to_check)
        future.result()

        if future.result():
            result_label.config(text="El sitio está construido con WordPress.", fg="green")
        else:
            result_label.config(text="El sitio no parece estar construido con WordPress.", fg="red")

        check_button.config(state="normal")

window = tk.Tk()
window.title("Verificar WordPress")
window.geometry("400x200")

font_style = ("Helvetica", 12)
bg_color = "#f0f0f0"

url_label = tk.Label(window, text="Escriba la URL:", font=font_style, bg=bg_color)
url_label.pack(pady=10)
url_entry = tk.Entry(window, width=40, font=font_style)
url_entry.pack()

check_button = tk.Button(window, text="Verificar", overrelief="flat", borderwidth=1, font=font_style, command=check_wordpress_gui)
check_button.pack(pady=10)

result_label = tk.Label(window, text="", font=font_style, bg=bg_color)
result_label.pack()

window.mainloop()
