<h1 style="text-align: center"> ReportCheck </h1>

## Install

```shell
pip3 install https://github.com/Rhythmicc/ReportCheck.git -U
```

## Usage

```shell
cup-rc --help

cup-rc [--press] remote_url username password email email_password email_smtp to1 to2 ...
```

## Developer

If you need use global config, just edit `__config__.py`:

1. make `enable_config = True`.
2. edit `questions` list.
3. using `config` at `main.py`.
