# import math
# for i in range(1, 2880, 10):
#     item = {"min_passed": i}
#     time_penalizer = 1 / (1 + math.exp((-item["min_passed"]-100) / (60 * 12))) ** 2
#     print(f"{(i/60):.2f}h score: {time_penalizer:.2f}")


import util
util.update_hotness()
