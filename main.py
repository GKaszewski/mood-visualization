from typing import List
import pandas as pd
import calmap
import matplotlib.pyplot as plt

RAD = 5
GOOD = 4
MEH = 3
BAD = 2
AWFUL = 1

moods = ['rad', 'good', 'meh', 'bad', 'awful']

data_file_path = 'daylio_export_2021_09_03.csv'


def convert_str_mood_to_value(mood: str) -> int:
    if mood == 'rad':
        return RAD
    elif mood == 'good':
        return GOOD
    elif mood == 'meh':
        return MEH
    elif mood == 'bad':
        return BAD
    elif mood == 'awful':
        return AWFUL


def set_data_to_proper_format(data: List[dict[str, int]]) -> List[dict[str, int]]:
    contents = []
    for i in range(0, len(data), 2):
        contents.append({data[i]['date']: data[i + 1]['mood']})
    return contents


def filter_data(lines: List[str]) -> List[dict[str, int]]:
    tmp = []
    for line in lines:
        elements = line.split(',')
        for element in elements:
            content = {}
            if not element:
                continue
            if len(element) >= 3:
                if element in moods:
                    content['mood'] = convert_str_mood_to_value(element)
                elif len(element.split('-')) == 3:
                    content['date'] = element
            if content:
                tmp.append(content)

    contents = set_data_to_proper_format(tmp)
    return contents


def load_csv(path: str) -> List[dict[str, int]]:
    with open(path) as f:
        lines = f.readlines()
        contents = filter_data(lines)
        return contents


def convert_to_one_dict(data: List[dict[str, int]]) -> dict[str, int]:
    output = {}
    for entry in data:
        for k,v in entry.items():
            output[k] = v
    return output


def prepare_calendar(data: dict[str, int]) -> None:
    events = pd.Series(data, index=data)
    events.index = pd.to_datetime(events.index)
    calmap.calendarplot(events, dayticks=False, fillcolor='grey', vmin=1.0, vmax=5.0, cmap='RdYlGn')


def main() -> None:
    raw_data = load_csv(data_file_path)
    data = convert_to_one_dict(raw_data)
    prepare_calendar(data)
    plt.show()


if __name__ == '__main__':
    main()
