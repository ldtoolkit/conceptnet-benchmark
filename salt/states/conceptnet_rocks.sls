{% set conceptnet5_dir = "/home/conceptnet/conceptnet5" %}
{% set conceptnet_rocks_virtualenv_dir = "/home/conceptnet/conceptnet_rocks_virtualenv" %}
{% set conceptnet_rocks_dir = "/home/conceptnet/conceptnet_rocks" %}
{% set python_version = "3.7.9" %}

{{ conceptnet_rocks_virtualenv_dir }}:
  virtualenv.managed:
    - venv_bin: /usr/local/pyenv/versions/{{ python_version }}/bin/virtualenv
    - python: /usr/local/pyenv/versions/{{ python_version }}/bin/python3
    - require:
      - pyenv: python-{{ python_version }}
      - pip: virtualenv

conceptnet_rocks_repo:
  git.latest:
    - name: https://github.com/ldtoolkit/conceptnet-rocks.git
    - rev: bd94cc6817cdd03a4eeb80418aab372a9f6ad5ab
    - user: conceptnet
    - target: {{ conceptnet_rocks_dir }}
    - require:
      - user: conceptnet

conceptnet_rocks_package:
  pip.installed:
    - name: {{ conceptnet_rocks_dir }}
    - bin_env: {{ conceptnet_rocks_virtualenv_dir }}
    - require:
      - virtualenv: {{ conceptnet_rocks_virtualenv_dir }}

conceptnet_rocks_benchmark:
  pip.installed:
    - requirements: salt://requirements/conceptnet_rocks_benchmark.txt
    - bin_env: {{ conceptnet_rocks_virtualenv_dir }}
    - require:
      - pip: conceptnet_rocks_package

conceptnet_rocks_system_requirements:
  pip.installed:
    - requirements: salt://requirements/system_requirements.txt
    - bin_env: {{ conceptnet_rocks_virtualenv_dir }}
    - require:
      - virtualenv: {{ conceptnet_rocks_virtualenv_dir }}
