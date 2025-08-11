# DEMCON Festival Timetable Generator

This project contains a script to generate an HTML timetable for the DEMCON festival based on a .txt data file provided by the user. The script automatically determines the required number of stages, and assigns acts to stages such that there is no overlap between acts on a single stage.

## Data file
The data file should be a .txt containing whitespace separated fields in the following format: `act_name, start_hour, end_hour`. Each row corresponds to a single act. See 'example_input.txt' for an example. Note that the `act_name` field cannot contain a whitespace, and `start_hour` and `end_hour` should be integers.

#### Assigning priority
Acts are given priority based on their position in the data file. I.e. if multiple acts overlap, the first one encountered will be assigned to the first stage, the second one to the second stage, etc. E.g. if the Demcon Band, Taylor Swift and Coldplay overlap, you'll want to enter them in this order to make sure the Demcon Band gets the stage it deserves:
```
DemconBand 1 10
Coldplay 1 4
TaylorSwift 2 8
```

## How to run
To run the script on the example input, run:
```bash
python build_timetable.py example_input.txt
```

To run it on your own input, replace `example_input.txt` with the file path pointing to your data file. A message will be output telling you where the HTML was saved, and how many stages are needed:

```
Timetable saved to timetable.html
Number of stages needed: 9
```

You can now open the HTML file in your browser to view it.

