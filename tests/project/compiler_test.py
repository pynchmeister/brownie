#!/usr/bin/python3

import pytest
import solcx


from brownie import config
from brownie.project import build, compiler, sources
from brownie.exceptions import CompilerError, ContractExists

sources = sources.Sources()


@pytest.fixture(scope="function")
def version():
    yield
    config['solc']['version'] = "v0.5.7"
    compiler.set_solc_version()


def _solc_5_source():
    source = sources['BrownieTester']
    source = source.replace('BrownieTester', 'TempTester')
    source = source.replace('UnlinkedLib', 'TestLib')
    return source


def _solc_4_source():
    source = _solc_5_source()
    source = source.replace('payable ', '')
    source = source.replace('^0.5.0', '^0.4.25')
    return source


def test_build_keys():
    build_json = compiler.compile_contracts(["contracts/BrownieTester.sol"])
    assert set(build.BUILD_KEYS) == set(build_json['BrownieTester'])


def test_contract_exists():
    with pytest.raises(ContractExists):
        compiler.compile_source(sources['BrownieTester'])
    compiler.compile_contracts(["contracts/BrownieTester.sol"])


def test_set_solc_version(version):
    config['solc']['version'] = "v0.5.0"
    compiler.set_solc_version()
    assert config['solc']['version'] == solcx.get_solc_version_string().strip('\n')


def test_unlinked_libraries(version):
    source = _solc_5_source()
    build_json = compiler.compile_source(source)
    assert '__TestLib__' in build_json['TempTester']['bytecode']
    config['solc']['version'] = "v0.4.25"
    compiler.set_solc_version()
    source = _solc_4_source()
    build_json = compiler.compile_source(source)
    assert '__TestLib__' in build_json['TempTester']['bytecode']


def test_compiler_errors(version):
    with pytest.raises(CompilerError):
        compiler.compile_contracts(["contracts/Token.sol"])
    compiler.compile_contracts(["contracts/Token.sol", "contracts/SafeMath.sol"])
    source = _solc_4_source()
    with pytest.raises(CompilerError):
        compiler.compile_source(source)
    config['solc']['version'] = "v0.4.25"
    compiler.set_solc_version()
    compiler.compile_source(source)
