from pathlib import Path
import json

BASE_DIR = "./Result"
NUM_OF_CHALLENGE = 6.0


def getUsers():
    # get all the files
    results = Path(BASE_DIR).glob('*')
    # get users
    return list(map(lambda x: str(x).split('/')[1], results))


def filterTries(tries):
    result = []
    for t in tries:
        if t['if_success'] == True:
            result.append(t)
            return result
        else:
            result.append(t)
    return result


def analyseOneFile(file):
    try:
        with open(file) as json_file:
            result = json.load(json_file)
            c_list = result['challenge_list']
            tries = 0.0
            successes = 0.0
            overall_quality_achieved = 0.0
            all_failure = 0.0
            for c in c_list:
                target = c['target']
                filtered_tries = filterTries(c['logs']['tries'])
                tries_per_c = len(filtered_tries)
                if tries_per_c == 0:  # may have missed this
                    continue
                tries += tries_per_c
                qualities = list(map(lambda x: x['quality_percent'], filtered_tries))
                success = True in list(map(lambda x: x['if_success'], filtered_tries))
                all_fail = not (False in list(map(lambda x: x['quality_percent'] == -1, filtered_tries)))
                if success:
                    successes += 1
                    overall_quality_achieved += 1.0
                else:
                    overall_quality_achieved += max(
                        list(map(lambda x: 1.0 - abs(((0 if x == -1 else x) - target) / target), qualities)))
                if all_fail:
                    all_failure += 1
            return {'tries': tries / NUM_OF_CHALLENGE, 'success_rate': successes / NUM_OF_CHALLENGE,
                    'quality': overall_quality_achieved / NUM_OF_CHALLENGE, "all_fail": all_failure / NUM_OF_CHALLENGE}
    except Exception as e:
        print("fail to parse ", file, str(e))
        return None


def summarizeOne(result, resultAll):
    if result is None:
        return False
    for k, v in result.items():
        if not k in resultAll:
            resultAll[k] = 0.0
        resultAll[k] += v
    return True


def scanAll():
    users = getUsers()
    concrete_overall = {}
    virtual_overall = {}
    tot_virtual = 0.0
    tot_concrete = 0.0
    for user in users:
        print("scanning:", user)
        concrete_file = BASE_DIR + '/' + user + '/study_logs_concrete.json'
        virtual_file = BASE_DIR + '/' + user + '/study_logs_virtual.json'
        concrete_res = analyseOneFile(concrete_file)
        if summarizeOne(concrete_res, concrete_overall):
            tot_concrete += 1
        virtual_res = analyseOneFile(virtual_file)
        if summarizeOne(virtual_res, virtual_overall):
            tot_virtual += 1
    for k, v in virtual_overall.items():
        virtual_overall[k] = v / tot_virtual
        concrete_overall[k] = concrete_overall[k] / tot_concrete
    print(virtual_overall, concrete_overall)


scanAll()
