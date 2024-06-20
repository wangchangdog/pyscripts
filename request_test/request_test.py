import sys
import time
import requests
from datetime import datetime
from colorama import init, Fore, Style

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        return

    url = sys.argv[1]

    init(autoreset=True)

    while True:
        try:
            response = requests.get(url)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Time: {current_time} - Status Code: {response.status_code}")
            
            # 500番台のステータスコードが出た場合にベルを鳴らす
            if 500 <= response.status_code < 600:
                print('\a', end='')  # ベルを鳴らす

        except requests.exceptions.RequestException as e:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if e.response:
                print(Fore.RED + f"Time: {current_time} - Error: {e}, Status Code: {e.response.status_code}")
                # 500番台のステータスコードが出た場合にベルを鳴らす
                if 500 <= e.response.status_code < 600:
                    print('\a', end='')  # ベルを鳴らす
            else:
                print(Fore.RED + f"Time: {current_time} - Error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    main()

### コマンドプロンプトで実行する場合
# python request_test.py https://www.google.com
# 