{% set conceptnet5_dir = "/home/conceptnet/conceptnet5" %}
{% set conceptnet5_virtualenv_dir = "/home/conceptnet/conceptnet5_virtualenv" %}
{% set python_version = "3.7.9" %}

conceptnet5_repo:
  git.latest:
    - name: https://github.com/commonsense/conceptnet5.git
    - rev: 8b11062866c1791f003bf0de4542c35f0c118dfc
    - user: conceptnet
    - target: {{ conceptnet5_dir }}
    - require:
      - user: conceptnet

conceptnet5_deps:
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
      - git: conceptnet5_repo

{{ conceptnet5_virtualenv_dir }}:
  virtualenv.managed:
    - venv_bin: /usr/local/pyenv/versions/{{ python_version }}/bin/virtualenv
    - python: /usr/local/pyenv/versions/{{ python_version }}/bin/python3
    - require:
      - pyenv: python-{{ python_version }}
      - pip: virtualenv

conceptnet5_package:
  pip.installed:
    - editable: {{ conceptnet5_dir }}[vectors]
    - bin_env: {{ conceptnet5_virtualenv_dir }}
    - require:
      - virtualenv: {{ conceptnet5_virtualenv_dir }}

conceptnet5_benchmark:
  pip.installed:
    - requirements: salt://requirements/conceptnet5_benchmark.txt
    - bin_env: {{ conceptnet5_virtualenv_dir }}
    - require:
      - pip: conceptnet5_package

conceptnet5_system_requirements:
  pip.installed:
    - requirements: salt://requirements/system_requirements.txt
    - bin_env: {{ conceptnet5_virtualenv_dir }}
    - require:
      - pip: conceptnet5_package
