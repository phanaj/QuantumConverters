# ES170 Project

Python Alibaba Interface demonstrates a way to interface with the Alibaba Quantum Computer.  
Quil2Qasm is a command line tool that allows easy conversion of .quil files into .qasm files.

## Dependencies

The following dependencies are necessary to run the Alibaba Interface.

#### Splinter

Follow the installation guide here to get splinter: [splinter setup](https://splinter.readthedocs.io/en/latest/install.html)  
Follow the installation guide here to set up Firefox driver: [Firefox driver setup](https://splinter.readthedocs.io/en/latest/drivers/firefox.html)

#### Requests

```bash
pip install requests
```

## Installation

Git clone this repo:

```bash
git clone https://github.com/lepmichael/ES170-Quil2Qasm-And-Python-Interface.git
```

## Usage

### Quil2Qasm

`Quil2Qasm.py` takes in one or more directories of `.quil` files as input, such as

```bash
python Quil2Qasm.py data/tests/hello_world.quil data/tests/qft.quil
```

Run `python Quil2Qasm.py --help` for additional arguments.

### Alibaba Interface

See [docstrings](https://github.com/lepmichael/ES170-Quil2Qasm-And-Python-Interface/blob/master/Alibaba-Python-Interface.ipynb).


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
