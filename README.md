# JSON Parser
This project is a simple JSON parser built from scratch using Test-Driven Development (TDD). The parser is designed to read, validate, and extract data from JSON strings, ensuring correctness through a suite of unit tests.
## Project Setup:
Clone the repository:
```bash
git clone https://github.com/AbderrahimRezki/JSONParser.git
cd JSONParser
```
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
Install json_parser as a library (to be able to import it anywhere in the directory
```bash
pip install .
```
Run tests: 
```bash
python -m unittest discover test/
```
## Usage
```py
from json_parser import parse_json

json_string = '''{
  "key-s": "string value",
  "key-n": 37.7,
  "key-a": [1, 2, 3, "string", true, null],
  "key-o": {
    "key-o-bool": false
  }
}'''

print(parse_json(json_string))

# Output
{'key-s': 'string value', 'key-n': 37.7, 'key-a': [1.0, 2.0, 3.0, 'string', True, None], 'key-o': {'key-o-bool': False}}
```
