import shutil
from datetime import datetime, timedelta, date
# moving files from switch to afdeling prepress products
# checking time
from Paths.paden import *
time_passed = datetime.now()-timedelta(minutes=150)
print(time_passed)

timetestfile= itemnum_collection[0]
timestamp = date.fromtimestamp(timetestfile.stat().st_mtime)

timestamp_folder = datetime.fromtimestamp(test_hp_folder.stat().st_ctime)

past_time = date.today() - timedelta(days=1)

nu = datetime.now()

if nu.day == 5:
    hours = 48 +24
else:
    hours=24

print(hours)

def timeblock_to_watch_in(pdf_file):
    '''looking for the time the itemnumber folder was created
    ideally it would be between 6 and 1700 every workday'''

    timestamp_pdf_folder = datetime.fromtimestamp(pdf_file.parent.stat().st_ctime)

    moment_in_time = datetime.now()
    #als sat en sun and monday then look in friday

    if moment_in_time.day == 1 or 5 or 6: # 1 = monday match is an option match 1 = 3 match 6 = 2 match 7 =3
        days_to_search_in = 3
    else:
        days_to_search_in = 1

    untill = moment_in_time - timedelta(minutes=15)

    start_looking_time = moment_in_time - timedelta(days=days_to_search_in)

    print(start_looking_time,untill.hour)
    # look_back_in_time between 5 15 minutes ago and 24 hours
    if timestamp_pdf_folder > start_looking_time and timestamp_pdf_folder < untill:
        print(f"looking for tsf {timestamp_pdf_folder} between  {start_looking_time} and {untill}")
        return 1
    else:
        print(f'tsf {timestamp_pdf_folder} {start_looking_time}  not looking')
        return 0
