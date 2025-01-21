import os
import math
import time
from PIL import Image, ImageChops
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class PlaushkuKeywords:
    """
    A simplified Robot Framework library for visual regression testing
    of entire web pages (including content outside the initial viewport).
    """

    def compare_web_page_with_baseline(self, test_name, url, threshold=0):
        driver = None
        try:
            driver = self._open_chrome_browser()

            driver.get(url)
            time.sleep(2)

            base_dir = os.path.join("visual_testing", test_name)
            baseline_img = os.path.join(base_dir, "baseline", "fullpage.png")
            actual_img = os.path.join(base_dir, "actual_result", "fullpage.png")
            diff_img = os.path.join(base_dir, "diff", "fullpage_diff.png")

            os.makedirs(os.path.dirname(actual_img), exist_ok=True)
            os.makedirs(os.path.dirname(diff_img), exist_ok=True)

            self._capture_full_page_screenshot(driver, actual_img)

            if not os.path.exists(baseline_img):
                raise FileNotFoundError(
                    f"Baseline image not found: {baseline_img}\n"
                    f"Please create a baseline image at this path."
                )

            self._compare_images(baseline_img, actual_img, diff_img, threshold)

        finally:
            if driver:
                driver.quit()

    def _open_chrome_browser(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1920, 1080)
        return driver

    def _capture_full_page_screenshot(self, driver, output_path):
        scroll_width = driver.execute_script("return document.body.scrollWidth")
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        chunk_height = 800
        driver.set_window_size(scroll_width, chunk_height)

        stitched_image = Image.new("RGB", (scroll_width, scroll_height))
        total_screens = math.ceil(scroll_height / chunk_height)

        for i in range(total_screens):
            scroll_top = i * chunk_height
            driver.execute_script(f"window.scrollTo(0, {scroll_top});")
            time.sleep(0.5)
            screenshot_png = driver.get_screenshot_as_png()
            temp_img = Image.open(bytes(screenshot_png))
            stitched_image.paste(temp_img, (0, scroll_top))

        stitched_image.save(output_path)

    def _compare_images(self, baseline_path, actual_path, diff_path, threshold=0):
        base_img = Image.open(baseline_path).convert("RGB")
        actual_img = Image.open(actual_path).convert("RGB")

        if base_img.size != actual_img.size:
            raise ValueError("Images must be the same size.")

        diff_img = ImageChops.difference(base_img, actual_img)
        diff_bbox = diff_img.getbbox()

        if not diff_bbox:
            return

        diff_hist = diff_img.histogram()
        total_pixels = base_img.width * base_img.height * 3
        diff_percent = sum(diff_hist[1:]) / float(total_pixels) * 100

        if diff_percent > threshold:
            diff_img.save(diff_path)
            raise AssertionError(
                f"Images differ by {diff_percent:.2f}% (threshold: {threshold}%). Diff saved at {diff_path}"
            )