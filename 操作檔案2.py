import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def move_files_with_prefix(src, dst, prefix, progress):
    # 檢查目標資料夾是否存在，不存在則創建
    if not os.path.exists(dst):
        os.makedirs(dst)

    pattern = re.compile(prefix)
    files = [f for f in os.listdir(src) if pattern.match(f)]
    total_files = len(files)

    for i, filename in enumerate(files, 1):
        shutil.move(os.path.join(src, filename), os.path.join(dst, filename))
        progress['value'] = (i / total_files) * 100
        window.update_idletasks()

    messagebox.showinfo("完成", "所有檔案搬移完成！")

def browse_directory():
    folder_selected = filedialog.askdirectory()
    return folder_selected

def create_gui():
    global window
    window = tk.Tk()
    window.title("檔案搬移工具")

    tk.Label(window, text="源資料夾:").grid(row=0)
    tk.Label(window, text="目標資料夾:").grid(row=1)
    tk.Label(window, text="檔案前綴/正則表達式:").grid(row=2)

    src_entry = tk.Entry(window)
    dst_entry = tk.Entry(window)
    prefix_entry = tk.Entry(window)

    src_entry.grid(row=0, column=1)
    dst_entry.grid(row=1, column=1)
    prefix_entry.grid(row=2, column=1)

    src_browse_button = tk.Button(window, text="瀏覽", command=lambda: src_entry.insert(0, browse_directory()))
    dst_browse_button = tk.Button(window, text="瀏覽", command=lambda: dst_entry.insert(0, browse_directory()))

    src_browse_button.grid(row=0, column=2)
    dst_browse_button.grid(row=1, column=2)

    progress = ttk.Progressbar(window, length=200, mode='determinate')
    progress.grid(row=4, column=0, columnspan=3, pady=10)

    move_button = tk.Button(window, text="搬移檔案", command=lambda: move_files_with_prefix(src_entry.get(), dst_entry.get(), prefix_entry.get(), progress))
    move_button.grid(row=3, column=1, pady=10)

    window.mainloop()

create_gui()
