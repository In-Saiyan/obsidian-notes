# 1	Cluster
A cluster is a set of resources that makes up a Kubernetes system.
It comprises of:
- **Control Plane** — manages the cluster
- **Data Plane** — runs user workloads

![](attachments/Pasted%20image%2020250617043830.png)

### 1.1.1	Control Plane
This is where all the system components run. It is responsible for making global decisions about the cluster (e.g. scheduling), as well as detecting and responding to cluster events.

### 1.1.2	Data Plane
This is where end-user applications run. Each node in the data plane runs a `kubelet` and a container runtime.

We can also make just one node which acts as both — the data and the control plane — but in practice they are separated in most production systems.

> [!TIP]
> Managed Kubernetes offerings (EKS, AKS, GKE) abstract away the control plane entirely.

# 2	Kubernetes System Architecture

![](attachments/Pasted%20image%2020250617044041.png)


## 2.1	On the Control Plane

### 2.1.1	Cloud Controller Manager (C-C-M)
Interface between kubernetes and cloud provider.

### 2.1.2	Controller Manager (C-M)
Runs all the various controllers that regulate the state of the cluster.  
Examples: Node Controller, ReplicaSet Controller, Endpoints Controller.

### 2.1.3	API Server (kube-apiserver)
The central management entity and the **only** component that talks to etcd directly. All other components interact with the cluster through the API server.

### 2.1.4	etcd
A distributed key-value store that Kubernetes uses to persist all cluster state — resource definitions, configuration, secrets, etc. It provides strong consistency guarantees via the Raft consensus algorithm.

### 2.1.5	Scheduler
Assigns pods to nodes based on resource requests, affinity/anti-affinity rules, taints & tolerations, and current node utilisation.

## 2.2	On the Data Plane

### 2.2.1	Kubelet
Primary node agent. Responsible for:
- Registering the node with the API server
- Spawning and managing containers via the CRI
- Performing liveness, readiness, and startup probes
- Reporting node and pod status back to the control plane

### 2.2.2	Kube-proxy
Maintains network rules on each node. It programmes `iptables` (or IPVS) rules so that Services can route traffic to the correct pods.

> **Note:** Some CNIs like Cilium replace kube-proxy entirely by programming eBPF at the kernel level.

# 3	Kubernetes Standard Interfaces
These are used to handle runtime, networking, and storage. They make the system modular by allowing different implementations to be swapped in without changing Kubernetes itself.

| Interface | Purpose |
|---|---|
| **CRI** — Container Runtime Interface | Execute containers |
| **CNI** — Container Network Interface | Set up pod networking |
| **CSI** — Container Storage Interface | Provision persistent storage |

These are separated from the core Kubernetes codebase so that each interface is pluggable and independently versioned.

### 3.1.1	Container Runtime Interfaces (CRIs)

Is the standard interface that kubernetes uses to execute and run container processes within the system.

Popular CRIs:
- Containerd
- cri-o

> In earlier versions, docker was used as a CRI but was later deprecated since its interface is a bit different than that of the standard implementation of an actual CRI. Hence, docker-shim was used instead but in Kubernetes 1.20 docker-shim was removed.

### 3.1.2	Container Network Interface (CNIs)
Defines how networking should be set up for the containers.

Ex: Calico, Flannel, Cilium.
Amazon, Microsoft(Azure) and Google have their service-specific CNIs.

> Not all of these use kube-proxy. For example, Cilium uses **eBPF** and manages networking at the kernel layer instead of the user-space/iptables layer.

### 3.1.3	Container Storage Interfaces (CSIs)
Used to provide durable, persistent storage to workloads running in Kubernetes. These drivers can communicate with cloud providers to leverage their underlying block-storage implementations.

These can also be used to provide information or configuration to a container at runtime. For ex: cert-manager can load a certificate at runtime, Secret Store CSI driver can load env variables into the file system at runtime as well.

Ex:
- Amazon EBS
- Compute Engine persistent disk
- Azure disk container
- Cert Manager
- Secret Store 

# 4	Namespaces
Namespaces provide a mechanism to **logically group and isolate** resources within a cluster. They are useful for multi-team or multi-environment setups.

There are 4 initial namespaces created by Kubernetes:
1. **default** — where resources land if no namespace is specified
2. **kube-node-lease** — holds Lease objects for node heartbeats
3. **kube-system** — reserved for system-level components
4. **kube-public** — readable by all users, typically used for cluster info

![](attachments/Pasted%20image%2020250622021228.png)

`Namespace.yaml`
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: non-default
```

**Common namespace commands:**
```bash
# Create a namespace imperatively
kubectl create namespace my-namespace

# Create from YAML
kubectl apply -f Namespace.yaml

# List all namespaces
kubectl get namespaces

# Delete a namespace (removes ALL resources inside it)
kubectl delete namespace my-namespace
kubectl delete -f Namespace.yaml
```

---

# 5	Core Workload Resources

## 5.1	Pod
Smallest deployable unit. A pod encapsulates one or more containers that share networking and storage.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx
      image: nginx:1.27
      ports:
        - containerPort: 80
```

## 5.2	Deployment
Manages a **ReplicaSet** and provides declarative updates for Pods — rolling updates, rollbacks, and scaling.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - containerPort: 80
```

## 5.3	Service
Provides a **stable network endpoint** for accessing a set of pods.

| Type | Description |
|---|---|
| **ClusterIP** | Reachable only within the cluster (default) |
| **NodePort** | Exposed on each node's IP at a static port |
| **LoadBalancer** | Provisions an external load balancer (cloud) |
| **ExternalName** | Maps to an external DNS name |

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
```

## 5.4	ConfigMap & Secret

**ConfigMap** — injects non-sensitive configuration into pods.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "debug"
  DATABASE_HOST: "db.example.com"
```

**Secret** — stores sensitive data (base64-encoded at rest by default).

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  username: YWRtaW4=
  password: cGFzc3dvcmQ=
```

---

# 6	Health Probes

Kubernetes uses probes to determine container health:

| Probe | Purpose | Failure action |
|---|---|---|
| **Liveness** | Is the container alive? | Restart the container |
| **Readiness** | Is it ready to serve traffic? | Remove from Service endpoints |
| **Startup** | Has it finished initialising? | Kill & restart (protects slow starters) |

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  periodSeconds: 5
```

---

# 7	Resource Management

```yaml
resources:
  requests:
    cpu: "250m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

- **Requests** — guaranteed minimum; used by the scheduler for placement.
- **Limits** — hard ceiling; container is throttled (CPU) or OOM-killed (memory) if exceeded.