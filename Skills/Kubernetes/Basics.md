# 1	Cluster
A cluster is a set of resources that makes up a kubernetes system.
It comprises of:
- Control Plane
- Data Plane

![[Pasted image 20250617043830.png]]

### 1.1.1	Control Plane
This is where all the system components run.

### 1.1.2	Data Plane
This is where end-user applications run.

We can also make just one node which acts as both - the data and the control plain, but in practice they are used separately in most production systems.

# 2	Kubernetes System Architecture

![[Pasted image 20250617044041.png]]


## 2.1	On the Control Plane

### 2.1.1	Cloud Controller Manager (C-C-M)
Interface between kubernetes and cloud provider.

### 2.1.2	Controller Manager (C-M)
This runs all the various controller that regulate the state of the cluster.

### 2.1.3	API
API for interacting with the kubernetes cluster.

### 2.1.4	etc-d
This is the data store that kubernetes uses to manage all the resources that are deployed on it. It also ensures data consistency.

### 2.1.5	Scheduler 
It assigns pods/containers to new nodes based on their current usage.

## 2.2	On the Data Plane

### 2.2.1	Kubelet
It is the component responsible to spawn and manage the workloads, it also performs health checking and relays that information back to the API server on the control plane.

### 2.2.2	Kube-proxy
Is responsible for setting up and maintaining the network between different workloads. It sets up the rules within the IP table to ensure that the workload can communicate according to the config.

# 3	Kubernetes Standard Interfaces
These are used to handle things like runtime, network and storage. This makes the system more modular and allow using different implementation of any of the interfaces according to the need.

Ex:
- Container Runtime Interface (CRI)
- Container Networking Interface (CNI)
- Container Storage Interface (CSI)

These are separated from main implementation of Kubernetes so that we can have a 'pluggable' interface which is independent of rest of the project.

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

> Not all of these use kube-proxy, for example Cilium uses EPPF, it manages networking at kernel layer instead of the Data layer.

### 3.1.3	Control Storage Interfaces (CSIs)
They are used to provide durable, persistent storage to a workload running in kubernetes.
These drivers also can(often) communicate to cloud provider to use their underlying block storage implementations which are cloud-service specific.



