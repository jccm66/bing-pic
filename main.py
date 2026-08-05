import os
import json
import urllib.request
from datetime import datetime

API_URL = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
BASE_URL = "https://cn.bing.com"
SAVE_DIR = "./Bing_Picture"


def download_bing_picture():
    os.makedirs(SAVE_DIR, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        req = urllib.request.Request(API_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read().decode("utf-8")

        result = json.loads(data)
        if "images" in result and len(result["images"]) > 0:
            image_info = result["images"][0]
            relative_url = image_info["url"]
            full_url = BASE_URL + relative_url
            uhd_url = full_url.replace("_1920x1080.jpg", "_UHD.jpg")

            title = image_info.get("title", "未知")
            startdate = image_info.get("startdate", "")
            safe_title = "".join([c for c in title if c.isalnum() or c in " -_"])
            filename = f"{startdate}_{safe_title}.jpg"
            save_path = os.path.join(SAVE_DIR, filename)

            img_req = urllib.request.Request(uhd_url, headers=headers)
            with urllib.request.urlopen(img_req, timeout=30) as img_response:
                with open(save_path, "wb") as f:
                    f.write(img_response.read())

            print(f"图片已成功下载到: {save_path}")
            print(f"图片标题: {image_info.get('title', '未知')}")
            print(f"图片描述: {image_info.get('copyright', '未知')}")
        else:
            print("未获取到图片信息")
    except Exception as e:
        print(f"下载失败: {str(e)}")


if __name__ == "__main__":
    download_bing_picture()