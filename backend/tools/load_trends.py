import json

def load_mock_trends():
    with open("backend/data/mock_trends.json", "r") as file:
        return json.load(file)

if __name__ == "__main__":
    print(load_mock_trends())