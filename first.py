#!/usr/bin/env python3
import os
import time

start = time.time()
time.sleep(5)
end = time.time()
duration = round(end - start, 2)
m = __file__ + " was ran for " + str(duration) + " seconds."
with open("squirm.log", "a") as file:
    file.write(m + "\n")
print(m)
