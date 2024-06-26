import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog


def filter_files_with_content(src, content):
    # 使用正則表達式來過濾檔案
    pattern = re.compile(content)
    files = [f for f in os.listdir(src) if pattern.search(f)]
    return files


def move_files_with_content(src, dst, content, progress):
    # 檢查目標資料夾是否存在，不存在則創建
    if not os.path.exists(dst):
        os.makedirs(dst)

    files = filter_files_with_content(src, content)
    total_files = len(files)

    for i, filename in enumerate(files, 1):
        shutil.move(os.path.join(src, filename), os.path.join(dst, filename))
        progress["value"] = (i / total_files) * 100
        window.update_idletasks()

    messagebox.showinfo("完成", "所有檔案搬移完成！")


def copy_files_with_content(src, dst, content, progress):
    if not os.path.exists(dst):
        os.makedirs(dst)

    files = filter_files_with_content(src, content)
    total_files = len(files)

    for i, filename in enumerate(files, 1):
        if os.path.exists(os.path.join(dst, filename)):
            # 如果檔案或目錄已經存在於目標資料夾，則跳過這個檔案或目錄
            continue
        full_path = os.path.join(src, filename)
        if os.path.isfile(full_path):
            shutil.copy(full_path, os.path.join(dst, filename))
        elif os.path.isdir(full_path):
            shutil.copytree(full_path, os.path.join(dst, filename))
        progress["value"] = (i / total_files) * 100
        window.update_idletasks()

    messagebox.showinfo("完成", "所有檔案與目錄複製完成！")


def delete_files_with_content(src, content, progress):
    files = filter_files_with_content(src, content)
    total_files = len(files)

    # 詢問是否確定刪除
    message = f"你現在要刪除的是「{src}」中關鍵字為「{content}」的文件，這個操作會讓你永久刪除此檔案，確定要刪除嗎？"
    answer = messagebox.askquestion("確認", message, icon="warning")
    if answer == "yes":
        for i, filename in enumerate(files, 1):
            full_path = os.path.join(src, filename)
            # 判斷是檔案還是資料夾，選擇適當的方法來刪除
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
            progress["value"] = (i / total_files) * 100
            window.update_idletasks()

        messagebox.showinfo("完成", "所有檔案及資料夾刪除完成！")
    else:
        messagebox.showinfo("取消", "操作已取消！")


def rename_files_with_content(src, old_content, new_content, progress):
    files = filter_files_with_content(src, old_content)
    total_files = len(files)

    for i, filename in enumerate(files, 1):
        old_path = os.path.join(src, filename)
        new_name = filename.replace(old_content, new_content)
        new_path = os.path.join(src, new_name)
        os.rename(old_path, new_path)
        progress["value"] = (i / total_files) * 100
        window.update_idletasks()

    messagebox.showinfo("完成", "所有檔案及資料夾重新命名完成！")


def number_files(src, progress):
    files = [f for f in os.listdir(
        src) if os.path.isfile(os.path.join(src, f))]
    total_files = len(files)

    for i, filename in enumerate(files, 1):
        file_extension = os.path.splitext(filename)[1]
        new_name = f"{i}{file_extension}"
        old_path = os.path.join(src, filename)
        new_path = os.path.join(src, new_name)
        os.rename(old_path, new_path)
        progress["value"] = (i / total_files) * 100
        window.update_idletasks()

    messagebox.showinfo("完成", "所有檔案已編號完成！")


def browse_directory():
    folder_selected = filedialog.askdirectory()
    return folder_selected


def create_gui():
    global window
    window = tk.Tk()
    window.title("檔案管理工具")

    tk.Label(window, text="源資料夾:").grid(row=0)
    tk.Label(window, text="目標資料夾:").grid(row=1)
    tk.Label(window, text="檔案關鍵字/正則表達式:").grid(row=2)

    src_entry = tk.Entry(window)
    dst_entry = tk.Entry(window)
    content_entry = tk.Entry(window)

    src_entry.grid(row=0, column=1)
    dst_entry.grid(row=1, column=1)
    content_entry.grid(row=2, column=1)

    src_browse_button = tk.Button(
        window,
        text="瀏覽",
        command=lambda: [
            src_entry.delete(0, tk.END),
            src_entry.insert(0, browse_directory()),
        ],
    )
    dst_browse_button = tk.Button(
        window,
        text="瀏覽",
        command=lambda: [
            dst_entry.delete(0, tk.END),
            dst_entry.insert(0, browse_directory()),
        ],
    )

    src_browse_button.grid(row=0, column=2)
    dst_browse_button.grid(row=1, column=2)

    progress = ttk.Progressbar(window, length=200, mode="determinate")
    progress.grid(row=7, column=0, columnspan=3, pady=10)

    move_button = tk.Button(
        window,
        text="搬移檔案",
        command=lambda: move_files_with_content(
            src_entry.get(), dst_entry.get(), content_entry.get(), progress
        ),
    )
    move_button.grid(row=4, column=0, pady=10)

    copy_button = tk.Button(
        window,
        text="複製檔案",
        command=lambda: copy_files_with_content(
            src_entry.get(), dst_entry.get(), content_entry.get(), progress
        ),
    )
    copy_button.grid(row=4, column=1, pady=10)

    delete_button = tk.Button(
        window,
        text="刪除檔案",
        command=lambda: delete_files_with_content(
            src_entry.get(), content_entry.get(), progress
        ),
    )
    delete_button.grid(row=5, column=0, pady=10)

    rename_button = tk.Button(
        window,
        text="修改名稱",
        command=lambda: rename_files_with_content(
            src_entry.get(),
            content_entry.get(),
            simpledialog.askstring("輸入新名稱", "請輸入新的文字："),
            progress,
        ),
    )
    rename_button.grid(row=5, column=1, pady=10)

    number_button = tk.Button(
        window,
        text="編號檔案",
        command=lambda: number_files(src_entry.get(), progress),
    )
    number_button.grid(row=6, column=0, columnspan=2, pady=10)

    window.mainloop()


create_gui()
