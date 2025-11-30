import pandas as pd
from io import StringIO


class Faker:

    @classmethod
    def read_json_file(cls, path):
        with open(path) as f_:
            data = f_.read()
            return pd.read_json(StringIO(data))

    def students(self):
        return Faker.read_json_file("sample_data/students.json")
