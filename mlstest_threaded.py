# This is a sample just to show how threading can scale Nova Act processes in parallel.

from concurrent.futures import ThreadPoolExecutor, as_completed
from nova_act import ActError, NovaAct
from pathlib import Path
import re
import json

INPUT_JSON_FILE = "SingleFamilyHome.json"
STARTING_PAGE = "http://www.amazon.com/"
NUMBER_OF_WORKERS = 20

def read_json_from_file():
    #Read json object from local json file
    json_file_path = Path(__file__).parent / INPUT_JSON_FILE
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
        print(json.dumps(json_data))
        return json_data
    #return json_data

def enter_json_data_using_nova_act(count):
    #Enter json object using nova act
    json_data = read_json_from_file()
    with NovaAct(starting_page=STARTING_PAGE,record_video=True, headless=True) as browser:
        try:
            for field_name, field_value in json_data.items():
                    #browser.act(f"""Activate '{field_name}' by clicking below the '{field_name}'""")
                    browser.act(f"""Type {field_value} into '{field_name}' field. DO NOT press enter. The names might not be exactly the same, use your judgement.""")
                    browser.act(f"""Ensure you've filled {field_value} into '{field_name}.""")
            res = browser.act("hit submit")
        except Exception as e:
            print(f"Error: {e}")
            return False
        return res

def main():
    # Set max workers to the max number of active browser sessions.
    with ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:
        mythreads= { executor.submit(enter_json_data_using_nova_act, count): count for count in range(1, NUMBER_OF_WORKERS) }

if __name__ == "__main__":
    main()

