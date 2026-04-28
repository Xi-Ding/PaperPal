import asyncio
from playwright.async_api import async_playwright
import httpx
import time
import os
import json
import re

# 配置
API_KEY_HEADER = "webmonitor_secure_v1"
# 亮数据连接参数
BRD_PW = "eokmdb0tf7wp"
BRD_USER = "brd-customer-hl_7bccbe55-zone-scraping_browser1"
SBR_WS_ENDPOINT = f"wss://{BRD_USER}:{BRD_PW}@brd.superproxy.io:9222"

async def dmit_dna_extract(page, label):
    """
    基于用户提供的 HTML 结构 DNA 进行智能提取。
    """
    js_payload = """
    () => {
        // 1. 等待 Vue App 加载（检测加载 SVG 是否消失）
        const app = document.querySelector('#dmit_vm_app');
        if (!app || app.innerHTML.includes('loading-iI5cY85G.svg')) return null;

        // 2. DNA 特征寻找
        // 寻找包含特定背景渐变色的蓝色卡片 (这是 208GB 数据的专属容器)
        const blueCard = document.querySelector('.dmit-from-blue-50');
        if (blueCard) {
            const val = blueCard.querySelector('.dmit-text-2xl.dmit-font-bold');
            const unit = blueCard.querySelector('.dmit-text-sm');
            if (val) {
                return (val.innerText + ' ' + (unit ? unit.innerText : '')).trim();
            }
        }

        // 备选方案：全页面寻找第一个符合 2xl 样式的数值块
        const allBold = document.querySelectorAll('.dmit-text-2xl.dmit-font-bold');
        if (allBold.length > 0) return allBold[0].innerText;

        return null;
    }
    """
    # 轮询探测，给 Vue 渲染留出 40 秒的最长等待时间
    for i in range(20):
        try:
            val = await page.evaluate(js_payload)
            if val and len(val) > 0:
                return val, "dna_match"
        except: pass
        await asyncio.sleep(2)
    
    return "获取超时 (Vue渲染慢)", "failed"

async def run_tracker():
    async with async_playwright() as p:
        print(f"🚀 [Scraping Browser] DNA 模式启动于 {time.ctime()}...")
        try:
            browser = await p.chromium.connect_over_cdp(SBR_WS_ENDPOINT)
            context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        except Exception as e:
            print(f"❌ 亮数据连接失败: {e}")
            return

        # 获取任务 (直接连接本地 8000 端口，避开 Nginx)
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get("http://127.0.0.1:8000/data", headers={"X-API-Key": API_KEY_HEADER})
                db_data = resp.json()
        except Exception as e:
            print(f"❌ 无法连接本地后端: {e}")
            await browser.close()
            return

        all_cookies = db_data.get("cookies", {})
        all_tasks = db_data.get("tasks", {})

        for service, cookie_info in all_cookies.items():
            tasks = all_tasks.get(service, {})
            if not tasks: continue
            
            page = await context.new_page()
            results = {}
            
            try:
                print(f"[{service}] 正在同步 Session...")
                await page.goto("https://www.dmit.io/", wait_until="commit")
                for name, value in cookie_info["data"].items():
                    await page.evaluate(f"document.cookie='{name}={value}; domain=.dmit.io; path=/; secure'")
                
                for label, task_info in tasks.items():
                    target_url = task_info.get("url") if isinstance(task_info, dict) else "https://www.dmit.io/clientarea.php"
                    
                    print(f"🌐 跳转并等待渲染: {target_url}")
                    # 使用 commit 模式进入，然后通过 DNA 函数进行轮询探测
                    await page.goto(target_url, wait_until="commit")
                    
                    val, method = await dmit_dna_extract(page, label)
                    results[label] = val
                    print(f"📊 {label} = {val} ({method})")
                
                if results:
                    async with httpx.AsyncClient() as client:
                        await client.post("http://127.0.0.1:8000/update_result", 
                                        headers={"X-API-Key": API_KEY_HEADER},
                                        json={"service": service, "data": results})
                        print(f"✅ 数据已传回: {results}")

            except Exception as e:
                print(f"❌ 运行异常: {e}")
            finally:
                await page.close()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_tracker())
