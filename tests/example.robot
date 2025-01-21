*** Settings ***
Library    plaushku

*** Test Cases ***
Verify Full Page Comparison
    Compare Web Page With Baseline    test_google_home    https://www.google.com    threshold=2