import zipfile
import shutil
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from main import main
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from tools import utils

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class CrawlerParams(BaseModel):
    platform: str
    target_ids: list[str]


@app.post("/start-crawler")
async def start_crawler(params: CrawlerParams):
    try:
        utils.logger.info(f"Received crawler params: {params}")

        data_dir = os.path.join(os.path.dirname(__file__), "data")
        if os.path.exists(data_dir):
            shutil.rmtree(data_dir)

        await main(params.platform, params.target_ids)

        # 删除 data.zip 文件（如果存在）
        zip_file_path = os.path.join(os.path.dirname(__file__), "data.zip")
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)

        # 打包 data 文件夹为压缩文件
        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(data_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, data_dir)
                    zipf.write(file_path, arcname)

        # 返回 blob 类型数据
        def iterfile():
            with open(zip_file_path, mode="rb") as file_like:
                yield from file_like

        return StreamingResponse(
            iterfile(),
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=data.zip"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
