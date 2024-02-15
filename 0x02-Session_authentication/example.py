from datetime import datetime, timedelta
import time

d = 60
session_dictionary = {'user_id': '123', 'created_at': datetime.now()}
time.sleep(3)
delta = datetime.now() - session_dictionary.get('created_at')

print(delta)

if delta >= timedelta(seconds=d):
    print('done')
else:
    print('not done')

