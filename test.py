import util


def generate_test_submissions(print_em = False):
    # generate a list of submissions
    top = util.get_top(10000)
    submissions_clean = []
    for submission in top:
        if submission:
            submissions_clean.append(
                {
                    "platform": submission["platform"],
                    "score": submission["score"],
                    "min_passed": submission["min_passed"],
                    "subscribers": submission["subscribers"],
                    # "title": submission["title"],
                }
            )

    if print_em:
        for i in submissions_clean:
            print(f"{i},")

    return submissions_clean

test_submissions = generate_test_submissions(print_em = False)
test_submissions.pop()

for submission in test_submissions:
    hotness = util.get_hotness(submission)
    submission["hotness"] = hotness

# print out sorted list by hotness
test_submissions.sort(key=lambda x: x["hotness"])
for submission in test_submissions:
    print(f"{submission['platform']}: {submission['hotness']} : {submission['score']} : {submission['min_passed']} : {submission['subscribers']}")
    