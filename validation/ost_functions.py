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

"""Ossie functions for .ost scripts.

FUNCTIONS adds validate(model) to the built-in .ost functions. It runs
every check in validate.py on a YAML document held in a string, and
returns "valid", or one line per diagnostic, each starting with
"error:" or "warning:". A script that calls it is a validation test
whose expected output sits next to the model it checks.
"""

import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from ossie_ost import Function, Kind


def _load_validate():
    path = Path(__file__).resolve().parent / "validate.py"
    spec = spec_from_file_location("ossie_validate", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_validate = _load_validate()
_schema = json.loads(_validate.default_schema_path().read_text(encoding="utf-8"))


def validate(_session, text: str) -> str:
    data = _validate.load_yaml_named(text, "<model>")
    problems = _validate.validate_document(data, _schema)
    if not problems:
        return "valid"
    return "\n".join(
        ("warning: " if isinstance(p, _validate.ValidationWarning) else "error: ") + p
        for p in problems
    )


FUNCTIONS = {"validate": Function((Kind.STRING,), validate)}
