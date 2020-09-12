{% set python_version = "3.7.9" %}

pyenv_deps:
  pkg.installed:
    - pkgs:
      - make
      - build-essential
      - libssl-dev
      - zlib1g-dev
      - libbz2-dev
      - libreadline-dev
      - libsqlite3-dev
      - wget
      - curl
      - llvm
      - libncurses5-dev
      - libncursesw5-dev
      - xz-utils
      - tk-dev
      - libffi-dev
      - liblzma-dev
      - python-openssl

python-{{ python_version }}:
  pyenv.installed:
    - default: True
    - require:
      - pkg: pyenv_deps

# A workaround for using pip state
python3-pip:
  pkg.installed

virtualenv:
  pip.installed:
    - bin_env: /usr/local/pyenv/versions/{{ python_version }}/bin/pip3
    - require:
      - pyenv: python-{{ python_version }}
      - pkg: python3-pip
