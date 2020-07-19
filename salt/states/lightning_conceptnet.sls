{% set conceptnet5_dir = "/home/conceptnet/conceptnet5" %}
{% set lightning_conceptnet_virtualenv_dir = "/home/conceptnet/lightning_conceptnet-virtualenv" %}
{% set lightning_conceptnet_dir = "/home/conceptnet/lightning_conceptnet" %}
{% set legdb_dir = "/home/conceptnet/legdb" %}
{% set pynndb2_dir = "/home/conceptnet/pynndb2" %}
{% set python_version = "3.7.8" %}

{{ lightning_conceptnet_virtualenv_dir }}:
  virtualenv.managed:
    - venv_bin: /usr/local/pyenv/versions/{{ python_version }}/bin/virtualenv
    - python: /usr/local/pyenv/versions/{{ python_version }}/bin/python3
    - require:
      - pyenv: python-{{ python_version }}
      - pip: virtualenv

lightning-conceptnet-repo:
  git.latest:
    - name: https://github.com/ldtoolkit/lightning-conceptnet.git
    - user: conceptnet
    - target: {{ lightning_conceptnet_dir }}
    - require:
      - user: conceptnet

lightning-conceptnet-package:
  pip.installed:
    - name: {{ lightning_conceptnet_dir }}
    - bin_env: {{ lightning_conceptnet_virtualenv_dir }}
    - require:
      - virtualenv: {{ lightning_conceptnet_virtualenv_dir }}

legdb-repo:
  git.latest:
    - name: https://github.com/ldtoolkit/legdb.git
    - user: conceptnet
    - target: {{ legdb_dir }}
    - require:
      - user: conceptnet

legdb-package:
  pip.installed:
    - name: {{ legdb_dir }}
    - bin_env: {{ lightning_conceptnet_virtualenv_dir }}
    - require:
      - virtualenv: {{ lightning_conceptnet_virtualenv_dir }}

pynndb2-repo:
  git.latest:
    - name: https://gitlab.com/oddjobz/pynndb2.git
    - user: conceptnet
    - target: {{ pynndb2_dir }}
    - require:
      - user: conceptnet

pipenv:
  pip.installed:
    - bin_env: {{ lightning_conceptnet_virtualenv_dir }}
    - require:
      - virtualenv: {{ lightning_conceptnet_virtualenv_dir }}

pynndb2-package:
  pip.installed:
    - name: {{ pynndb2_dir }}
    - bin_env: {{ lightning_conceptnet_virtualenv_dir }}
    - require:
      - virtualenv: {{ lightning_conceptnet_virtualenv_dir }}
      - pip: pipenv

lightning-conceptnet-benchmark:
  pip.installed:
    - requirements: salt://requirements/lightning_conceptnet_benchmark.txt
    - bin_env: {{ lightning_conceptnet_virtualenv_dir }}
    - require:
      - pip: lightning-conceptnet-package
      - pip: legdb-package
      - pip: pynndb2-package

lightning-conceptnet-system-requirements:
  pip.installed:
    - requirements: salt://requirements/system_requirements.txt
    - bin_env: {{ lightning_conceptnet_virtualenv_dir }}
    - require:
      - virtualenv: {{ lightning_conceptnet_virtualenv_dir }}
