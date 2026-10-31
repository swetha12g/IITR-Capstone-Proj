# Day 4 control mapping and limits — 22 October 2026

Selected reference: **CIS Kubernetes Benchmark 2.0.0**, using the inspectable [kube-bench CIS 2.0 policy definitions](https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-2.0/policies.yaml) for section/control numbering. The [CIS catalog](https://www.cisecurity.org/benchmark/kubernetes) now lists 2.1.0; this is a bounded 2.0.0 mapping, not a claim of current full-benchmark compliance or Kubernetes 1.37 certification. These are workload checks in one owned kind lab. kube-bench/CIS-CAT and a complete cluster audit were not run.

| CIS 2.0.0 reference | Workload implementation / Checkov evidence | Remaining boundary |
|---|---|---|
| 5.1.5–5.1.6, service-account exposure | Dedicated account; pod and account disable token mounting; CKV_K8S_38 passes; token absent in running container | Default accounts and RBAC across other namespaces not audited |
| 5.2.2–5.2.5, privileged/host namespace access | Workload uses neither privileged mode nor host PID/IPC/network; built-in checks pass | No cluster-wide admission enforcement claimed |
| 5.2.6, privilege escalation | `allowPrivilegeEscalation: false`; CKV_K8S_20 passes; process `NoNewPrivs=1` | Namespace admission is audit/warn only |
| 5.2.7, root identity | UID/GID 65532, `runAsNonRoot`; CKV_K8S_23/40 pass; runtime identity checked | Other workloads are outside the assertion |
| 5.2.8–5.2.9, capabilities | Drop ALL; CKV_K8S_28/37 pass; effective and bounding capability sets are zero | No application capability exception is needed |
| 5.2.11–5.2.12, host filesystem/ports | Only bounded `emptyDir` mounts; no hostPath or hostPort; built-in checks pass | Host and kind node container privileges are outside workload scope |
| 5.3.1–5.3.2, traffic isolation | **Gap:** no NetworkPolicy defined; CKV2_K8S_6 still fails | CNI enforcement not tested; no isolation is claimed by adding an untested policy |
| 5.6.1, namespace boundaries | Dedicated namespace and ClusterIP service | Namespace naming alone does not restrict network traffic or RBAC |
| 5.6.2, seccomp | RuntimeDefault; CKV_K8S_31 passes; process reports seccomp filtering | No custom syscall profile or full exploit containment claim |

Additional project controls: strict digest syntax (`CKV_PF_K8S_1`), resource requests/limits, startup/readiness/liveness probes, read-only image filesystem, production-only root dependencies, no shell/npm in runtime, and pinned builder/runtime bases. These complement the mapping; they are not invented CIS control IDs. [Checkov policy index](https://www.checkov.io/5.Policy%20Index/kubernetes.html), [Kubernetes security contexts](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/).

Writable mounts are explicit: `data` (SQLite/static seed), `ftp` (restored training files), `i18n`, `frontend/dist` (customized HTML/media/uploads), `uploads`, `logs`, `.well-known` (generated CSAF metadata), and `/tmp`. The immutable seed and application code reject writes. Empty directories are seeded as the non-root process starts. State is ephemeral and may reset when a pod is replaced; this is the existing training-lab lifecycle. The broad frontend mount preserves upstream customization behavior and remains a writable attack surface.

Uncovered controls include control-plane/etcd/kubelet configuration, host file permissions, TLS/audit/encryption settings, cluster-wide RBAC and admission enforcement, secret storage, image signing/provenance admission, network enforcement and Windows controls. No live provider/API credentials were configured. Source-level training weaknesses remain for later measured remediation work.
