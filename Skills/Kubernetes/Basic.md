## 0.1	Cluster
A cluster is a set of resources that makes up a kubernetes system.
It comprises of:
- Control Plane
- Data Plane

![[Pasted image 20250617043830.png]]

### 0.1.1	Control Plane
This is where all the system components run.

### 0.1.2	Data Plane
This is where end-user applications run.

We can also make just one node which acts as both - the data and the control plain, but in practice they are used separately in most production systems.

## 0.2	Kubernetes System Architecture

![[Pasted image 20250617044041.png]]


