import urllib
import json
import time, os

MAX_SUBS = 1000000
MAX_CF_CONTEST_ID = 600
MAGIC_START_POINT = 17000

SOURCE_CODE_BEGIN = '<pre class="prettyprint" style="padding:0.5em;">'
SUBMISSION_URL = 'http://codeforces.com/contest/{ContestId}/submission/{SubmissionId}'
USER_INFO_URL = 'http://codeforces.com/api/user.status?handle={handle}&from=1&count={count}'

EXT = {'C++': 'cpp', 'C': 'c', 'Java': 'java', 'Python': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}
EXT_keys = EXT.keys()

replacer = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'"}
keys = replacer.keys()

def get_ext(comp_lang):
    if 'C++' in comp_lang:
        return 'cpp'
    for key in EXT_keys:
        if key in comp_lang:
            return EXT[key]
    return ""

def parse(source_code):
    for key in keys:
        source_code = source_code.replace(key, replacer[key])
    return source_code

handle='tacklemore'

if not os.path.exists(handle):
    os.makedirs(handle)

user_info = urllib.urlopen(USER_INFO_URL.format(handle=handle, count=MAX_SUBS)).read()
dic = json.loads(user_info)
if dic['status'] != u'OK':
    print 'Oops.. Something went wrong...'
    exit(0)

submissions = dic['result']
start_time = time.time()

for submission in submissions:
    if submission['verdict'] == u'OK' and submission['contestId'] < MAX_CF_CONTEST_ID:
        con_id, sub_id = submission['contestId'], submission['id'],
        prob_name, prob_id = submission['problem']['name'], submission['problem']['index']
        comp_lang = submission['programmingLanguage']
        submission_info = urllib.urlopen(SUBMISSION_URL.format(ContestId=con_id, SubmissionId=sub_id)).read()
        
        start_pos = submission_info.find(SOURCE_CODE_BEGIN, MAGIC_START_POINT) + len(SOURCE_CODE_BEGIN)
        end_pos = submission_info.find("</pre>", start_pos)
        result = parse(submission_info[start_pos:end_pos]).replace('\r', '')
        ext = get_ext(comp_lang)
        
        new_directory = handle + '/' + str(con_id)
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
        file = open(new_directory + '/' + prob_id + '[ ' + prob_name + ' ]' + '.' + ext, 'w')
	file.write(result)
	file.close()		
end_time = time.time()

print 'Execution time %d seconds' % int(end_time - start_time)
