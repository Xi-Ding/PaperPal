import requests
import json
import os

# 从环境变量或直接配置中获取 Bright Data API 凭证
# 注意：API Token 通常可以在 Bright Data 控制台的 "API Tokens" 页面找到
API_TOKEN = "your_bright_data_api_token"  # 建议从环境变量读取
COLLECTION_ID = "your_collection_id"      # 如果是使用 Dataset/Scraper API

def trigger_scraper(url):
    """
    使用 Bright Data 的 Web Scraper API (Trigger)
    """
    endpoint = f"https://api.brightdata.com/datasets/v3/trigger?dataset_id={COLLECTION_ID}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = [
        {"url": url}
    ]
    
    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        snapshot_id = response.json().get("snapshot_id")
        print(f"🚀 抓取任务已启动，Snapshot ID: {snapshot_id}")
        return snapshot_id
    else:
        print(f"❌ 启动失败: {response.text}")
        return None

def get_scraper_result(snapshot_id):
    """
    获取抓取结果
    """
    endpoint = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"⏳ 结果尚未就绪或获取失败 (Status: {response.status_code})")
        return None

if __name__ == "__main__":
    # 示例用法
    # sid = trigger_scraper("https://www.dmit.io/clientarea.php")
    # if sid:
    #     result = get_scraper_result(sid)
    #     print(json.dumps(result, indent=2, ensure_ascii=False))
    print("请在脚本中配置 API_TOKEN 和 COLLECTION_ID 后运行")
