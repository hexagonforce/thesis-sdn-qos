from pathlib import Path
from os import environ

BASEDIR = Path.cwd()

# User-edited files
SERVERCONF = BASEDIR / 'config/server_config.yml'
TOPOCONF = f"{BASEDIR}/config/simulate_topo.yml"
CLASS_PROFILE_FILE = BASEDIR / 'config/class_profile_functionname.yml'
CONFIG_METADATA = BASEDIR / 'config/config_metadata.yml'
CONTROLLERCONF = BASEDIR / 'controller.conf'

# Simulations and related directories
SIMULATION_RESULTS = BASEDIR / 'simulation/test.results'
SIMULATION_LOGS = BASEDIR / 'simulation/server-logs'
RESULTS_ARCHIVE_DIRECTORY = Path(f"/home/{environ.get('SUDO_USER', 'mininet')}/results")

