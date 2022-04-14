# HfM-roombooker

This is a program for booking a practice room in HfM (Hochschule für Musik Karlsruhe).

## Implementation
Automated web operations using **selenium**
The program has 2 modes:
### 1. Normal Mode  
**Input**: desired start time, end time, room number(if need), date(if need, default value = today+7)  
**Output**:  
-  if date = today+7, Auto-timed room booking + extended time to set end time (If not found in the set period will automatically shift the preset start and end time back 15 minutes)  
- if date before today+7, search and book available rooms immediately

### 2. Extension time of the booked room  
This mode is used to automatic extend the time for the booked room.
**Input**: date(default:today+7), start time, desired end time
**Output**: The room is extended to the set given time.
