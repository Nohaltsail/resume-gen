import base64
import os


def save_photo(photo_base64: str, resume_id: str):
    img_bytes = base64.b64decode(photo_base64)
    filename = f"{resume_id}.png"
    file_path = os.path.join(r'../avatar', filename)
    with open(file_path, "wb") as f:
        f.write(img_bytes)

    return os.path.abspath(file_path)


def get_photo(resume_id: str):
    filename = f"{resume_id}.png"
    file_path = os.path.join(r'../avatar', filename)
    if os.path.exists(file_path):
        return file_path
    return None


def file_to_base64(abs_path: str) -> str:
    """把磁盘文件读成 base64 字符串（不含 data: 前缀）"""
    if not abs_path or not os.path.isfile(abs_path):
        return ""
    with open(abs_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
