import importlib
import os
import re
from pathlib import Path
from typing import Optional

import mypy.api
import pytest

here = Path(__file__).parent

cases = [
    ("data/mypy-config.ini", "data/simple.py", None),
]


@pytest.mark.parametrize("config_filename,python_filename,output_filename", cases)
def test_mypy_results(
    config_filename: Path, python_filename: Path, output_filename: Optional[str]
) -> None:
    output_path = None if output_filename is None else here / output_filename

    res = mypy.api.run(
        [
            "--config-file",
            str(here / config_filename),
            str(here / python_filename),
            # '--pdb',
            "--raise-exceptions",
            "--show-traceback",
            "--cache-dir=/dev/null",
        ]
    )
    print("STDOUT: \n", res[0])
    print("STDERR: \n", res[1])
    assert res[2] == 0
