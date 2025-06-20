import logging

def get_logger(name: str):
    # สร้าง logger object โดยใช้ชื่อที่ระบุ
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # ตรวจสอบว่ามี handler อยู่แล้วหรือยัง เพื่อไม่ให้เพิ่มซ้ำ
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
