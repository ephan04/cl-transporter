from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).parent.parent

def load_config(): 
    path = PROJECT_ROOT/"config.yaml"
    with open(path) as f:
        return yaml.safe_load(f)

def get_paths(cfg): 
    data_dir = PROJECT_ROOT/cfg["paths"]["data_dir"]
    return{
        "train": data_dir/cfg["data"]["train_file"],
        "test": data_dir/cfg["data"]["test_file"],
        "results": PROJECT_ROOT/cfg["paths"]["results_dir"]

    }
CFG   = load_config()
PATHS = get_paths(CFG)