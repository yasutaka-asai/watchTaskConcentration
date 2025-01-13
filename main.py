from src.watchtaskconcentration.config import get_settings
from src.watchtaskconcentration.screenshot_analyzer import analyze_task_execution

def main():
    settings = get_settings()
    
    print("タスク実行状況を確認中...")
    is_task_executing = analyze_task_execution(
        api_key=settings.openai_api_key,
        task_description=settings.task_description
    )
    
    if is_task_executing:
        print("タスクが実行中です")
    else:
        print("タスクが実行されていません")

if __name__ == "__main__":
    main()
