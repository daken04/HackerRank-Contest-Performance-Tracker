import csv
import getpass
import sys
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def print_get_contest(email, password):
    contestsr = requests.get(
        "https://www.hackerrank.com/rest/administration/contests",
        params={"offset": 0, "limit": 100},
        auth=(email, password), headers=headers)

    if contestsr.status_code != 200:
        print(contestsr.status_code)
        print("Error getting contests. Exiting...")
        sys.exit(-1)

    contests_dict = contestsr.json()

    if not contests_dict['status']:
        print("No success getting contests. Exiting...")
        sys.exit(-1)

    contests_list = contests_dict['models']

    for i in range(len(contests_list)):
        print("%d) %s (%s)" % (i+1, contests_list[i]['name'], contests_list[i]['slug']))

    c_no = int(input("Enter contest no :"))

    if c_no-1 >= len(contests_list):
        print("Invalid contest no. Exiting...")
        sys.exit(-1)

    return contests_list[c_no-1]['slug'], contests_list[c_no-1]['id']


def get_leaderboard_data(email, password, slug):
    # Fetch leaderboard data from both pages
    lbr1 = requests.get(
        f"https://www.hackerrank.com/rest/contests/{slug}/leaderboard",
        params={"offset": 0, "limit": 100},
        auth=(email, password), headers=headers)

    lbr2 = requests.get(
        f"https://www.hackerrank.com/rest/contests/{slug}/leaderboard",
        params={"offset": 100, "limit": 100},
        auth=(email, password), headers=headers)

    if lbr1.status_code != 200 or lbr2.status_code != 200:
        print("Error getting leaderboard. Exiting...")
        sys.exit(-1)

    # Combine both pages of results
    lb_list1 = lbr1.json()['models']
    lb_list2 = lbr2.json()['models']
    lb_list = lb_list1 + lb_list2

    leaderboard_dict = {entry['hacker']: {'rank': entry['rank'], 'score': entry['score']} for entry in lb_list}
    return leaderboard_dict


def get_contest_details(email, password, slug):
    challenges_request = requests.get(
        f"https://www.hackerrank.com/rest/contests/{slug}/challenges",
        auth=(email, password), headers=headers)

    if challenges_request.status_code != 200:
        print("Error getting challenges. Exiting...")
        sys.exit(-1)

    challenges_list = challenges_request.json()['models']
    return challenges_list


def get_problem_scores(email, password, slug, problem_slug, max_score):
    # Fetch problem scores from both pages
    problem_leaderboard1 = requests.get(
        f"https://www.hackerrank.com/rest/contests/{slug}/challenges/{problem_slug}/leaderboard",
        params={"offset": 0, "limit": 100},
        auth=(email, password), headers=headers)

    problem_leaderboard2 = requests.get(
        f"https://www.hackerrank.com/rest/contests/{slug}/challenges/{problem_slug}/leaderboard",
        params={"offset": 100, "limit": 100},
        auth=(email, password), headers=headers)

    if problem_leaderboard1.status_code != 200 or problem_leaderboard2.status_code != 200:
        print("Error getting problem leaderboard. Exiting...")
        sys.exit(-1)

    # Combine both pages of results
    problem_list1 = problem_leaderboard1.json()['models']
    problem_list2 = problem_leaderboard2.json()['models']
    problem_list = problem_list1 + problem_list2

    problem_scores = {entry['hacker']: 1 if entry['score'] == max_score else 0 for entry in problem_list}
    return problem_scores


def create_leaderboard_file(email, password):
    con_slug, con_id = print_get_contest(email, password)
    leaderboard_dict = get_leaderboard_data(email, password, con_slug)
    challenges_list = get_contest_details(email, password, con_slug)

    # Field names for CSV
    problem_fields = [f"problem{i+1}-{c['name']}-{c['difficulty_name']}" for i, c in enumerate(challenges_list)]
    fieldnames = ['name'] + problem_fields + ['rank', 'score']

    # Prepare problem-wise scores dictionary
    problem_scores_dict = {hacker: {field: 0 for field in problem_fields} for hacker in leaderboard_dict}

    # Fetch problem scores
    for i, challenge in enumerate(challenges_list):
        problem_slug = challenge['slug']
        max_score = challenge['max_score']
        problem_scores = get_problem_scores(email, password, con_slug, problem_slug, max_score)

        for hacker, score in problem_scores.items():
            # Dynamically add missing hackers
            if hacker not in problem_scores_dict:
                problem_scores_dict[hacker] = {field: 0 for field in problem_fields}
                # Default rank and score if the hacker is not in the overall leaderboard
                problem_scores_dict[hacker]['rank'] = None
                problem_scores_dict[hacker]['score'] = None

            problem_scores_dict[hacker][f"problem{i+1}-{challenge['name']}-{challenge['difficulty_name']}"] = score

    # Write to CSV
    with open(f'leaderboard-{con_slug}.csv', 'w') as lbf:
        writer = csv.DictWriter(lbf, fieldnames=fieldnames)
        writer.writeheader()

        for hacker, details in problem_scores_dict.items():
            row = {'name': hacker, 'rank': leaderboard_dict.get(hacker, {}).get('rank', 'N/A'), 'score': leaderboard_dict.get(hacker, {}).get('score', 'N/A')}
            row.update(details)
            writer.writerow(row)

    return True


def main():
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")

    if create_leaderboard_file(email, password):
        print("Done")



if __name__ == '__main__':
    main()
