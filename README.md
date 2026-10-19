# Generate the protobuf codecs

From the `leos-protobufs` directory, create a Python virtual environment,
install the pinned generator dependencies, and run the generator:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/generate.py
```

The generated nanopb C codecs are written to `generated/c`, and the generated
Python codecs are written to `generated/python`.
