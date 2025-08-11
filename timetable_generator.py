import sys

from collections import defaultdict

from build_html import build


data_file = 'example_input.txt'
if len(sys.argv) > 1:
    data_file = sys.argv[1]


with open(data_file, 'r') as f:
    input = f.read().strip()


schedule = defaultdict(dict)  # {stage: {hour: act_name}}, allows for easy overlap checking.
schedule_list = []  # list of (stage, act_name, start, end) tuples, allows for easy HTML insertion.
festival_start = None
festival_end = None
for i, line in enumerate(input.split('\n')):
    if not line.strip():
        continue
    entry = line.split(' ')
    # Load entry fields into variables and perform some basic sanitization.
    act_name = entry[0]
    # We expect 3 fields per entry. Raise error otherwise.
    if len(entry) != 3:
        raise ValueError(f'Data error in file {data_file}, line {i+1}: line contains {len(entry)} '
                         'whitespace-separated fields, but 3 are expected.')
    # Try to read start and end times as integers. Raise error if it fails.
    try:
        start = int(entry[1])
        end = int(entry[2])
    except ValueError:
        raise ValueError(f'Data error in file {data_file}, line {i+1}: start and end fields must be integer values.')
    if end < start:
        raise ValueError(f'Data error in file {data_file}, line {i}: end time must be greater than start time.')
    
    scheduled_hours = range(start, end+1)
    stage = 1
    # Check if stage is already booked for these hours, and move to the next stage if so.
    while any(hour in schedule[stage] for hour in scheduled_hours):
        stage += 1
    schedule[stage].update({h: act_name for h in scheduled_hours})
    schedule_list.append((stage, act_name, start, end))
    # Keep track of festival start and end hours, this helps in building the HTML.
    if festival_start is None or start < festival_start:
        festival_start = start
    if festival_end is None or end > festival_end:
        festival_end = end


build(schedule, schedule_list, festival_start, festival_end)
print(f'Number of stages needed: {len(schedule)}')

