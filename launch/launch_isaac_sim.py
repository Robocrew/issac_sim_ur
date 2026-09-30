#!/home/faps/env_isaacsim/bin/python

from pathlib import Path

from isaacsim import SimulationApp


simulation_app = SimulationApp({"headless": False})

import carb
import omni.usd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
URDF_ROOT = PROJECT_ROOT / "urdf"
COMBINED_STAGE = URDF_ROOT / "main_ws" / "configuration" / "ur_ws.usd"


def get_stage_path() -> Path:
    if not COMBINED_STAGE.exists():
        raise FileNotFoundError(f"Expected combined USD not found: {COMBINED_STAGE}")
    return COMBINED_STAGE


def wait_for_stage_load(app: SimulationApp, timeout_frames: int = 600) -> None:
    context = omni.usd.get_context()
    for frame in range(timeout_frames):
        loading, total = context.get_stage_loading_status()
        if total == 0:
            break
        app.update()

    else:
        carb.log_warn(
            "Stage did not finish loading within the timeout; "
            "assets may still be resolving."
        )


def main() -> None:
    combined_stage = get_stage_path()
    print(f"Opening USD stage: {combined_stage}", flush=True)

    simulation_app.update()
    context = omni.usd.get_context()
    print("Loading saved USD stage...", flush=True)
    result = context.open_stage(str(combined_stage))
    if not result:
        raise RuntimeError(f"Failed to open stage: {combined_stage}")

    print("Simulation started. Close the window or press Ctrl+C to stop.", flush=True)
    try:
        while simulation_app.is_running():
            simulation_app.update()
    except KeyboardInterrupt:
        print("Interrupted by user.")


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()
