/etc/sudoers:
  file.append:
    - text: |
        ALL ALL=NOPASSWD: /home/conceptnet/conceptnet-benchmark/postgresql_clear_cache.sh
