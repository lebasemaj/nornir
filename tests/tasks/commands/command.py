from brigade.core.exceptions import BrigadeExecutionError, CommandError
from brigade.plugins.tasks import commands

import pytest


class Test(object):

    def test_command(self, brigade):
        result = brigade.run(commands.command,
                             command="echo {host.name}")
        assert result
        for h, r in result.items():
            assert h, result.stdout

    def test_command_error(self, brigade):
        with pytest.raises(BrigadeExecutionError) as e:
            brigade.run(commands.command,
                        command="ech")
        assert len(e.value.failed_hosts) == len(brigade.inventory.hosts)
        for exc in e.value.failed_hosts.values():
            assert isinstance(exc, FileNotFoundError)

    def test_command_error_generic(self, brigade):
        with pytest.raises(BrigadeExecutionError) as e:
            brigade.run(commands.command,
                        command="ls /asdadsd")
        assert len(e.value.failed_hosts) == len(brigade.inventory.hosts)
        for exc in e.value.failed_hosts.values():
            assert isinstance(exc, CommandError)
