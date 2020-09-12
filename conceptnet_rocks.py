from invoke import task
from pathlib import Path


conceptnet_rocks_virtualenv_dir = Path("/home/conceptnet/conceptnet_rocks_virtualenv")
conceptnet_rocks = conceptnet_rocks_virtualenv_dir / "bin" / "conceptnet-rocks"


@task
def install_arangodb(c):
    c.run([conceptnet_rocks, "install-arangodb"])


@task(install_arangodb)
def load_db(c):

