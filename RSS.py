import tkinter as tk
from tkinter import ttk, scrolledtext
import feedparser
import threading
import webbrowser
import datetime

# 配色方案
PRIMARY_COLOR = "#282c34"
SECONDARY_COLOR = "#61afef"
TEXT_COLOR = "#abb2bf"
BACKGROUND_COLOR = "#1c1e24"
BUTTON_COLOR = "#61afef"
BUTTON_HOVER_COLOR = "#528bcf"

# RSS 來源 URL
rss_feeds = {
    "TechNews": "https://technews.tw/feed/",
    "iThome": "https://www.ithome.com.tw/rss",
    "Techmeme": "https://www.techmeme.com/feed.xml"
}

# 日期格式化函數
def format_pub_date(pub_date):
    possible_formats = ['%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d %H:%M:%S']
    for fmt in possible_formats:
        try:
            return datetime.datetime.strptime(pub_date, fmt).strftime('%Y-%m-%d(%a)')  # 這裡使用 datetime.datetime
        except ValueError:
            continue
    return pub_date


# 抓取 RSS feed 資料
def fetch_rss_feed(feed_url):
    articles = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        pub_date = entry.get('published', '無日期')
        formatted_date = format_pub_date(pub_date)
        articles.append((entry.title, entry.link, formatted_date))
    return articles

# 顯示文章內容
def display_articles(articles):
    text_area.delete('1.0', tk.END)
    for title, link, pub_date in articles:
        text_area.insert(tk.END, f"標題: {title}\n", "title")
        text_area.insert(tk.END, f"發佈日期: {pub_date}\n", "date")
        text_area.insert(tk.END, f"連結: {link}\n{'-'*40}\n", "link")

# 更新 RSS feed
def update_feed():
    try:
        selected_feed = feed_var.get()
        feed_url = rss_feeds[selected_feed]
        articles = fetch_rss_feed(feed_url)
        display_articles(articles)
        update_status("RSS Feed 更新成功")
    except Exception as e:
        update_status(f"RSS Feed 更新失敗: {str(e)}")

# 更新狀態欄
def update_status(message):
    status_label.config(text=message)

# 點擊顯示文章內容並在瀏覽器中打開連結
def open_link(event):
    index = text_area.index(tk.CURRENT)
    line = text_area.get(f"{index} linestart", f"{index} lineend")
    if line.startswith("連結:"):
        url = line.replace("連結: ", "").strip()
        webbrowser.open(url)

# 多執行緒抓取 RSS 資料
def fetch_feed_in_thread():
    threading.Thread(target=update_feed).start()

# 設計改進的主視窗
root = tk.Tk()
root.title("RSS 資訊聚合器")
root.geometry("1000x700")
root.configure(bg=PRIMARY_COLOR)

# 設定字體
font_title = ("Noto Sans", 20, "bold")
font_text = ("Noto Sans", 16)
font_button = ("Noto Sans", 14)

# 左側主框架
left_frame = tk.Frame(root, bg=PRIMARY_COLOR)
left_frame.pack(side="left", fill="both", expand=True)

# 標題標籤
title_label = tk.Label(left_frame, text="RSS Reader", font=font_title, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, pady=20)
title_label.pack(fill="x")

# 篩選 RSS 功能
filter_frame = tk.Frame(left_frame, bg=PRIMARY_COLOR)
filter_frame.pack(pady=10)

feed_var = tk.StringVar(value="TechNews")
category_menu = ttk.Combobox(filter_frame, textvariable=feed_var, values=list(rss_feeds.keys()), font=font_text)
category_menu.grid(row=0, column=1, padx=10)
category_menu.bind("<<ComboboxSelected>>", lambda event: fetch_feed_in_thread())

# 顯示區域 - 調整大小和設計
text_area = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=90, height=25, font=font_text, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
text_area.pack(pady=20, fill="both", expand=True)


# 狀態欄
status_label = tk.Label(left_frame, text="準備就緒", font=font_text, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR)
status_label.pack(fill="x", pady=5)

# 綁定雙擊事件打開連結
text_area.bind("<Double-1>", open_link)

# 設定顯示區域的格式
# 設置背景和文字的顏色對比
text_area.configure(bg="#000000", fg="#FFFFFF")  # 深藍背景，淺黃色文字
text_area.tag_configure("title", font=("Noto Sans", 16, "bold"), foreground="#FFFFFF", spacing3=15)  # 白色標題

# 初始化顯示
fetch_feed_in_thread()

# 進入 Tkinter 主循環
root.mainloop()
