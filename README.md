# Flent tests on Dumbell Topology

## Requirements Setup

* nitk-nest

```bash
python3 -m pip install nitk-nest
```

* flent

```bash
sudo add-apt-repository ppa:tohojo/flent
sudo apt install flent
```

* Clone/Download the repository

```bash
git clone https://github.com/shashank68/flent-aqm-tests
```

## Running the tests

```bash
sudo python3 dumbell_experiment.py
```

## Inspecting the results with flent-gui

```bash
flent-gui results/<result_file>.flent.gz
```
