{% set conceptnet5_dir = "/home/conceptnet/conceptnet5" %}
{% set conceptnet5_virtualenv_dir = "/home/conceptnet/conceptnet5-virtualenv" %}
{% set python_version = "3.7.8" %}

conceptnet5-repo:
  git.latest:
    - name: https://github.com/commonsense/conceptnet5.git
    - rev: 096b7457f54ca3c1f34ff59192ee3cd751d6a1eb
    - user: conceptnet
    - target: {{ conceptnet5_dir }}
    - require:
      - user: conceptnet

conceptnet5-deps:
  pkg.installed:
    - pkgs:
      - build-essential
      - python3-dev
      - libhdf5-dev
      - libmecab-dev
      - mecab-ipadic-utf8

{{ conceptnet5_dir }}/data:
  file.directory:
    - user: conceptnet
    - group: users
    - require:
      - user: conceptnet
      - git: conceptnet5-repo

{{ conceptnet5_virtualenv_dir }}:
  virtualenv.managed:
    - venv_bin: /usr/local/pyenv/versions/{{ python_version }}/bin/virtualenv
    - python: /usr/local/pyenv/versions/{{ python_version }}/bin/python3
    - require:
      - pyenv: python-{{ python_version }}
      - pip: virtualenv

conceptnet5-package:
  pip.installed:
    - editable: {{ conceptnet5_dir }}[vectors]
    - bin_env: {{ conceptnet5_virtualenv_dir }}
    - require:
      - virtualenv: {{ conceptnet5_virtualenv_dir }}

conceptnet5-benchmark:
  pip.installed:
    - requirements: salt://requirements/conceptnet5_benchmark.txt
    - bin_env: {{ conceptnet5_virtualenv_dir }}
    - require:
      - pip: conceptnet5-package

conceptnet5-system-requirements:
  pip.installed:
    - requirements: salt://requirements/system_requirements.txt
    - bin_env: {{ conceptnet5_virtualenv_dir }}
    - require:
      - pip: conceptnet5-package
