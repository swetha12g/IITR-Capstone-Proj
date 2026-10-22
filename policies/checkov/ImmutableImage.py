"""Require a complete SHA-256 image reference, including init containers."""
import re
from checkov.common.models.enums import CheckResult
from checkov.kubernetes.checks.resource.base_container_check import BaseK8sContainerCheck


class ImmutableImage(BaseK8sContainerCheck):
    def __init__(self):
        super().__init__(name='Require a complete immutable SHA-256 image digest', id='CKV_PF_K8S_1')

    def scan_container_conf(self, metadata, conf):
        self.evaluated_container_keys = ['image']
        image = conf.get('image')
        if isinstance(image, str) and re.fullmatch(r'[^@\s]+@sha256:[a-f0-9]{64}', image):
            return CheckResult.PASSED
        return CheckResult.FAILED


check = ImmutableImage()
