import os
import tempfile
import sys
import json
from click.testing import CliRunner
from tests.utils import generate_fake_dataframe_model

try:
    from bentoml.cli import create_bentoml_cli
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from bentoml.cli import create_bentoml_cli


def generate_test_input_file():
    import uuid
    random_id = uuid.uuid4().hex
    tempdir = tempfile.mkdtemp()
    file_path = os.path.join(tempdir, random_id + '.json')

    with open(file_path, 'w') as f:
        f.write('[{"age": 1}, {"age": 2}]')
    return file_path


def test_run_command_with_input_file():
    saved_path = generate_fake_dataframe_model()
    input_path = generate_test_input_file()
    runner = CliRunner()

    cli = create_bentoml_cli()
    run_cmd = cli.commands["<API_NAME>"]
    result = runner.invoke(
        run_cmd, ['predict', saved_path, '--input', input_path])

    assert result.exit_code == 0
    result_json = json.loads(result.output)
    assert result_json['age']['0'] == 6
