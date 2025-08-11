"""
Uses the parsed user data to populate the HTML template.

I used ChatGPT to help generate large parts of this file, as well as the HTML template itself.
"""

import random

from html import escape
from string import Template
from pathlib import Path


TEMPLATE_FILE = "timetable_template.html"
TITLE = "DEMCON Non Stop Festival Timetable"
LOGO_HTML = '<img src="logo-demcon.png" alt"DEMCON logo">'
OUPUT_DEST = "timetable.html"


def build(schedule, schedule_list, festival_start, festival_end):
    all_hours = range(festival_start, festival_end)
    all_stages = sorted(schedule.keys())
    hour_to_col = {h: idx + 2 for idx, h in enumerate(all_hours)}  # +2 because col1 is stage labels
    stage_to_row = {s: idx + 2 for idx, s in enumerate(all_stages)}     # +2 because row1 is time headers

    # Generate colors dynamically based on the number of stages
    palette = [f"hsl({int((stage_index - 1) * 360 / len(all_stages)) % 360} 70% 85%)" 
               for stage_index, _ in enumerate(all_stages)]
    random.shuffle(palette)  # Randomize order of colors

    # Time labels (row 1)
    time_labels = "".join(
        f'<div class="time-header" style="grid-row:1; grid-column:{hour_to_col[h]};">{h}:00</div>'
        for h in all_hours
    )

    # Stage labels (col 1)
    stage_labels = "".join(
        f'<div class="stage-label" style="grid-row:{stage_to_row[s]}; grid-column:1;">Stage {s}</div>'
        for s in all_stages
    )

    # Generate divs for each act.
    block_divs = []
    for stage, act_name, start, end in schedule_list:
        col_start = hour_to_col[start]
        span = end - start + 1
        row = stage_to_row[stage]
        color = palette[(stage - 1)]
        label = f'{escape(act_name)} ({start}:00–{end}:59)'
        block_divs.append(
            f'''<div class="block"
                style="grid-row:{row}; grid-column:{col_start} / span {span}; background:{color};"
                title="{label}">
                <div class="block-title">{escape(act_name)}</div>
                <div class="block-time">{start}:00–{end}:59</div>
            </div>'''
        )
    blocks_html = "".join(block_divs)

    # Read template and substitute placeholders
    tpl_text = Path(TEMPLATE_FILE).read_text(encoding="utf-8")
    tpl = Template(tpl_text)
    html = tpl.substitute(
        TITLE=escape(TITLE),
        HOUR_COUNT=len(all_hours),
        TIME_HEADERS=time_labels,
        STAGE_LABELS=stage_labels,
        BLOCKS=blocks_html,
        LOGO=LOGO_HTML
    )

    Path(OUPUT_DEST).write_text(html, encoding="utf-8")
    print(f'Timetable saved to {OUPUT_DEST}')