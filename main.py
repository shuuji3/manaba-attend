import os
import argparse
from getpass import getpass
import yaml
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome


class Manaba:

    def __init__(self):
        self.attend_url = 'https://atmnb.tsukuba.ac.jp/attend/tsukuba'
        self.br = Chrome()
        self.load_credentials()

    def load_credentials(self):
        credentials_path = os.path.expanduser('~/.manaba_attend')
        if not os.path.exists(credentials_path):
            print('Enter your credentials')
            self.id = input('id: ')
            self.password = getpass()
            with open(credentials_path, 'w') as f:
                yaml.dump({'id': self.id, 'password': self.password}, f)
            os.chmod(credentials_path, 0o600)
        else:
            with open(credentials_path) as f:
                credentials = yaml.load(f)
                self.id = credentials['id']
                self.password = credentials['password']

    def make_soup(self):
        return BeautifulSoup(self.br.page_source, 'lxml')

    def send_code(self, attend_code):
        # 1. Enter attend code
        self.br.get(self.attend_url)
        self.br.find_element_by_css_selector('[name="code"]').send_keys(attend_code + '\n')

        # attend_codeに誤りがある場合、ログイン画面には遷移しない
        s = self.make_soup()
        error = s.select('.errmsg')
        if error:
            success = False
            print(error[0].text)
            print('!!! attend failed !!!')
            return

        # 2. Login to manaba
        self.br.find_element_by_css_selector('#username').send_keys(self.id)
        self.br.find_element_by_css_selector('#password').send_keys(self.password)

        # 3. Check the state
        s = self.make_soup()
        error = s.select('.errmsg')
        if error:
            success = False
            print(error[0].text)
        else:
            body = s.select('.attend-box-body')[0].text
            description = s.select('.description')[0].text.strip()
            if '提出済' in description:
                success = True
                print(body)
            elif '提出しました' in description:
                success = True
                print(body)
            else:
                success = False
                print(body)
                print('Unknown result')

        if not success:
            print('!!! attend failed !!!')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('attend_code')
    args = ap.parse_args()

    manaba = Manaba()
    manaba.send_code(args.attend_code)