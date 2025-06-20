#import time
#ไม่ได้ใช้ time sleep แล้วเพราะว่า set slow mo ไว้แล้วใน conftest

from playwright.sync_api import sync_playwright, expect
# 🔹 นำเข้า sync_playwright สำหรับรัน Playwright แบบ synchronous
# 🔹 นำเข้า expect สำหรับทำ assertion (ตรวจสอบว่าเงื่อนไขต่างๆ เป็นจริง)

def test_prices_sorted_ascending(page, logger):
    # 🔹 ฟังก์ชันทดสอบชื่อว่า test_prices_sorted_ascending
    # 🔹 Pytest จะส่ง `page` (browser tab) เข้ามาให้จาก fixture อัตโนมัติ

    # Login เข้าระบบ
    page.goto("https://www.saucedemo.com/v1/index.html")
    # 🔹 เปิดหน้า login ของ saucedemo
    page.fill("#user-name", "standard_user")
    # 🔹 กรอก username โดยใช้ id selector `#user-name`
    page.fill("#password", "secret_sauce")
    # 🔹 กรอก password โดยใช้ id selector `#password`
    page.click("#login-button")
    # 🔹 คลิกปุ่ม login เพื่อเข้าสู่ระบบ

    # รอให้โหลดหน้า inventory
    expect(page).to_have_url("https://www.saucedemo.com/v1/inventory.html")
    # 🔹 ตรวจสอบว่าหลัง login แล้วเปลี่ยนหน้ามาที่ inventory
    # 🔹 หากยังไม่เปลี่ยน จะรอจนกว่าหน้าโหลดเสร็จ (timeout ถ้านานเกิน)

    # 🔻 เลือก Price (low to high)
    page.select_option(".product_sort_container", "lohi")

    # ดึงราคาของสินค้าทั้งหมด (ใน order ที่ปรากฏใน DOM)
    price_elements = page.locator(".inventory_item_price")
    # 🔹 หา element ทั้งหมดที่มี class = "inventory_item_price"
    # 🔹 จะได้ Locator group ที่รวมราคาของสินค้าทั้งหมด
    prices = []
    # 🔹 เตรียม list ว่างไว้เก็บราคาสินค้าในรูปแบบ float
    count = price_elements.count()
    # 🔹 นับจำนวนราคาทั้งหมด (เช่น อาจมี 6 ชิ้น → count = 6)
    for i in range(count):
        # 🔹 วนลูปตามจำนวนสินค้า
        price_text = price_elements.nth(i).inner_text()  # เช่น "$29.99"
        # 🔹 ดึงข้อความของราคาชิ้นที่ i (เช่น "$9.99")
        price_value = float(price_text.replace("$", ""))
        # 🔹 ลบ `$` ออกจาก string แล้วแปลงเป็น float (เช่น "$29.99" → 29.99)
        prices.append(price_value)
        # 🔹 เพิ่มราคาที่แปลงแล้วลงใน list prices
    # ตรวจสอบว่าราคาเรียงจากน้อยไปมาก
    assert prices == sorted(prices), f"ราคาสินค้าไม่เรียงจากน้อยไปมาก: {prices}"
    # 🔹 ตรวจสอบว่า list prices มีค่าตรงกับ version ที่ sort แล้ว (ascending)
    # 🔹 ถ้าไม่ตรง → แปลว่าราคาบางชิ้นเรียงผิด จะเกิด AssertionError และแสดงราคาทั้งหมด
    logger.info(f"[LOW→HIGH] ราคาที่ได้จากหน้าเว็บ: {prices}")

    # 🔻 เลือก Price (high to low)
    page.select_option(".product_sort_container", "hilo")

    # ดึงราคาของสินค้าทั้งหมด (ใน order ที่ปรากฏใน DOM)
    price_elements = page.locator(".inventory_item_price")
    # 🔹 หา element ทั้งหมดที่มี class = "inventory_item_price"
    # 🔹 จะได้ Locator group ที่รวมราคาของสินค้าทั้งหมด
    prices = []
    # 🔹 เตรียม list ว่างไว้เก็บราคาสินค้าในรูปแบบ float
    count = price_elements.count()
    # 🔹 นับจำนวนราคาทั้งหมด (เช่น อาจมี 6 ชิ้น → count = 6)
    for i in range(count):
        # 🔹 วนลูปตามจำนวนสินค้า
        price_text = price_elements.nth(i).inner_text()  # เช่น "$29.99"
        # 🔹 ดึงข้อความของราคาชิ้นที่ i (เช่น "$9.99")
        price_value = float(price_text.replace("$", ""))
        # 🔹 ลบ `$` ออกจาก string แล้วแปลงเป็น float (เช่น "$29.99" → 29.99)
        prices.append(price_value)
        # 🔹 เพิ่มราคาที่แปลงแล้วลงใน list prices

    # ตรวจสอบว่าราคาเรียงจากมากไปน้อย
    assert prices == sorted(prices, reverse=True), f"ราคาสินค้าไม่เรียงมากไปน้อย: {prices}"
    # 🔹 ตรวจสอบว่า list prices มีค่าตรงกับ version ที่ sort แล้ว (desc)
    # 🔹 ถ้าไม่ตรง → แปลว่าราคาบางชิ้นเรียงผิด จะเกิด AssertionError และแสดงราคาทั้งหมด
    logger.info(f"[HIGH to LOW] ราคาที่ได้จากหน้าเว็บ: {prices}")

    # 🔻 เลือก Name (A to Z)
    page.select_option(".product_sort_container", "az")

     # ดึงชื่อสินค้าทั้งหมด (ใน order ที่ปรากฏใน DOM)
    name_elements = page.locator(".inventory_item_name")
    # 🔹 หา element ทั้งหมดที่มี class = "inventory_item_name"
    # 🔹 จะได้ Locator group ที่รวมชื่อของสินค้าทั้งหมด

    names = []
    # 🔹 เตรียม list ว่างไว้เก็บชื่อสินค้า
    count = name_elements.count()
    # 🔹 นับจำนวนชื่อสินค้าทั้งหมด (เช่น อาจมี 6 ชิ้น → count = 6)
    for i in range(count):
    # 🔹 วนลูปตามจำนวนสินค้า
        name = name_elements.nth(i).inner_text()
        # 🔹 ดึงข้อความของชื่อสินค้า
        names.append(name)
        # 🔹 เพิ่มชื่อสินค้าลงใน list

    assert names == sorted(names), f"❌ ชื่อสินค้าไม่เรียงจาก A → Z: {names}"
    logger.info(f"[A to Z] ชื่อที่ได้จากหน้าเว็บ: {names}")

    # 🔻 เลือก Name (A to Z)
    page.select_option(".product_sort_container", "za")

     # ดึงชื่อสินค้าทั้งหมด (ใน order ที่ปรากฏใน DOM)
    name_elements = page.locator(".inventory_item_name")
    # 🔹 หา element ทั้งหมดที่มี class = "inventory_item_name"
    # 🔹 จะได้ Locator group ที่รวมชื่อของสินค้าทั้งหมด

    names = []
    # 🔹 เตรียม list ว่างไว้เก็บชื่อสินค้า
    count = name_elements.count()
    # 🔹 นับจำนวนชื่อสินค้าทั้งหมด (เช่น อาจมี 6 ชิ้น → count = 6)
    for i in range(count):
    # 🔹 วนลูปตามจำนวนสินค้า
        name = name_elements.nth(i).inner_text()
        # 🔹 ดึงข้อความของชื่อสินค้า
        names.append(name)
        # 🔹 เพิ่มชื่อสินค้าลงใน list

    assert names == sorted(names, reverse=True), f"❌ ชื่อสินค้าไม่เรียงจาก Z → A: {names}"
    logger.info(f"[Z to A] ชื่อที่ได้จากหน้าเว็บ: {names}")
