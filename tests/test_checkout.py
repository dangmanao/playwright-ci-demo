import time
#  เพิ่มสำหรับใช้ delay
import re

from playwright.sync_api import Page, expect
# 🔹 นำเข้า Page สำหรับควบคุม browser tab
# 🔹 นำเข้า expect สำหรับ assertion เช่น ตรวจสอบว่า element แสดงผลจริง

def test_example(page: Page, logger) -> None:
    # 🔹 กำหนดให้เป็น test function สำหรับ pytest
    # 🔹 รับ object `page` ซึ่งเป็น browser page (tab) ที่ใช้ดำเนินการใน test นี้

    page.goto("https://www.saucedemo.com/v1/index.html")
    # 🔹 เปิดหน้าเว็บ saucedemo (URL ของหน้า login)

    page.locator("[data-test=\"username\"]").click()
    # 🔹 คลิกที่ช่อง username (focus ให้พร้อมกรอก)

    page.locator("[data-test=\"username\"]").fill("standard_user")
    # 🔹 กรอก username ว่า "standard_user"

    page.locator("[data-test=\"password\"]").click()
    # 🔹 คลิกช่อง password

    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    # 🔹 กรอก password ใหม่ว่า "secret_sauce" (ซึ่งเป็นค่าที่ถูกต้อง)

    page.get_by_role("button", name="LOGIN").click()
    # 🔹 คลิกปุ่ม Login โดยระบุว่าเป็นปุ่มที่มีชื่อว่า "LOGIN" (ตาม ARIA role)

    page.locator(".inventory_item", has_text="Sauce Labs Backpack").get_by_role("button", name="ADD TO CART").click()
    # 🔹 หาสินค้าที่มีข้อความว่า "Sauce Labs Backpack"
    # 🔹 คลิกปุ่ม "ADD TO CART" ของสินค้านั้น

    expect(page.locator(".inventory_item", has_text="Sauce Labs Backpack").get_by_role("button", name="ADD TO CART")).not_to_be_visible()
    # 🔹 หลังจากกดปุ่ม ADD TO CART ของ item Sauce Labs Backpack ไปแล้วปุ่ม ADD TO CART จะต้องหายไป

    expect(page.locator(".inventory_item", has_text="Sauce Labs Backpack").get_by_role("button", name="REMOVE")).to_be_visible()
    # 🔹 หลังจากกดปุ่ม ADD TO CART ของ item Sauce Labs Backpack ไปแล้วปุ่ม REMOVE จะต้องแสดงขึ้นมาแทน

    page.locator(".inventory_item", has_text="Sauce Labs Bike Light").get_by_role("button", name="ADD TO CART").click()
      # 🔹 หาสินค้าที่มีข้อความว่า "Sauce Labs Bike Light"
      # 🔹 คลิกปุ่ม "ADD TO CART" ของสินค้านั้น

    page.locator(".inventory_item", has_text="Sauce Labs Onesie").get_by_role("button", name="ADD TO CART").click()
      # 🔹 หาสินค้าที่มีข้อความว่า "Sauce Labs Onesie"
      # 🔹 คลิกปุ่ม "ADD TO CART" ของสินค้านั้น

    badge = page.locator("span.shopping_cart_badge")
    expect(badge).to_have_text("3")
    # ตรวจสอบว่าเลข badge ที่แสดงบนรถเช็นเป็น 3 ตามตำนวน item ที่ add ลงไปไหม

    page.locator(".shopping_cart_link").click()
    # 🔹 คลิกลิงก์ที่ชื่อว่า "3" (คือ cart icon ที่แสดงว่ามีสินค้า 3 ชิ้น)

    page.locator(".cart_item", has_text="Sauce Labs Bike Light").get_by_role("button", name="REMOVE").click()
    # 🔹 หาสินค้าใน cart item ทั้งหมด ตัวไหนที่มีข้อความว่า "Sauce Labs Backpack"
    # 🔹 คลิกปุ่ม "REMOVE" ของสินค้านั้น

    expect(badge).to_have_text("2")
    # ตรวจสอบว่าเลข badge ที่แสดงบนรถเช็นเป็น 2 ตามตำนวน item ที่ remove ออกมาไหม

    page.locator(".cart_item", has_text="Sauce Labs Backpack").get_by_role("button", name="REMOVE").click()
    # 🔹 หาสินค้าใน cart item ทั้งหมด ตัวไหนที่มีข้อความว่า "Sauce Labs Backpack"
    # 🔹 คลิกปุ่ม "REMOVE" ของสินค้านั้น

    expect(badge).to_have_text("1")
    # ตรวจสอบว่าเลข badge ที่แสดงบนรถเช็นเป็น 2 ตามตำนวน item ที่ remove ออกมาไหม

    page.locator(".cart_item", has_text="Sauce Labs Onesie").get_by_role("button", name="REMOVE").click()
    # 🔹 หาสินค้าใน cart item ทั้งหมด ตัวไหนที่มีข้อความว่า "Sauce Labs Backpack"
    # 🔹 คลิกปุ่ม "REMOVE" ของสินค้านั้น

    expect(badge).not_to_be_attached()
    # เช็คว่า element นี้ต้องหายไปหลังจากที่ไม่มี item ใน cart
    page.screenshot(path="reports/noitemincart.png")
    # ถ่ายรูปเพื่อความชัวร์ว่า ไม่มี item ใน cart

    page.get_by_role("link", name="Continue Shopping").click()
    # 🔹 คลิกลิงก์ที่ชื่อว่า "Continue Shopping" เพื่อเข้าสู่หน้ากรอกข้อมูลจัดส่ง

    expect(page).to_have_url("https://www.saucedemo.com/v1/inventory.html")
    # 🔹 ตรวจสอบว่าหลังกดปุ่ม Continue Shopping ระบบไปหน้า Product list ถูกต้อง

    page.locator(".inventory_item", has_text="Sauce Labs Bike Light").get_by_text("Sauce Labs Bike Light").click()
      # 🔹 หาสินค้าที่มีข้อความว่า "Sauce Labs Bike Light" จากนั้นกดไปที่ชื่อสินค้านั้นเพื่อไปที่หน้า Product detail

    expect(page).to_have_url(re.compile(r".*/inventory-item.html*"))
    # 🔹 ตรวจสอบว่าไปหน้า product detail ถูกต้อง URL ต้องประกอบไปด้วยคำที่อยู่ข้างใน *

    page.locator(".inventory_details", has_text="Sauce Labs Bike Light").get_by_role("button", name="ADD TO CART").click()
      # 🔹 หาสินค้าที่มีข้อความว่า "Sauce Labs Onesie"
      # 🔹 คลิกปุ่ม "ADD TO CART" ของสินค้านั้น

    expect(page.locator(".inventory_details_container").get_by_role("button", name="REMOVE")).to_be_visible()
    # 🔹 หลังจากกดปุ่ม ADD TO CART ของ item Sauce Labs Backpack ไปแล้วปุ่ม REMOVE จะต้องแสดงขึ้นมาแทน

    page.locator(".inventory_details").get_by_role("button", name="REMOVE").click()
      # 🔹 กดปุ่ม REMOVE สินค้านั้นเพื่อทำการ Remove product นั้นออกจาก Cart

    page.locator(".inventory_details", has_text="Sauce Labs Bike Light").get_by_role("button", name="ADD TO CART").click()
      # 🔹 หาสินค้าที่มีข้อความว่า "Sauce Labs Onesie"
      # 🔹 คลิกปุ่ม "ADD TO CART" ของสินค้านั้น

    page.locator(".inventory_details").get_by_role("button", name="Back").click()
      # กดปุ่ม Back เพื่อออกจากหน้า product Detail page

    page.locator(".inventory_item", has_text="Sauce Labs Onesie").get_by_role("button", name="ADD TO CART").click()
      # 🔹 หาสินค้าที่มีข้อความว่า "Sauce Labs Onesie"
      # 🔹 คลิกปุ่ม "ADD TO CART" ของสินค้านั้น
    
    page.locator(".shopping_cart_link").click()
    # 🔹 กดที่ icon รถเข็น

    page.get_by_role("link", name="CHECKOUT").click()
    # 🔹 คลิกลิงก์ที่ชื่อว่า "CHECKOUT" เพื่อเข้าสู่หน้ากรอกข้อมูลจัดส่ง

    page.get_by_role("link", name="CANCEL").click()
    # 🔹 คลิกลิงก์ที่ชื่อว่า "CANCEL" เพื่อกลับไปหน้า product list

    page.get_by_role("link", name="CHECKOUT").click()
    # 🔹 คลิกลิงก์ที่ชื่อว่า "CHECKOUT" เพื่อเข้าสู่หน้ากรอกข้อมูลจัดส่ง

    expect(page).to_have_url("https://www.saucedemo.com/v1/checkout-step-one.html")
    # 🔹 ตรวจสอบว่าหลังกดปุ่ม Checkout ระบบไปหน้า Checkout ถูกต้อง

    page.get_by_role("button", name="CONTINUE").click()
    # กดปุ่ม Continue โดยที่ยังไม่ได้กรอก information ใดๆเลย
    expect(page.locator(".checkout_info_wrapper", has_text="First Name is required")).to_be_visible()
    # เช็คว่าขึ้น Error message "First Name is required" ถูกต้องไหม

    page.get_by_role("textbox", name="First Name").click()
    page.get_by_role("textbox", name="First Name").fill("Dang")
    # 🔹 คลิกและกรอกชื่อจริงว่า "Dang"

    page.get_by_role("button", name="CONTINUE").click()
    expect(page.locator(".checkout_info_wrapper", has_text="Last Name is required")).to_be_visible()
    # เช็คว่าขึ้น Error message "Last Name is required" ถูกต้องไหม

    page.locator("[data-test=\"lastName\"]").click()
    page.locator("[data-test=\"lastName\"]").fill("DangLastName")
    # 🔹 คลิกและกรอกนามสกุลว่า "DangLastName"

    page.get_by_role("button", name="CONTINUE").click()
    expect(page.locator(".checkout_info_wrapper", has_text="Postal Code is required")).to_be_visible()
    # เช็คว่าขึ้น Error message "Last Name is required" ถูกต้องไหม

    page.locator("[data-test=\"postalCode\"]").click()
    page.locator("[data-test=\"postalCode\"]").fill("99999")
    # 🔹 คลิกและกรอกรหัสไปรษณีย์ว่า "99999"

    page.get_by_role("button", name="CONTINUE").click()
    # 🔹 คลิกปุ่ม CONTINUE เพื่อไปหน้าสรุปออเดอร์

    expect(page.locator(".inventory_item_name", has_text="Sauce Labs Bike Light")).to_be_visible()
    expect(page.locator(".inventory_item_name", has_text="Sauce Labs Onesie")).to_be_visible()
    expect(page.locator(".summary_info").get_by_text("SauceCard #31337")).to_be_visible()
    # เช็คว่ามีคำเหล่านี้แสดงอยู่ในหน้า checkout overview ไหม

    # เช็คว่าราคาของสินค้าที่กดมารวมแล้ว คำนวณแสดงขึ้นมาถูกไหม
    # ✅ 1. หา element ราคาสินค้าทั้งหมดใน cart
    item_price_elements = page.locator(".inventory_item_price")
    count = item_price_elements.count()
    
    prices = []
    for i in range(count):
        price_text = item_price_elements.nth(i).inner_text()  # เช่น "$9.99"
        price = float(price_text.replace("$", ""))
        prices.append(price)
    
    logger.info(f"ราคาสินค้าแต่ละชิ้น: {prices}")

    # ✅ 2. รวมราคาทั้งหมด
    total_from_items = sum(prices)
    logger.info(f"ผลรวมราคาสินค้า: {total_from_items:.2f}")

    # ✅ 3. ดึงค่าราคารวมที่แสดงในเว็บ
    total_text = page.locator(".summary_subtotal_label").inner_text()
    logger.info(f"text ของ total: {total_text}")
    
    # ตัดข้อความ “Item total: ” แล้วแปลงเป็น float
    total_displayed = float(total_text.replace("Item total: $", "").strip())
    logger.info(f"ราคาที่แสดงใน UI: {total_displayed:.2f}")

    # ✅ 4. ตรวจสอบว่าเท่ากัน
    assert round(total_from_items, 2) == round(total_displayed, 2), f"❌ รวมราคาไม่ตรงกัน: คำนวณได้ {total_from_items} แต่ UI แสดง {total_displayed}"

    page.get_by_role("link", name="FINISH").click()
    # 🔹 คลิก FINISH เพื่อยืนยันการสั่งซื้อ

    expect(page.get_by_role("heading", name="THANK YOU FOR YOUR ORDER")).to_be_visible()
    # 🔹 ตรวจสอบว่ามีข้อความ "THANK YOU FOR YOUR ORDER" แสดงอยู่บนหน้าจอ
    # 🔹 เป็นการยืนยันว่า order สำเร็จแล้ว

    page.get_by_role("button", name="Open Menu").click()
      # กด Hamburger menu

    page.get_by_role("link", name="Logout").click()
      # กด Hamburger menu

    expect(page).to_have_url("https://www.saucedemo.com/v1/index.html")
    # 🔹 ตรวจสอบว่าหลังกดปุ่ม Logout ระบบกลับมาที่หน้า Login ได้ถูกต้อง

    




