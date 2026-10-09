#!/home/faps/env_isaacsim/bin/python

from pathlib import Path

from isaacsim import SimulationApp


simulation_app = SimulationApp({"headless": False})

from isaacsim.core.utils.extensions import enable_extension

enable_extension("isaacsim.ros2.bridge")

import omni.timeline
import omni.usd


ASSET_ROOT = Path(__file__).resolve().parents[1]
COMBINED_STAGE = ASSET_ROOT / "main_ws" / "configuration" / "ur_ws.usd"


def get_stage_path() -> Path:
    if not COMBINED_STAGE.exists():
        raise FileNotFoundError(f"Expected combined USD not found: {COMBINED_STAGE}")
    return COMBINED_STAGE


def main() -> None:
    combined_stage = get_stage_path()
    print(f"Opening USD stage: {combined_stage}", flush=True)

    simulation_app.update()
    context = omni.usd.get_context()
    print("Loading saved USD stage...", flush=True)
    result = context.open_stage(str(combined_stage))
    if not result:
        raise RuntimeError(f"Failed to open stage: {combined_stage}")

    omni.timeline.get_timeline_interface().play()

    print("Simulation started. Close the window or press Ctrl+C to stop.", flush=True)
    try:
        while simulation_app.app.is_running():
            simulation_app.update()
    except KeyboardInterrupt:
        print("Interrupted by user.")


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()
