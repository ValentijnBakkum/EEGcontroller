import subprocess

process = subprocess.Popen(["python3", "-u", "MeasurementSubgroup/Streaming/Subrotine test/sub.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,)



character = process.stdout.read1(1)
process.stdin.write(b"G\n") # G for go
process.stdin.flush()

process.communicate()
