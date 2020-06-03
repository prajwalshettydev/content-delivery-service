import sys 

sys.stderr = open('log_err.txt', 'w', 1)
sys.stdout = open('log.txt', 'w', 1)