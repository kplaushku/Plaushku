*** Settings ***
Library    ../src/plaushku/visual.py

*** Test Cases ***
Check Google Homepage Visually
    [Documentation]    Verify Google homepage against the baseline.
    Compare Web Page With Baseline    test_google_home    https://www.google.com    threshold=2