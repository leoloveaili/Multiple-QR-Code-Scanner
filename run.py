import webbrowser
import sys
import os
import time
import traceback
from datetime import datetime
from app import app

def run_app():
    try:
        print("="*50)
        print("Starting QR Scanner application...")
        print(f"Current directory: {os.getcwd()}")
        print(f"Python version: {sys.version}")
        print("="*50)
        
        # 确保上传文件夹存在
        if not os.path.exists('uploads'):
            print("Creating uploads directory...")
            os.makedirs('uploads')
        
        # 检查templates文件夹
        if not os.path.exists('templates'):
            print("ERROR: templates directory not found!")
            print("Current directory contents:")
            print(os.listdir('.'))
            raise Exception("Templates directory is missing")
        
        # 设置端口
        port = 5000
        url = f"http://127.0.0.1:{port}"
        
        print(f"Starting web server on {url}")
        
        # 延迟1秒后打开浏览器
        def open_browser():
            try:
                time.sleep(1)
                print("Opening web browser...")
                webbrowser.open(url)
            except Exception as e:
                print(f"Error opening browser: {str(e)}")
        
        # 在新线程中打开浏览器
        from threading import Timer
        Timer(1.5, open_browser).start()
        
        # 启动Flask应用
        print("Starting Flask application...")
        app.run(port=port, host='127.0.0.1')
        
    except Exception as e:
        print("\n"+"="*50)
        print("Error occurred while starting the application:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nDetailed error information:")
        traceback.print_exc()
        print("="*50)
        
        # 保持窗口打开
        input("\nPress Enter to exit...")

if __name__ == '__main__':
    try:
        run_app()
    except Exception as e:
        print("\nCritical error in main:")
        traceback.print_exc()
        input("\nPress Enter to exit...") 