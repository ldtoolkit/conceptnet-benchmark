postgres:
  version: 12
#  acls:
#  - ['local', 'conceptnet5', 'all', 'trust']
  users:
    conceptnet:
      ensure: present
      createdb: true
  databases:
    conceptnet5:
      owner: conceptnet
