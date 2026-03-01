# Kubernetes Practical — Test Cases & Exercises

A set of hands-on exercises to validate your understanding of core Kubernetes concepts.

- [[#1 Cluster & Node Verification]]
- [[#2 Namespace Operations]]
- [[#3 Pod Lifecycle]]
- [[#4 Deployment Management]]
- [[#5 Service Networking]]
- [[#6 ConfigMap & Secret Injection]]
- [[#7 Health Probes]]
- [[#8 Resource Limits & QoS]]
- [[#9 Rolling Updates & Rollbacks]]
- [[#10 Debugging & Troubleshooting]]

---

## 1 Cluster & Node Verification

| # | Test Case | Command / Action | Expected Result |
|---|---|---|---|
| 1.1 | Check cluster info | `kubectl cluster-info` | Displays control plane endpoint URL |
| 1.2 | List all nodes | `kubectl get nodes` | All nodes show `Ready` status |
| 1.3 | Describe a node | `kubectl describe node <name>` | Shows capacity, allocatable, conditions, pods |
| 1.4 | Check component status | `kubectl get componentstatuses` | scheduler, controller-manager, etcd show `Healthy` |

---

## 2 Namespace Operations

| # | Test Case | Command / Action | Expected Result |
|---|---|---|---|
| 2.1 | Create namespace imperatively | `kubectl create namespace test-ns` | Namespace created |
| 2.2 | Create namespace declaratively | `kubectl apply -f namespace.yaml` | Namespace created |
| 2.3 | List namespaces | `kubectl get ns` | Shows default + system + custom namespaces |
| 2.4 | Deploy pod into custom namespace | `kubectl run nginx --image=nginx -n test-ns` | Pod running in `test-ns` |
| 2.5 | Verify isolation | `kubectl get pods` (no `-n` flag) | Pod is **not** visible in default namespace |
| 2.6 | Delete namespace cascades | `kubectl delete ns test-ns` | Namespace and all its resources removed |

---

## 3 Pod Lifecycle

| # | Test Case | Command / Action | Expected Result |
|---|---|---|---|
| 3.1 | Create a simple pod | `kubectl run nginx --image=nginx:1.27` | Pod enters `Running` state |
| 3.2 | Check pod logs | `kubectl logs nginx` | nginx startup logs visible |
| 3.3 | Exec into a pod | `kubectl exec -it nginx -- /bin/sh` | Interactive shell opens |
| 3.4 | Port-forward to pod | `kubectl port-forward pod/nginx 8080:80` | `curl localhost:8080` returns nginx welcome page |
| 3.5 | Pod with invalid image | `kubectl run bad --image=nonexistent:v1` | Pod stays in `ErrImagePull` / `ImagePullBackOff` |
| 3.6 | Delete pod | `kubectl delete pod nginx` | Pod terminated and removed |
| 3.7 | Multi-container pod | Apply pod with 2 containers | Both containers running, share localhost |

**Multi-container pod YAML:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container
spec:
  containers:
    - name: app
      image: nginx:1.27
      ports:
        - containerPort: 80
    - name: sidecar
      image: busybox
      command: ["sh", "-c", "while true; do wget -qO- http://localhost:80 > /dev/null; sleep 5; done"]
```

---

## 4 Deployment Management

| # | Test Case | Command / Action | Expected Result |
|---|---|---|---|
| 4.1 | Create deployment | `kubectl create deployment nginx --image=nginx:1.27 --replicas=3` | 3 pods running |
| 4.2 | Scale up | `kubectl scale deployment nginx --replicas=5` | 5 pods running |
| 4.3 | Scale down | `kubectl scale deployment nginx --replicas=2` | 2 pods running, 3 terminated |
| 4.4 | Delete a pod | `kubectl delete pod <one-of-the-pods>` | ReplicaSet recreates it; count stays at 2 |
| 4.5 | Zero-downtime deploy | Update image → watch pods | Old pods terminated only after new ones are `Ready` |
| 4.6 | Check rollout status | `kubectl rollout status deployment/nginx` | Reports "successfully rolled out" |
| 4.7 | Rollout history | `kubectl rollout history deployment/nginx` | Shows revision list |

---

## 5 Service Networking

| # | Test Case | Command / Action | Expected Result |
|---|---|---|---|
| 5.1 | Create ClusterIP service | `kubectl expose deployment nginx --port=80` | Service created, ClusterIP assigned |
| 5.2 | DNS resolution inside cluster | Exec into a pod, `nslookup nginx` | Resolves to ClusterIP |
| 5.3 | Create NodePort service | `kubectl expose deployment nginx --port=80 --type=NodePort` | Accessible on `<NodeIP>:<NodePort>` |
| 5.4 | Verify endpoints | `kubectl get endpoints nginx` | Lists IPs of backing pods |
| 5.5 | Scale to 0, check endpoints | `kubectl scale deployment nginx --replicas=0` | Endpoints list is empty |
| 5.6 | Service with wrong selector | Apply service with mismatched label | No endpoints; traffic blackholes |

---

## 6 ConfigMap & Secret Injection

| # | Test Case | Command / Action | Expected Result |
|---|---|---|---|
| 6.1 | Create ConfigMap | `kubectl create configmap app-cfg --from-literal=LOG=debug` | ConfigMap created |
| 6.2 | Inject as env var | Mount ConfigMap key as env var in pod | `echo $LOG` prints `debug` |
| 6.3 | Inject as volume | Mount ConfigMap as volume | File exists at mount path with correct content |
| 6.4 | Create Secret | `kubectl create secret generic db-cred --from-literal=pass=s3cret` | Secret created |
| 6.5 | Secret visible in env | Mount secret key as env var | `echo $pass` prints `s3cret` |
| 6.6 | Verify base64 encoding | `kubectl get secret db-cred -o yaml` | `pass` value is base64-encoded |

**ConfigMap volume mount example:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: config-test
spec:
  containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "cat /etc/config/LOG && sleep 3600"]
      volumeMounts:
        - name: config-vol
          mountPath: /etc/config
  volumes:
    - name: config-vol
      configMap:
        name: app-cfg
```

---

## 7 Health Probes

| # | Test Case | Command / Action | Expected Result |
|---|---|---|---|
| 7.1 | Liveness probe (happy path) | Deploy pod with liveness HTTP probe on `/healthz` | Pod stays `Running` |
| 7.2 | Liveness probe failure | Probe endpoint returns 500 | Pod is restarted (restart count increments) |
| 7.3 | Readiness probe failure | Probe endpoint returns 503 | Pod marked `NotReady`; removed from Service endpoints |
| 7.4 | Startup probe slow app | Set `failureThreshold * periodSeconds > start time` | Pod starts successfully without liveness killing it |
| 7.5 | Exec probe | `exec` probe runs `cat /tmp/healthy` | Pod healthy when file exists, restarted when deleted |

**Liveness + Readiness example:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: probe-test
spec:
  containers:
    - name: app
      image: registry.k8s.io/e2e-test-images/agnhost:2.40
      args: ["liveness"]
      livenessProbe:
        httpGet:
          path: /healthz
          port: 8080
        initialDelaySeconds: 3
        periodSeconds: 5
      readinessProbe:
        httpGet:
          path: /healthz
          port: 8080
        periodSeconds: 5
```

---

## 8 Resource Limits & QoS

| # | Test Case | Command / Action | Expected Result |
|---|---|---|---|
| 8.1 | Pod with requests & limits | Set `requests.cpu: 250m`, `limits.cpu: 500m` | Pod scheduled on node with ≥ 250m free |
| 8.2 | Exceed memory limit | Container tries to allocate beyond limit | Container is OOM-killed, pod shows `OOMKilled` |
| 8.3 | Exceed CPU limit | Container spins CPU | CPU is throttled, not killed |
| 8.4 | QoS class Guaranteed | `requests == limits` for all containers | `kubectl describe pod` shows QoS: Guaranteed |
| 8.5 | QoS class Burstable | Only `requests` set (no limits) | QoS: Burstable |
| 8.6 | QoS class BestEffort | No requests or limits | QoS: BestEffort (first to be evicted) |

---

## 9 Rolling Updates & Rollbacks

| # | Test Case | Command / Action | Expected Result |
|---|---|---|---|
| 9.1 | Update image | `kubectl set image deployment/nginx nginx=nginx:1.28` | Pods are gradually replaced |
| 9.2 | Monitor rollout | `kubectl rollout status deployment/nginx` | Reports progress until complete |
| 9.3 | Rollback to previous | `kubectl rollout undo deployment/nginx` | Reverts to previous revision |
| 9.4 | Rollback to specific revision | `kubectl rollout undo deployment/nginx --to-revision=1` | Reverts to revision 1 |
| 9.5 | Pause / Resume | `kubectl rollout pause deployment/nginx` | Rollout pauses mid-way; resume continues |
| 9.6 | Bad image rollout | Update to non-existent tag | New pods stuck in `ImagePullBackOff`; old pods stay running |

---

## 10 Debugging & Troubleshooting

| # | Test Case | Command / Action | Expected Result |
|---|---|---|---|
| 10.1 | Describe failing pod | `kubectl describe pod <name>` | Events section shows reason for failure |
| 10.2 | Check pod events | `kubectl get events --sort-by=.metadata.creationTimestamp` | Lists recent cluster events |
| 10.3 | CrashLoopBackOff diagnosis | `kubectl logs <pod> --previous` | Shows logs from the crashed container |
| 10.4 | DNS debugging | `kubectl run dnsutil --image=registry.k8s.io/e2e-test-images/agnhost:2.40 -- nslookup kubernetes` | Resolves `kubernetes.default.svc.cluster.local` |
| 10.5 | Ephemeral debug container | `kubectl debug -it <pod> --image=busybox` | Attaches debug container to running pod |
| 10.6 | Node not ready | Cordon a node → check pod scheduling | New pods avoid cordoned node |

---

## Quick Reference — Common `kubectl` Commands

```bash
# Context & cluster
kubectl config get-contexts
kubectl config use-context <name>

# Resources (generic)
kubectl get <resource> -o wide
kubectl describe <resource> <name>
kubectl delete <resource> <name>
kubectl apply -f <file.yaml>

# Logs & exec
kubectl logs <pod> -c <container> -f --tail=100
kubectl exec -it <pod> -- /bin/sh

# Scaling
kubectl scale deployment <name> --replicas=<n>
kubectl autoscale deployment <name> --min=2 --max=10 --cpu-percent=80

# Debugging
kubectl get events --sort-by='.lastTimestamp'
kubectl top nodes
kubectl top pods
```