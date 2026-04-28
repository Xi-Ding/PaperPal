from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import time
import uvicorn

app = FastAPI(title="SMS Relay Server")

# 统一 API Key 配置
API_KEY = "webmonitor_secure_v1"
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# 简单的内存存储
sms_store = {}
cookie_store = {}

async def get_api_key(header_key: str = Security(api_key_header)):
    if header_key == API_KEY:
        return header_key
    raise HTTPException(status_code=403, detail="Invalid API Key")

class SMSPayload(BaseModel):
    service: str
    code: str

class CookiePayload(BaseModel):
    service: str
    cookies: dict

@app.post("/cookie", dependencies=[Depends(get_api_key)])
async def receive_cookie(payload: CookiePayload):
    """接收来自手机端的登录 Cookies"""
    cookie_store[payload.service] = {
        "cookies": payload.cookies,
        "timestamp": time.time()
    }
    print(f"Received updated cookies for {payload.service}")
    return {"status": "success"}

@app.get("/cookie/{service}", dependencies=[Depends(get_api_key)])
async def get_cookie(service: str):
    """获取存储的 Cookies"""
    data = cookie_store.get(service)
    if not data:
        raise HTTPException(status_code=404, detail="No cookies found")
    return data

@app.post("/sms", dependencies=[Depends(get_api_key)])
async def receive_sms(payload: SMSPayload):
    """接收来自 iOS/Android 的验证码"""
    sms_store[payload.service] = {
        "code": payload.code,
        "timestamp": time.time()
    }
    print(f"Received code for {payload.service}: {payload.code}")
    return {"status": "success"}

@app.get("/sms/{service}", dependencies=[Depends(get_api_key)])
async def get_sms(service: str, max_age: int = 300):
    """获取验证码 (带有效期检查)"""
    data = sms_store.get(service)
    if not data:
        raise HTTPException(status_code=404, detail="No code found")
    
    if time.time() - data["timestamp"] > max_age:
        raise HTTPException(status_code=410, detail="Code expired")
        
    return {"code": data["code"], "timestamp": data["timestamp"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
