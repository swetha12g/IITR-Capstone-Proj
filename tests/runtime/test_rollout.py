"""Readiness must follow live image-bound pods, not retiring replicas."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "runtime_baseline", Path(__file__).resolve().parents[2] / "scripts/runtime-baseline.py")
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)
IMAGE = "sha256:" + "1" * 64


def pod(ready=True, image=IMAGE, retiring=False):
    result = {"metadata": {"annotations": {"pipelinefortress/image-config-id": image}},
              "status": {"conditions": [{"type": "Ready", "status": "True" if ready else "False"}]}}
    if retiring:
        result["metadata"]["deletionTimestamp"] = "2026-10-18T08:22:56Z"
    return result


class RolloutReadiness(unittest.TestCase):
    def test_retiring_unready_replica_does_not_block_current_ready_pod(self):
        current = pod()
        self.assertEqual(runtime.current_ready_pods([pod(False, image="old", retiring=True), current], IMAGE), [current])

    def test_unready_live_replica_blocks(self):
        with self.assertRaisesRegex(ValueError, "not Ready"):
            runtime.current_ready_pods([pod(False)], IMAGE)

    def test_wrong_live_image_blocks(self):
        with self.assertRaisesRegex(ValueError, "expected image"):
            runtime.current_ready_pods([pod(image="old")], IMAGE)

    def test_only_retiring_replicas_cannot_pass(self):
        with self.assertRaisesRegex(ValueError, "No live"):
            runtime.current_ready_pods([pod(retiring=True)], IMAGE)

    def test_no_live_pods_cannot_pass(self):
        with self.assertRaisesRegex(ValueError, "No live"):
            runtime.current_ready_pods([], IMAGE)
