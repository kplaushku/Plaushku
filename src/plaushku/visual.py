import os
import math
import time
from PIL import Image, ImageChops
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class PlaushkuKeywords:
    """
    A simplified Robot Framework library for visual regression testing
    of *entire* web pages (including content outside the initial viewport).

    Core Feature:
      - One keyword: `Compare Web Page With Baseline`, which:
        1) Opens a headless Chrome browser
        2) Navigates to the URL
        3) Scrolls & stitches a full-page screenshot
        4) Compares it against a baseline image
        5) Generates a diff if there's a mismatch
        6) Closes the browser
    """

    def compare_web_page_with_baseline(self, test_name, url, threshold=0):
        """
        This single keyword handles everything for a full-page visual test.

        Usage in Robot:
            Compare Web Page With Baseline    test_google_home    https://www.google.com    threshold=2

        Steps it performs:
          - Opens a headless Chrome browser
          - Navigates to `url`
          - Scrolls through the entire page, capturing multiple screenshots
            which are stitched into one large image
          - Compares the new screenshot against a baseline image located at:
                visual_testing/<test_name>/baseline/fullpage.png
          - If there's a difference above `threshold`%,
            a diff image is saved to:
                visual_testing/<test_name>/diff/fullpage_diff.png
          - Closes the browser
        """
        driver = None
        try:
            # 1) Open headless Chrome
            driver = self._open_chrome_browser()

            # 2) Go to URL
            driver.get(url)
            time.sleep(2)  # Allow some load time (adjust if needed)

            # 3) Define file paths
            base_dir = os.path.join("visual_testing", test_name)
            baseline_img = os.path.join(base_dir, "baseline", "fullpage.png")
            actual_img   = os.path.join(base_dir, "actual_result", "fullpage.png")
            diff_img     = os.path.join(base_dir, "diff", "fullpage_diff.png")

            # Ensure folders exist
            os.makedirs(os.path.dirname(actual_img), exist_ok=True)
            os.makedirs(os.path.dirname(diff_img), exist_ok=True)

            # 4) Capture full-page screenshot by scrolling & stitching
            self._capture_full_page_screenshot(driver, actual_img)

            # 5) Compare with baseline
            if not os.path.exists(baseline_img):
                raise FileNotFoundError(
                    f"Baseline image not found: {baseline_img}\n"
                    f"Please place a baseline at this path, or update your workflow."
                )

            self._compare_images(baseline_img, actual_img, diff_img, threshold)

        finally:
            # 6) Close the browser
            if driver:
                driver.quit()

    # -------------------------------------------------------------------------
    # Internal Helper Methods (not exposed as Robot keywords)
    # -------------------------------------------------------------------------

    def _open_chrome_browser(self, headless=True):
        """Open and return a headless Chrome driver."""
        options = Options()
        if headless:
            options.add_argument("--headless=new")  # For Chrome 109+
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver

    def _capture_full_page_screenshot(self, driver, output_path):
        """
        Scrolls through the page in chunks and stitches partial screenshots into one final image.
        """
        scroll_width  = driver.execute_script("return document.body.scrollWidth")
        scroll_height = driver.execute_script("return document.body.scrollHeight")

        # We'll pick a chunk height to scroll step by step
        chunk_height = 800
        driver.set_window_size(scroll_width, chunk_height)

        stitched_image = Image.new('RGB', (scroll_width, scroll_height))
        total_screens = max(1, math.ceil(scroll_height / chunk_height))

        for i in range(total_screens):
            scroll_top = i * chunk_height
            driver.execute_script(f"window.scrollTo(0, {scroll_top});")
            time.sleep(0.5)  # Short pause to let rendering catch up

            # Get a screenshot of the current viewport
            screenshot_png = driver.get_screenshot_as_png()
            temp_img = Image.open(bytes(screenshot_png))

            # Paste it in the correct position
            stitched_image.paste(temp_img, (0, scroll_top))

        stitched_image.save(output_path)
        print(f"[INFO] Full-page screenshot saved to: {output_path}")

    def _compare_images(self, baseline_path, actual_path, diff_path, threshold=0):
        """
        Compare two images. If difference > threshold%, raise an AssertionError.
        Saves a diff image highlighting differences (in basic gray).
        """
        from PIL import ImageChops

        base_img   = Image.open(baseline_path).convert("RGB")
        actual_img = Image.open(actual_path).convert("RGB")

        if base_img.size != actual_img.size:
            raise ValueError("Cannot compare images of different sizes.")

        diff_img = ImageChops.difference(base_img, actual_img)
        diff_bbox = diff_img.getbbox()

        # If diff_bbox is None, images are identical
        if not diff_bbox:
            print("[INFO] Images match exactly (0% difference).")
            return

        # Calculate difference in a simple way: count non-zero (changed) pixels
        diff_hist = diff_img.histogram()
        sum_of_differences = sum(diff_hist[1:])  # skipping the zero bin
        total_pixels = base_img.width * base_img.height * 3
        difference_percent = (sum_of_differences / float(total_pixels)) * 100

        if difference_percent > threshold:
            diff_img.save(diff_path)
            msg = (
                f"Images differ by {difference_percent:.2f}% "
                f"(threshold: {threshold}%). Diff saved to {diff_path}"
            )
            raise AssertionError(msg)
        else:
            print(f"[INFO] Images differ by {difference_percent:.2f}%, within threshold.")