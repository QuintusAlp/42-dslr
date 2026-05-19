import shutil
from pathlib import Path

def main():
    project_root = Path(__file__).parent.parent.parent
    plots_dir = project_root / "srcs" / "v2_data_visualization" / "plots"
    houses_file = project_root / "houses.csv"

    if plots_dir.exists():
        shutil.rmtree(plots_dir)
        print(f"✓ Removed {plots_dir}/ directory")
    else:
        print(f"✓ {plots_dir}/ directory doesn't exist")

    if houses_file.exists():
        houses_file.unlink()
        print(f"✓ Removed {houses_file}")
    else:
        print(f"✓ {houses_file} doesn't exist")
        