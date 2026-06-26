# pysdb - python structural database

GUI front-end to create, edit and manage the field structural geology data in sqlite3 file database
(SDB structural database). This database format is compatible with [readsdb QGIS3 plugin](https://github.com/ondrolexa/readsdb).

For advanced analyses and visualization, it could be used with [APSG](https://github.com/ondrolexa/apsg).

## How to install

It is strongly suggested to install **pysdb** into separate environment.

### Using uv (recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package and project manager.
Install it following the [official instructions](https://docs.astral.sh/uv/getting-started/installation/).

Install **pysdb3** as a standalone tool (uv manages an isolated environment automatically):

    uv tool install pysdb3

Then run it from anywhere:

    pysdb3

To upgrade later:

    uv tool upgrade pysdb3

### Using Python virtual environment

You can create a Python virtual environment. For Linux and macOS use:

    python -m venv .venv
    source .venv/bin/activate

for Windows use Command Prompt or PowerShell:

    python -m venv .venv
    .venv\Scripts\activate

> [!NOTE]
> On Microsoft Windows, it may be required to set the execution policy in PowerShell for the user.
> You can do this by issuing the following PowerShell command:
> ```
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

and install **pysdb** using pip within the environment:

    pip install pysdb3

To start pysdb, simply type:

    pysdb3

## Getting help

If you get any errors [open a new Issue](https://github.com/ondrolexa/pysdb/issues) providing
the versions from either command above, as well as any errors you saw in the console during the installation.


## License

pysdb is free software: you can redistribute it and/or modify it under the terms of the MIT License.
A copy of this license is provided in ``LICENSE`` file.
