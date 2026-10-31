# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Run every .ost script under scripts/ with the Ossie functions."""

import sys
from pathlib import Path

import pytest

ossie_ost = pytest.importorskip("ossie_ost")
pytest.importorskip("yaml")
pytest.importorskip("jsonschema")
pytest.importorskip("sqlglot")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ost_functions import FUNCTIONS  # noqa: E402

SCRIPTS = sorted((Path(__file__).parent / "scripts").glob("*.ost"))


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_script(script: Path):
    text = script.read_text(encoding="utf-8")
    result = ossie_ost.run(text, str(script), functions=FUNCTIONS)
    assert result.output == text
