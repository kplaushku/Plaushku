*** Settings ***
Library    ../src/plaushku/visual.py
*** Test Cases ***
Check Google Homepage Visually
    [Documentation]    Open google.com, take a full-page screenshot,
    ...               compare with baseline, store diff if mismatch.
    Compare Web Page With Baseline    test_google_home    https://www.google.com    threshold=2