#!/usr/bin/python3

from hashlib import sha1
from pathlib import Path
import re

from brownie.types.types import _Singleton
from brownie._config import CONFIG


class Sources(metaclass=_Singleton):

    def __init__(self):
        self._source = {}
        self._uncommented_source = {}
        self._comment_offsets = {}
        self._fn_map = {}
        self._path = None
        self._data = {}
        self._inheritance_map = {}
        self._string_iter = 1

    def _load(self):
        base_path = Path(CONFIG['folders']['project'])
        self. _path = base_path.joinpath('contracts')
        for path in [i.relative_to(base_path) for i in self._path.glob('**/*.sol')]:
            if "/_" in str(path):
                continue
            source = path.open().read()
            self._source[str(path)] = source
            self._remove_comments(path)
            self._get_contract_data(path)
        for name, inherited in [(k, v['inherited'].copy()) for k, v in self._data.items()]:
            self._data[name]['inherited'] = self._recursive_inheritance(inherited)

    def _remove_comments(self, path):
        source = self._source[str(path)]
        offsets = [(0, 0)]
        pattern = "((?:\s*\/\/[^\n]*)|(?:\/\*[\s\S]*?\*\/))"
        for match in re.finditer(pattern, source):
            offsets.append((
                match.start() - offsets[-1][1],
                match.end() - match.start() + offsets[-1][1]
            ))
        self._uncommented_source[str(path)] = re.sub(pattern, "", source)
        self._comment_offsets[str(path)] = offsets[::-1]

    def _get_contract_data(self, path):
        contracts = re.findall(
            "((?:contract|library|interface)[^;{]*{[\s\S]*?})\s*(?=contract|library|interface|$)",
            self._uncommented_source[str(path)]
        )
        for source in contracts:
            type_, name, inherited = re.findall(
                "\s*(contract|library|interface) (\S*) (?:is (.*?)|)(?: *{)",
                source
            )[0]
            inherited = set(i.strip() for i in inherited.split(', ') if i)
            offset = self._uncommented_source[str(path)].index(source)
            self._data[name] = {
                'sourcePath': str(path),
                'type': type_,
                'inherited': inherited.union(re.findall("(?:;|{)\s*using *(\S*)(?= for)", source)),
                'sha1': sha1(source.encode()).hexdigest(),
                'fn_offsets': [],
                'offset': (
                    self._commented_offset(path, offset),
                    self._commented_offset(path, offset + len(source))
                )
            }
            if type_ == "interface":
                continue
            fn_offsets = []
            for idx, pattern in enumerate((
                # matches functions
                "function\s*(\w*)[^{;]*{[\s\S]*?}(?=\s*function|\s*})",
                # matches public variables
                "(?:{|;)\s*(?!function)(\w[^;]*(?:public\s*constant|public)\s*(\w*)[^{;]*)(?=;)"
            )):
                for match in re.finditer(pattern, source):
                    fn_offsets.append((
                        self._commented_offset(path, match.start(idx) + offset),
                        self._commented_offset(path, match.end(idx) + offset),
                        match.groups()[idx]
                    ))
            self._data[name]['fn_offsets'] = sorted(fn_offsets, key=lambda k: k[0], reverse=True)

    def _commented_offset(self, path, offset):
        return offset + next(i[1] for i in self._comment_offsets[str(path)] if i[0] <= offset)

    def _recursive_inheritance(self, inherited):
        final = set(inherited)
        for name in inherited:
            final |= self._recursive_inheritance(self._data[name]['inherited'])
        return final

    def get_hash(self, contract_name):
        return self._data[contract_name]['sha1']

    def get_path(self, contract_name):
        return self._data[contract_name]['sourcePath']

    def get_type(self, contract_name):
        return self._data[contract_name]['type']

    def get_fn(self, name, start, stop):
        if name not in self._data:
            name = next((
                k for k, v in self._data.items() if v['sourcePath'] == str(name) and
                v['offset'][0] <= start <= stop <= v['offset'][1]
            ), False)
            if not name:
                return False
        offsets = self._data[name]['fn_offsets']
        if start < offsets[-1][0]:
            return False
        offset = next(i for i in offsets if start >= i[0])
        return False if stop >= offset[1] else offset[2]

    def inheritance_map(self):
        return dict((k, v['inherited'].copy()) for k, v in self._data.items())

    def __getitem__(self, key):
        if key in self._data:
            return self._source[self._data[key]['sourcePath']]
        return self._source[str(key)]

    def add_source(self, source):
        path = "<string-{}>".format(self._string_iter)
        self._source[path] = source
        self._get_contract_data(path)
        self._string_iter += 1
        return path
