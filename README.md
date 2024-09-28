## Test Playwright 

This repository contains a basic reference structure of how to organize a Playwright test suite. 

## Testing Sites 
- https://www.saucedemo.com/
- https://playwright.dev/python/

## How to Setup  
- Clone the repo into your box 
`$ git clone <repo_url>`   
- Create your virtual environment      
`$ python[X.yz] -v -m venv <venv_name>`   
- Activate the environment  
`$ . <venv_name>/bin/activate`  
- Install requirements  
`$ pip[X.yz]  install -r requirements.txt`  
- Install required browsers with `playwright`  
`$ playwright install`  


## How to run test file/s
Run all `test_` files in headless mode  
`$ pytest`

Run all `test_` files in headed mode  
`$ pytest --run-headed`  

Run a `test_` file in headed mode  
`$ pytest tests/test_login_logout.py --run-headed`

Run a `test_` file in headless mode  
`$ pytest tests/test_login_logout.py `  
Run a `test_` file in slow motion `miliseconds`  
`$ pytest tests/test_login_logout.py --slow-mo 1200 --run-headed`  
Run all test files one after another  
`pytest [--run-headed]  [--slow-mo]`  


## ⚠ Notes️
`- scripts/ directory contains rough codes. You can put your ones here or ignore this directory.`  
`- This suite is tested on Windows 10 , Deabian and Ubuntu`  
`- Docstrings are created using Gemini`  
`- This repo is verbosely and repeatedly commented for tutorial purposes 🐣. In real life use cases, do comments and docstrings when necessesary.`  
## To Dos  
~~- Details documentation~~ 
- Adding more complex test scenarios  
- Executing more complex test cases

