import os
import time
from PIL import ImageGrab
from openai import OpenAI
from typing import Optional
import base64

class ScreenshotAnalyzer:
    def __init__(self, api_key: str, task_description: str):
        self.api_key = api_key
        self.task_description = task_description
        self.client = OpenAI(api_key=self.api_key)

    def capture_screenshot(self) -> str:
        """スクリーンショットを撮影して一時ファイルに保存"""
        timestamp = int(time.time())
        filename = f"screenshot_{timestamp}.png"
        # スクリーンショットを撮影し、解像度を下げる
        screenshot = ImageGrab.grab(all_screens=True)
        # マルチスクリーン対応のため、アスペクト比を維持しつつ最大幅を1600pxに制限
        width, height = screenshot.size
        if width > 1600:
            ratio = 1600 / width
            new_height = int(height * ratio)
            screenshot = screenshot.resize((1600, new_height))
        screenshot.save(filename, optimize=True, quality=85)  # 画質を調整
        return filename

    def analyze_screenshot(self, image_path: str) -> Optional[str]:
        """スクリーンショットを分析してタスク実行状況を判定"""
        try:
            with open(image_path, "rb") as image_file:
                # リトライロジックを追加
                max_retries = 3
                retry_delay = 2  # seconds
                
                for attempt in range(max_retries):
                    try:
                        response = self.client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": f"以下の画像はPC画面のスクリーンショットです。{self.task_description}を行っているか判定してください。はい/いいえで答えてください。YoutubeやSNSが写り込んでいたら「いいえ」と回答してください。"},
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                            "url": f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
                                            },
                                        },
                                    ],
                                }
                            ],
                            max_tokens=300,
                            timeout=10  # 10秒タイムアウト
                        )
                        return response.choices[0].message.content
                    except Exception as e:
                        if attempt < max_retries - 1:
                            print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                            time.sleep(retry_delay)
                            continue
                        raise e
                return response.choices[0].message.content
        except Exception as e:
            print(f"Error analyzing screenshot: {e}")
            return None

    def cleanup(self, image_path: str):
        """一時ファイルを削除"""
        try:
            os.remove(image_path)
        except OSError:
            pass

def analyze_task_execution(api_key: str, task_description: str) -> bool:
    """タスク実行状況を分析するメイン関数"""
    analyzer = ScreenshotAnalyzer(api_key, task_description)
    screenshot_path = analyzer.capture_screenshot()
    result = analyzer.analyze_screenshot(screenshot_path)
    analyzer.cleanup(screenshot_path)
    
    if result and "はい" in result:
        return True
    return False
