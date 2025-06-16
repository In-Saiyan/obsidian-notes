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
Is responsible for setting up and maintaining the network between different workloads