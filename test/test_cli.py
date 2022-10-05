import zoe.cli as cli
import zoe.challenge as challenge


def test_challenge_solution():
    assert challenge.main(['zoe!', 'pascal.zoe']) == 0


def test_challenge_incorrect_solution():
    assert challenge.main(['zoe!', 'wrong.zoe']) != 0


def test_challenge_file_not_found():
    assert challenge.main(['zoe!', 'notfound.zoe']) != 0


def test_challenge_malformed():
    assert challenge.main(['zoe!', 'mal.zoe']) != 0


def test_challenge_no_arg():
    assert challenge.main(['zoe!']) != 0


def test_challenge_dir_arg():
    assert challenge.main(['zoe!', 'zoe']) != 0


def test_cli():
    assert cli.main(['zoe', 'hello.zoe']) == 0


def test_cli_file_not_found():
    assert cli.main(['zoe', 'notfound.zoe']) != 0


def test_cli_malformed():
    assert cli.main(['zoe', 'mal.zoe']) != 0


def test_cli_no_arg():
    assert cli.main(['zoe']) != 0


def test_cli_dir_arg():
    assert cli.main(['zoe', 'zoe']) != 0
