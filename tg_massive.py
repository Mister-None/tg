import subprocess, sys, time, os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.getenv('DOTENV_FILE_PATH'))

TBOT = os.getenv('tbot')

if len(sys.argv) < 3:
    print("Enter number of function and range of bots!!!")
    sys.exit(1)


function = int(sys.argv[1])

if function in [4, 12, 13, 24]:
    option = int(sys.argv[3])

elif function in [11]:
    option = sys.argv[3]

else: option = ''

bots_id = str(sys.argv[2]).split('-')
next_bot_id, last_bot_id = int(bots_id[0]), int(bots_id[-1])

for k in range(last_bot_id+1):
    if last_bot_id >= k >= next_bot_id:
        subprocess.Popen(f'terminator --new-tab -e \'bash -c "source work/bin/activate; python {TBOT} {function} {k} {option}; exec bash"\'', shell=True)
        time.sleep(1)
