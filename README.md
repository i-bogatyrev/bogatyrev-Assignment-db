
# Python Selenium shares prices test

This project demonstrates the use of Python, Selenium WebDriver, and Pytest to automate a single web test scenario, which compares DB1 (Deutsche Börse AG) share prices across two different resources. The test suite addresses various aspects of the application, including navigation, interaction, data validation, and error handling.


## Requirements
- Python 3.11
- pip3
## Installation

In terminal go to project root folder and run this command

```bash
  pip3 install -r requirements.txt         
```
    
## Running Tests

To run the test, run the following command in the project root folder

```bash
  pytest -s  test_compare_db1_share_prices.py 
```


## Example of test output, positive result

```bash
+-------------+
|             |
| TEST RESULT |
|             |
+-------------+

Current Date = May 01, 2023
Current Time = 22:35:08 CEST

DB1 Share price on Deutsche Boerse web page:
Price: 172.9€, Time: 17:35 CEST

DB1 Share price on Yahoo web page:
Price: 172.9€, Time: 17:35 CEST

Price Difference: 0.00
Time Difference: 0 (Both resources have the same data time)
```
## Author

[@Iaroslav.Bogatyrev](mailto:iaroslav.bogatyrev@adastra.one)

