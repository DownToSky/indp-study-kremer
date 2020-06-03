from pathlib import Path
import json

BASE_DIR = "./Result"
NUM_OF_CHALLENGE = 6.0


def getUsers():
    # get all the files
    results = Path(BASE_DIR).glob('*')
    # get users
    return list(map(lambda x: str(x).split('/')[1], results))


def analyseOneFile(file):
    with open(file) as json_file:
        result = json.load(json_file)
        c_list = result['challenge_list']
        tries = 0.0
        successes = 0.0
        overall_quality_achieved = 0.0
        for c in c_list:
            target = c['target']
            tries_per_c = len(c['logs']['tries'])
            if tries_per_c == 0:  # may have missed this
                continue
            tries += tries_per_c
            qualities = list(map(lambda x: x['quality_percent'], c['logs']['tries']))
            success = True in list(map(lambda x: x['if_success'], c['logs']['tries']))
            if success:
                successes += 1
                overall_quality_achieved += 1.0
            else:
                overall_quality_achieved += max(list(map(lambda x: 1.0 - abs((x - target) / target), qualities)))

        return {'tries': tries / NUM_OF_CHALLENGE, 'success_rate': successes / NUM_OF_CHALLENGE,
                'quality': overall_quality_achieved / NUM_OF_CHALLENGE}


def scanAll():
    users = getUsers()
    concrete_overall = {}
    virtual_overall = {}
    for user in users:
        print("scanning:", user)
        concrete_file = BASE_DIR + '/' + user + '/study_logs_concrete.json'
        virtual_file = BASE_DIR + '/' + user + '/study_logs_virtual.json'
        concrete_res = analyseOneFile(concrete_file)
        virtual_res = analyseOneFile(virtual_file)
        for k, v in concrete_res.items():
            if not k in concrete_overall:
                concrete_overall[k] = 0.0
            concrete_overall[k] += v
            if not k in virtual_overall:
                virtual_overall[k] = 0.0
            virtual_overall[k] += virtual_res[k]
    for k, v in virtual_overall.items():
        virtual_overall[k] = v / len(users)
        concrete_overall[k] = concrete_overall[k] / len(users)
    print(virtual_overall, concrete_overall)


scanAll()
