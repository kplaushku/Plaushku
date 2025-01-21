
# Plaushku

Plaushku is a Robot Framework library designed to make visual regression testing simple and painless. It automatically:
1. Opens a headless Chrome browser,
2. Navigates to a specified URL,
3. Captures a full-page screenshot (by scrolling and stitching),
4. Compares the captured screenshot with a baseline image,
5. Generates a diff image if differences are found,
6. Closes the browser.

All of these steps can be performed with a single Robot Framework keyword:

`Compare Web Page With Baseline`

## Table of Contents
1. Key Features
2. Installation
3. Folder Structure
4. Usage in Robot Tests
5. Example Test
6. Advanced Usage
7. Troubleshooting
8. Contributing
9. License

## Key Features
- **Full-Page Screenshots:** Plaushku captures the entire webpage by scrolling and stitching.
- **Single Keyword Simplicity:** Just call `Compare Web Page With Baseline` from your Robot tests.
- **Diff Image Generation:** If the actual screenshot differs from the baseline, a diff image is automatically created.
- **Headless Browser:** Uses Selenium with a headless Chrome driver for automated captures.
- **Threshold Support:** Specify a difference threshold to allow minor variations (e.g., 2%).
- **Easy Folder Conventions:** Organizes screenshots in `visual_testing/<test_name>/{baseline,actual_result,diff}`.

## Installation
1. Ensure you have Python 3.7+ and pip installed.
2. Install Chrome or Chromium, along with a matching ChromeDriver.
    - ChromeDriver Download or install from your package manager.
3. Install Plaushku from source (or PyPI, if available):
    ```bash
    # From the directory containing pyproject.toml (or setup.py)
    pip install .
    ```
    or
    ```bash
    # If Plaushku is published on PyPI (example placeholder)
    pip install plaushku
    ```
4. Verify installation by listing installed packages:
    ```bash
    pip list | grep plaushku
    ```

## Folder Structure

Plaushku organizes images in a predictable directory layout under `visual_testing/`. You provide a test name, and Plaushku uses that to create:

```
visual_testing/
└── <test_case_name>/
    ├── baseline/
    │   └── fullpage.png      # The known-good baseline screenshot
    ├── actual_result/
    └── diff/
```

- **baseline/**: Where you store your reference (expected) image named `fullpage.png`.
- **actual_result/**: Plaushku will save the newly captured screenshot here (`fullpage.png`).
- **diff/**: If a difference is detected, Plaushku saves a diff image (`fullpage_diff.png`) here.

You can customize or rename these directories in the source code if necessary, but the default structure is simple and intuitive.

## Usage in Robot Tests

To use Plaushku in your `.robot` files, do the following:
1. Import the Plaushku library:
    ```robotframework
    *** Settings ***
    Library    plaushku.visual.PlaushkuKeywords
    ```
2. Place a baseline screenshot in the correct folder:
    ```
    visual_testing/
    └── my_test_case/
        └── baseline/
            └── fullpage.png
    ```
3. Call the `Compare Web Page With Baseline` keyword with the test name and URL:
    ```robotframework
    *** Test Cases ***
    Check Google Homepage Visually
        [Documentation]    Compare new screenshot with an existing baseline.
        Compare Web Page With Baseline    my_test_case    https://www.google.com    threshold=2
    ```

4. **Threshold (optional):** The `threshold` argument (defaults to 0) allows small differences (e.g., font smoothing changes, minor layout shifts). You can omit it if you want an exact match.

## Example Test

Below is a simple `.robot` test suite named `example.robot`.
```robotframework
*** Settings ***
Library    plaushku.visual.PlaushkuKeywords

*** Test Cases ***
Check Google Homepage Visually
    [Documentation]   Capture a full-page screenshot of Google's homepage, compare
    ...              with baseline, and store a diff if there's a mismatch.
    Compare Web Page With Baseline    test_google_home    https://www.google.com    threshold=2
```

**Corresponding Folder Structure**
1. Create the baseline folder & place your reference image:
    ```
    visual_testing/
    └── test_google_home/
        └── baseline/
            └── fullpage.png     # Known-good screenshot of Google
    ```
2. Run the test:
    ```bash
    robot example.robot
    ```
3. Results:
    - A new screenshot saved in `visual_testing/test_google_home/actual_result/fullpage.png`.
    - If there’s a mismatch above `threshold%`, a diff image is written to `visual_testing/test_google_home/diff/fullpage_diff.png`.
    - Your Robot logs (`output.xml`, `log.html`, `report.html`) show the test results and any failure details.

## Advanced Usage
1. **Scrolling Chunk Size:**  
   By default, Plaushku scrolls in 800px increments. Adjust this in `_capture_full_page_screenshot` if your pages are shorter or longer.
2. **Non-Headless Testing:**  
   If you wish to see the browser (i.e., not headless), you can modify the `_open_chrome_browser` method in the library and remove or comment out the `--headless=new` argument.
3. **Parallel Testing:**  
   Plaushku can be used in parallel test execution, but ensure each test uses a unique `test_name` so they don’t overwrite each other’s screenshot directories.
4. **CI Integration:**  
   Plaushku can run in CI/CD pipelines if Chrome/ChromeDriver are available. Make sure to install them in your CI environment.
5. **Dynamic Baselines:**  
   You can version-control your baseline images or automate baseline updates if you decide new screenshots are “correct.” This is an optional strategy depending on your workflow.

## Troubleshooting
1. **ChromeDriver Issues:**
    - If you see errors like `selenium.common.exceptions.WebDriverException: Message: chromedriver executable needs to be in PATH`, ensure ChromeDriver is properly installed and on your system `PATH`.
    - Make sure your ChromeDriver version matches your local Chrome/Chromium browser version.
2. **Images Differ Slightly:**
    - Try using a small `threshold` (e.g., 1 or 2) if minor rendering differences cause false negatives.
    - Check fonts, browser versions, and OS rendering differences.
3. **Large Pages:**
    - If your page is extremely long, consider increasing the chunk size or adjusting the code to handle memory usage.
    - For very large pages, you might need more memory or additional optimization in stitching logic.
4. **Timed-Out / Partial Screens:**
    - Increase the `time.sleep()` inside `_capture_full_page_screenshot` if your pages are slow to load or dynamic content is not fully rendered at capture time.

## Contributing

Plaushku is intended as a starting point or reference. If you have improvements or additional features (e.g., region-based screenshots, ignoring dynamic elements, more advanced diffing algorithms), feel free to:
1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request.

We welcome contributions that make visual testing simpler, more robust, and more flexible.

## License

**MIT License**

Copyright (c) 20xx ...

Permission is hereby granted, free of charge, ...

---

Plaushku aims to simplify visual regression testing with Robot Framework by bundling Selenium and Pillow. It’s easy to extend or tailor to your organization’s needs—change the scrolling logic, add region-based comparisons, or integrate advanced diffing methods. If you have any questions, suggestions, or bug reports, please open an issue or reach out to the maintainers.

**Happy Testing!**

**Plaushku – Where Visual Testing Meets Simplicity!**
