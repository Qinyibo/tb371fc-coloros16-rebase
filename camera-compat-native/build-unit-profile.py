"""Build the standard two-camera profile for the TB371FC CameraUnit SDK."""
import hashlib
import json
from pathlib import Path
import re

CAMERA = Path(__file__).resolve().parent
SOURCE = CAMERA / "config-donor/camera_unit_config"
EVIDENCE = CAMERA / "candidate-feature/runtime-zui/zui-switched-lens-later.txt"
DONOR_SHA = "87842d4d03f2d5f1c7db9307271f449f9aee1033dcfd6582c1055b9f18344c29"
REAR = "rear_main"
FRONT = "front_main"

source = SOURCE.read_bytes()
assert hashlib.sha256(source).hexdigest() == DONOR_SHA
donor = json.loads(source)
assert donor["device_info"] == {"platform": "qcom"}

dump = EVIDENCE.read_text(encoding="utf-8")
devices = re.split(r"== Camera HAL device device@3\.5/legacy/([01]) \(v3\.5\) static information: ==", dump)
assert len(devices) == 5
sensors = {}
supported = {"1920X1080", "1280X720"}
for camera_id, metadata in zip(devices[1::2], devices[2::2]):
    facing = re.search(r"Facing: (Back|Front)", metadata).group(1)
    orientation = int(re.search(r"Orientation: (\d+)", metadata).group(1))
    configs = re.search(r"android\.scaler\.availableStreamConfigurations [^\n]+\n(.*?)(?=\n\s*android\.)", metadata, re.S).group(1)
    formats = {(int(fmt), f"{width}X{height}") for fmt, width, height in re.findall(r"\[(\d+) (\d+) (\d+) OUTPUT\s*\]", configs)}
    assert supported <= {size for fmt, size in formats if fmt == 34}
    assert any(fmt == 33 for fmt, _ in formats)
    sensors[camera_id] = {"facing": facing, "orientation": orientation}
assert sensors == {"0": {"facing": "Back", "orientation": 90}, "1": {"facing": "Front", "orientation": 270}}
assert "com.oplus.supported.cameraid.type" not in dump
for name in ("zui-first-lens.txt", "zui-switched-lens-later.txt"):
    assert "Operation mode: NORMAL (0)" in (EVIDENCE.parent / name).read_text(encoding="utf-8")

# Mode 0 uses the ordinary Camera2 session path verified on both TB cameras.
modes = ["photo_mode", "video_mode"]
assert all(mode in donor["mode_type_list"][camera] for camera in (REAR, FRONT) for mode in modes)
usecases = ("single_photo_case", "front_single_photo_case", "recorder_video_case",
            "video_recorder_snapshot_case", "preview_frame_case", "simple_preview_case", "simple_photo_case")
sizes = [size for size in donor["support_default_preview_sizes"] if size in supported]
assert set(sizes) == supported
profile = {
    "camera_id_list": list(sensors),
    "main_info": donor["main_info"],
    "device_info": donor["device_info"],
    "mode_type_list": {camera: modes for camera in (REAR, FRONT)},
    "mode_operation_mode": {mode: "0" for mode in modes},
    "usecase_info": {name: donor["usecase_info"][name] for name in usecases},
    "support_default_preview_sizes": sizes,
    "support_default_video_sizes": sizes,
    "mode_type_feature_max_video_size": {
        "video_mode": {camera: {"default": [sizes[0], sizes[0]]} for camera in (REAR, FRONT)}
    },
    "vendor_tag_type_values": {"com.oplus.third.cameraunit.support": "0"},
}
assert not (set(profile) - set(donor))
out = CAMERA / "tb-camera-unit"
out.mkdir(exist_ok=True)
target = out / "camera_unit_config"
target.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
(out / "profile.json").write_text(json.dumps({
    "source_sha256": DONOR_SHA,
    "profile_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    "physical_metadata": str(EVIDENCE.relative_to(CAMERA)),
    "sensors": sensors,
    "standard_stream_sizes": sizes,
    "sdk_needs_camera_type_mapping_from_standard_metadata": True,
    "coloros_runtime_verified": False,
}, indent=2) + "\n", encoding="utf-8")
print("TB_CAMERA_UNIT_PROFILE_GENERATED_AND_METADATA_CHECKED", target)
