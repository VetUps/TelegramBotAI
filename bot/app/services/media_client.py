import asyncio
import httpx
from config import config

async def generate_image_bytes(prompt: str) -> bytes | str:
    """Генерирует картинку, скачивает её и возвращает байты. При ошибке возвращает строку с описанием."""
    url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
    
    headers = {
        "Authorization": f"Bearer {config.QWEN_API}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "wan2.2-t2i-plus",
        "input": {
            "messages": [{
                "role": "user",
                "content": [{"text": prompt}]
            }]
        },
        "parameters": {
            "size": "2048*2048",
            "n": 1
        }
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
                                            
            response = await client.post(url, json=payload, headers=headers)
            data = response.json()

            if "output" not in data:
                return f"error: DashScope API Error {data}"

            content0 = data["output"]["choices"][0]["message"]["content"][0]
            image_url = content0.get("image") or content0.get("image_url") or content0.get("url")
            
            if not image_url:
                return f"error: Не нашел ссылку на картинку в ответе: {content0}"

                                         
            image_response = await client.get(image_url, timeout=60.0)
            if image_response.status_code != 200:
                 return f"error: Не удалось скачать картинку по ссылке. Статус: {image_response.status_code}"
            
            return image_response.content

        except Exception as e:
            return f"error: {e}"

async def generate_video_bytes(prompt: str) -> bytes | str:
    """Генерирует видео, дожидается готовности, скачивает и возвращает байты."""
    base_url = "https://dashscope-intl.aliyuncs.com/api/v1"
    create_url = f"{base_url}/services/aigc/video-generation/video-synthesis"
    task_url_template = f"{base_url}/tasks/{{task_id}}"

    headers_create = {
        "Authorization": f"Bearer {config.QWEN_API}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }
    
    headers_task = {
        "Authorization": f"Bearer {config.QWEN_API}",
    }

    payload = {
        "model": "wan2.6-t2v",
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "resolution": "720P", 
            "duration": 10,
            "prompt_extend": True,
            "shot_type": "single",
        }
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
                               
            r_create = await client.post(create_url, json=payload, headers=headers_create)
            data_create = r_create.json()
            
            if "output" not in data_create or "task_id" not in data_create["output"]:
                return f"error: Task create failed: {data_create}"

            task_id = data_create["output"]["task_id"]

                                            
            video_url = None
            while True:
                task_url = task_url_template.format(task_id=task_id)
                tr = await client.get(task_url, headers=headers_task)
                tdata = tr.json()

                output = tdata.get("output", {})
                status = output.get("task_status")

                if status == "SUCCEEDED":
                    video_url = output.get("video_url")
                    if not video_url:
                        return f"error: SUCCEEDED, but no video_url: {tdata}"
                    break

                if status in ("FAILED", "CANCELED", "UNKNOWN"):
                    return f"error: Task ended with status={status}: {tdata}"

                await asyncio.sleep(15)

                                         
            if video_url:
                 video_response = await client.get(video_url, timeout=300.0)
                 if video_response.status_code != 200:
                     return f"error: Не удалось скачать видео по ссылке. Статус: {video_response.status_code}"
                 return video_response.content
            return "error: Неизвестная ошибка при получении видео."

        except Exception as e:
            return f"error: {e}"