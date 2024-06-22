import subprocess
import time

process = subprocess.Popen(["python3", "-u", "MLsubgroup/Mocked_Stream_and_classify.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,)



process.stdin.write(b"2\n")
process.stdin.flush()
i = 0

for i in range(20):
    character = process.stdout.read1(1)
    print(character.decode('UTF-8'))
    character = process.stdout.read1(1)
    

process.kill()
