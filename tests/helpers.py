"""Helpers used in testing the tool."""

from contextlib import contextmanager
import mock

from click.testing import CliRunner

from cloudformation_helper import cli


@contextmanager
def cfhelper_mocks():
    session_mock = mock.MagicMock()
    client_mock = mock.MagicMock()

    with mock.patch("cloudformation_helper.utils.aws.boto3") as boto3_mock:
        boto3_mock.Session.return_value = session_mock
        session_mock.client.return_value = client_mock
        yield boto3_mock, session_mock, client_mock


def call_cfhelper(call_args, input=None):
    runner = CliRunner()

    result = runner.invoke(
        cli.cfhelper,
        call_args,
        input=input,
        catch_exceptions=False,
    )

    print(result.output)
    return result
