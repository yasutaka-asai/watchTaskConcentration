import pygame
import tkinter as tk
from tkinter import messagebox
from src.watchtaskconcentration.config import get_settings
from src.watchtaskconcentration.screenshot_analyzer import analyze_task_execution

def play_alert_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("alert.mp3")
    pygame.mixer.music.play()

def show_alert_window():
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを表示しない
    root.attributes("-topmost", True)  # 常に最前面に表示
    messagebox.showwarning(
        "タスク未実行警告",
        "タスクが実行されていません！\nすぐにタスクを開始してください。"
    )
    root.destroy()

def main():
    settings = get_settings()
    
    while True:
        print("タスク実行状況を確認中...")
        is_task_executing = analyze_task_execution(
            api_key=settings.openai_api_key,
            task_description=settings.task_description
        )
        
        if is_task_executing:
            print("タスクが実行中です")
        else:
            print("タスクが実行されていません")
            play_alert_sound()
            show_alert_window()
        
        time.sleep(10)  # 10秒間隔でチェック

if __name__ == "__main__":
    import time
    main()
