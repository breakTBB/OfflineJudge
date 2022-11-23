import httpx
import os
from os import system
from bs4 import BeautifulSoup

data = {
    'username' : 'prism17',
    'password' : '',
    'module' : 'Login'
}
problem_url = 'https://community.topcoder.com/stat?c=problem_solution&rm=319909&rd=15820&pm=12924&cr=22714443'
client = httpx.Client(params=data, follow_redirects=True)
res = client.get(url=problem_url)

test_list, answer_list,null_list = [], [], []

if res.status_code == 200:
    page = BeautifulSoup(res.content,'lxml')
    testcases = page.find_all('td', class_='statText')
    ok, turn = False, 0
    for case in testcases:
        text = case.text
        if ok:
            [test_list, answer_list, null_list][turn].append(text)
            turn = (turn + 1) % 3
        if text == 'Success':
            ok = True
    T = len(test_list)

    print('pending')

    # be careful!!!
    # it will overwrite some file
    # like ['main_you_wont_name_it_like_this.cpp','{user}input.txt', '{user}output.txt' ]
    # in this file's folder.
    for i in range(T):
        print(f'#Case {i}')

        # save test case to file
        with open('input.txt', 'w') as f:
            f.write(test_list[i])
            print(f'input saved as {os.path.realpath(f.name)}')
        with open('output.txt', 'w') as f:
            f.write(answer_list[i])
            print(f'output saved as {os.path.realpath(f.name)}')

        # generate main cpp file
        # make sure your code in main.cpp and method has the placeholder ${input}
        with open('main.cpp') as code:
            text = code.readlines()
            text = [l.replace('${input}', test_list[i]) for l in text]
            with open('you_wont_name_it_like_this.cpp', 'w') as newCode:
                newCode.writelines([l for l in text])
            system('g++ -o you_wont_name_it_like_this you_wont_name_it_like_this.cpp')
            system('you_wont_name_it_like_this < input.txt > user_output')
            if system('fc user_output output.txt'):
                print('Wrong Answer')
                print(f'input: {test_list[i]}')
                print(f'expected: {answer_list[i]}')
                exit(0)
            print('Accept')
else:
    print('fail to connect topcoder')
    exit(0)

