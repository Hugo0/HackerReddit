import util


# def generate_test_submissions():
#     # generate a list of submissions
#     top = util.get_top(100)
#     submissions_clean = []
#     for submission in top:
#         submissions_clean.append(
#             {
#                 "platform": submission["platform"],
#                 "score": submission["score"],
#                 "min_passed": submission["min_passed"],
#                 "subscribers": submission["subscribers"],
#                 # "title": submission["title"],
#             }
#         )
#     for i in submissions_clean:
#         print(f"{i},")


test_submissions = [
    {"platform": "reddit", "score": 1110, "min_passed": 782, "subscribers": 646772},
    {"platform": "reddit", "score": 362, "min_passed": 529, "subscribers": 603325},
    {"platform": "hackernews", "score": 39, "min_passed": 47, "subscribers": None},
    {"platform": "reddit", "score": 922, "min_passed": 1158, "subscribers": 603325},
    {"platform": "hackernews", "score": 38, "min_passed": 58, "subscribers": None},
    {"platform": "reddit", "score": 50626, "min_passed": 781, "subscribers": 7780486},
    {"platform": "reddit", "score": 13, "min_passed": 94, "subscribers": 647187},
    {"platform": "reddit", "score": 215, "min_passed": 347, "subscribers": 996517},
    {"platform": "reddit", "score": 842, "min_passed": 950, "subscribers": 996277},
    {"platform": "reddit", "score": 1027, "min_passed": 1967, "subscribers": 646773},
    {"platform": "reddit", "score": 22618, "min_passed": 563, "subscribers": 7780806},
    {"platform": "hackernews", "score": 251, "min_passed": 346, "subscribers": None},
    {"platform": "hackernews", "score": 66, "min_passed": 147, "subscribers": None},
    {"platform": "reddit", "score": 1160, "min_passed": 1028, "subscribers": 1206865},
    {"platform": "hackernews", "score": 200, "min_passed": 318, "subscribers": None},
    {"platform": "reddit", "score": 468, "min_passed": 1316, "subscribers": 646772},
    {"platform": "reddit", "score": 2733, "min_passed": 1883, "subscribers": 1206865},
    {"platform": "hackernews", "score": 862, "min_passed": 876, "subscribers": None},
    {"platform": "hackernews", "score": 150, "min_passed": 278, "subscribers": None},
    {"platform": "reddit", "score": 234, "min_passed": 1066, "subscribers": 603325},
    {"platform": "reddit", "score": 6550, "min_passed": 918, "subscribers": 3869937},
    {"platform": "hackernews", "score": 827, "min_passed": 1090, "subscribers": None},
    {"platform": "hackernews", "score": 6, "min_passed": 41, "subscribers": None},
    {"platform": "hackernews", "score": 1209, "min_passed": 1454, "subscribers": None},
    {"platform": "reddit", "score": 31, "min_passed": 328, "subscribers": 647187},
    {"platform": "hackernews", "score": 20, "min_passed": 111, "subscribers": None},
    {"platform": "reddit", "score": 190, "min_passed": 1167, "subscribers": 646773},
    {"platform": "reddit", "score": 9048, "min_passed": 1431, "subscribers": 3869937},
    {"platform": "reddit", "score": 8, "min_passed": 150, "subscribers": 646773},
    {"platform": "reddit", "score": 476, "min_passed": 1352, "subscribers": 996278},
    {"platform": "hackernews", "score": 5, "min_passed": 50, "subscribers": None},
    {"platform": "reddit", "score": 23854, "min_passed": 1210, "subscribers": 7780487},
    {"platform": "hackernews", "score": 111, "min_passed": 400, "subscribers": None},
    {"platform": "reddit", "score": 13107, "min_passed": 851, "subscribers": 7780486},
    {"platform": "hackernews", "score": 167, "min_passed": 568, "subscribers": None},
    {"platform": "reddit", "score": 217, "min_passed": 867, "subscribers": 1036747},
    {"platform": "hackernews", "score": 233, "min_passed": 728, "subscribers": None},
    {"platform": "hackernews", "score": 1377, "min_passed": 2449, "subscribers": None},
    {"platform": "hackernews", "score": 42, "min_passed": 249, "subscribers": None},
    {"platform": "reddit", "score": 5, "min_passed": 80, "subscribers": 996519},
    {"platform": "reddit", "score": 3361, "min_passed": 1024, "subscribers": 3869938},
    {"platform": "hackernews", "score": 13, "min_passed": 119, "subscribers": None},
    {"platform": "reddit", "score": 78, "min_passed": 1021, "subscribers": 603325},
    {"platform": "reddit", "score": 43, "min_passed": 689, "subscribers": 603325},
    {"platform": "reddit", "score": 6, "min_passed": 170, "subscribers": 646774},
    {"platform": "reddit", "score": 3, "min_passed": 119, "subscribers": 603325},
    {"platform": "hackernews", "score": 18, "min_passed": 155, "subscribers": None},
    {"platform": "reddit", "score": 2436, "min_passed": 883, "subscribers": 3869937},
    {"platform": "hackernews", "score": 59, "min_passed": 343, "subscribers": None},
    {"platform": "reddit", "score": 574, "min_passed": 2069, "subscribers": 996278},
    {"platform": "hackernews", "score": 153, "min_passed": 670, "subscribers": None},
    {"platform": "hackernews", "score": 564, "min_passed": 1600, "subscribers": None},
    {"platform": "reddit", "score": 44, "min_passed": 686, "subscribers": 647187},
    {"platform": "reddit", "score": 3, "min_passed": 116, "subscribers": 647187},
    {"platform": "hackernews", "score": 265, "min_passed": 991, "subscribers": None},
    {"platform": "hackernews", "score": 234, "min_passed": 930, "subscribers": None},
    {"platform": "reddit", "score": 1424, "min_passed": 266, "subscribers": 7780487},
    {"platform": "hackernews", "score": 313, "min_passed": 1141, "subscribers": None},
    {"platform": "hackernews", "score": 312, "min_passed": 1146, "subscribers": None},
    {"platform": "hackernews", "score": 4, "min_passed": 63, "subscribers": None},
    {"platform": "reddit", "score": 291, "min_passed": 1375, "subscribers": 1036747},
    {"platform": "reddit", "score": 72, "min_passed": 1147, "subscribers": 603325},
    {"platform": "reddit", "score": 41, "min_passed": 725, "subscribers": 646774},
    {"platform": "hackernews", "score": 70, "min_passed": 446, "subscribers": None},
    {"platform": "hackernews", "score": 95, "min_passed": 568, "subscribers": None},
    {"platform": "hackernews", "score": 254, "min_passed": 1106, "subscribers": None},
    {"platform": "reddit", "score": 228, "min_passed": 1399, "subscribers": 996278},
    {"platform": "hackernews", "score": 74, "min_passed": 502, "subscribers": None},
    {"platform": "reddit", "score": 70, "min_passed": 1146, "subscribers": 646773},
    {"platform": "reddit", "score": 343, "min_passed": 1496, "subscribers": 1206865},
    {"platform": "hackernews", "score": 63, "min_passed": 490, "subscribers": None},
    {"platform": "reddit", "score": 4906, "min_passed": 764, "subscribers": 7780487},
    {"platform": "hackernews", "score": 80, "min_passed": 587, "subscribers": None},
    {"platform": "hackernews", "score": 204, "min_passed": 1107, "subscribers": None},
    {"platform": "hackernews", "score": 18, "min_passed": 221, "subscribers": None},
    {"platform": "hackernews", "score": 135, "min_passed": 863, "subscribers": None},
    {"platform": "reddit", "score": 4268, "min_passed": 764, "subscribers": 7780486},
    {"platform": "reddit", "score": 3, "min_passed": 90, "subscribers": 1036747},
    {"platform": "hackernews", "score": 84, "min_passed": 707, "subscribers": None},
    {"platform": "hackernews", "score": 81, "min_passed": 692, "subscribers": None},
    {"platform": "reddit", "score": 7280, "min_passed": 1196, "subscribers": 7780487},
    {"platform": "reddit", "score": 99, "min_passed": 1061, "subscribers": 996277},
    {"platform": "reddit", "score": 11, "min_passed": 492, "subscribers": 603325},
    {"platform": "reddit", "score": 2475, "min_passed": 616, "subscribers": 7780807},
    {"platform": "hackernews", "score": 137, "min_passed": 1085, "subscribers": None},
    {"platform": "hackernews", "score": 66, "min_passed": 697, "subscribers": None},
    {"platform": "reddit", "score": 1069, "min_passed": 381, "subscribers": 7780806},
    {"platform": "reddit", "score": 4, "min_passed": 136, "subscribers": 1036747},
    {"platform": "reddit", "score": 4695, "min_passed": 1070, "subscribers": 7780487},
    {"platform": "reddit", "score": 314, "min_passed": 449, "subscribers": 3869937},
    {"platform": "hackernews", "score": 107, "min_passed": 1020, "subscribers": None},
    {"platform": "reddit", "score": 3574, "min_passed": 901, "subscribers": 7780487},
    {"platform": "reddit", "score": 22, "min_passed": 450, "subscribers": 1036862},
    {"platform": "hackernews", "score": 107, "min_passed": 1036, "subscribers": None},
    {"platform": "reddit", "score": 4087, "min_passed": 1003, "subscribers": 7780487},
    {"platform": "hackernews", "score": 95, "min_passed": 982, "subscribers": None},
    {"platform": "reddit", "score": 16813, "min_passed": 1039, "subscribers": 15673054},
    {"platform": "hackernews", "score": 115, "min_passed": 1131, "subscribers": None},
    {"platform": "reddit", "score": 1, "min_passed": 114, "subscribers": 647187},
    {"platform": "hackernews", "score": 80, "min_passed": 910, "subscribers": None},
]

for submission in test_submissions:
    hotness = util.get_hotness(submission)
    submission["hotness"] = hotness

# print out sorted list by hotness
test_submissions.sort(key=lambda x: x["hotness"])
for submission in test_submissions:
    print(f"{submission['platform']}: {submission['hotness']} : {submission['score']} : {submission['min_passed']} : {submission['subscribers']}")