"""Capture screenshots for LaTeX documentation.
Captures: gallery (2x2), anhinga viewer with bird popup, minerals viewer with whole-image lens.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.set_window_size(1400, 900)

try:
    driver.get("http://localhost:8080/index.html")
    time.sleep(3)

    # 1. Gallery screen (2x2 grid)
    driver.save_screenshot("docs/gallery.png")
    print("1. Gallery (2x2) captured")

    # 2. Click Anhinga (3rd item, index 2)
    items = driver.find_elements(By.CSS_SELECTOR, ".gallery-item")
    items[2].click()
    time.sleep(2)
    driver.save_screenshot("docs/viewer-anhinga.png")
    print("2. Anhinga viewer captured")

    # 3. Click on the bird region (center of image)
    artwork = driver.find_element(By.ID, "artwork")
    rect = artwork.rect
    # Bird is roughly center of the image
    ActionChains(driver).move_to_element_with_offset(
        artwork, int(rect['width'] * 0.05), int(rect['height'] * -0.05)
    ).click().perform()
    time.sleep(1)
    driver.save_screenshot("docs/anhinga-bird-popup.png")
    print("3. Anhinga bird popup captured")

    # 4. Go back to gallery
    driver.find_element(By.ID, "back-btn").click()
    time.sleep(1)

    # 5. Click Minerals (4th item, index 3)
    items = driver.find_elements(By.CSS_SELECTOR, ".gallery-item")
    items[3].click()
    time.sleep(2)
    driver.save_screenshot("docs/viewer-minerals.png")
    print("4. Minerals viewer captured")

    # 6. Click whole-image lens button
    lens_btn = driver.find_element(By.ID, "image-lens-btn")
    if lens_btn.is_displayed():
        lens_btn.click()
        time.sleep(1)
        driver.save_screenshot("docs/minerals-wholeimage.png")
        print("5. Minerals whole-image lens captured")

    print("\nAll screenshots captured in docs/")

finally:
    driver.quit()
