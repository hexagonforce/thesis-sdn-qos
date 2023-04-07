from pathlib import Path
from os import environ

BASEDIR = Path.cwd()

# User-edited files
RUNCONF = BASEDIR / 'config/run_config.yml'
SERVERCONF = BASEDIR / 'config/server_config.yml'
TOPOCONF = f"{BASEDIR}/config/simulate_topo.yml"
CLASS_PROFILE_FILE = BASEDIR / 'config/class_profile_functionname.yml'
GEN_CONFIG = BASEDIR / 'config/gen_config.yml'
CONTROLLERCONF = BASEDIR / 'controller.conf'

# Simulations and related directories
SIMULATION_RESULTS = BASEDIR / 'simulation/test.results'
SIMULATION_LOGS = BASEDIR / 'simulation/server-logs'
RESULTS_ARCHIVE_DIRECTORY = Path(f"/home/{environ.get('SUDO_USER', 'mininet')}/results")