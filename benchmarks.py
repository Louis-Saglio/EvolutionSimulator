from lib import Being
import time

start = time.time()
print(Being.build_random(100000, 7)[0])
print(round((time.time() - start) * 1000, 2), "millisecondes")
