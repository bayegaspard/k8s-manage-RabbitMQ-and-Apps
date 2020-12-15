# Advance Total virtualization
- All files can be found in the following [github repo](https://github.com/BAYEGASPARD/k8s-manage-RabbitMQ-and-Apps), including Dockerfile, docker-compose.yml, and all related files.
### Lab Docker and K8s
- Refer to the following set-up for the lab.
![](https://i.imgur.com/8viylxB.png)
### Installing docker compose
- To install docker compose, we use the following commads on ubuntu 20:
- We run this command to download the current stabke release
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

```
- Then we run this command to apply executablke permissions to the binary.
```
sudo chmod +x /usr/local/bin/docker-compose
```
- We verify it is installed via the followiing :
```
docker-compose --version
```
![](https://i.imgur.com/97FMOmW.png)
### Create a docker file
- I will create a rabbitmq docker yaml file.
- We create a script for the message creator and message consumer using python
- see code in github [here](https://github.com/BAYEGASPARD/k8s-manage-RabbitMQ-and-Apps) asn `cons.py` and `producer.py`.
- After running the command : 
```
docker-compose up -d
```
### Buikd a docker image.
- There are two python docker files; for consumer and for producer as seen in the github page.To build and image we use the following command:
```
docker build -t <file name> .

```
### Rabbitmq
- We set up rabbit mq according to the different configuration files, definitions and docker files proposed by the official link provied.See github page for the codes.
- We have our rabbitq app running and python scripts functional as seen from the screenshot below:
![](https://i.imgur.com/3XPYrvR.png)
- After testing we can see that our rabit mq accept and queus messages as well.
![](https://i.imgur.com/Kxn2nzA.png)
- Next we check if this container is running:
![](https://i.imgur.com/2FmIzwa.png)
- we can now test our python scripts for consumer and producer.
![](https://i.imgur.com/Wp3i8Za.png)
- Now let's I decided to create 3 containers one database, one message creator and one message consumer and write to the database.Source code can be found in the github link shared above.
- Settings :
 ```
        10.0.15.10  k8s-master
        10.0.15.21  worker01 (creator app)
        10.0.15.22  worker02 (conumer + db )
        10.0.15.23  worker03 (rabbitmq )
    Root privileges
 ```
# Step 1 - Kubeadm Installation
### Setup Hosts
- We edit the virtual hosts to have the different networking for the different applications so they can communicate and the k8s master can reach  them since they need to be on the same network.
```
sudo vim /etc/hosts
```
- We have the following in the host file.
```
10.0.15.10  k8s-master
10.0.15.21  worker01
10.0.15.22  worker02
10.0.15.23  worker03
```
![](https://i.imgur.com/Yp49ojp.png)
### Install Docker
- Docker can be installed via the following : 

```
sudo apt install docker.io -y
```
- We restart it using the following : 
```
sudo systemctl start docker
sudo systemctl enable docker
```
![](https://i.imgur.com/UGFiN2o.png)
- From industry , it is good practice to disable the swap in order to set up kubernetes .
- We use the command : 
```
sudo swapon -s
sudo swapoff -a
```
```
sudo vim /etc/fstab
```
```
#/dev/mapper/hakase--labs--vg-swap_1 none            swap    sw              0       0
```
![](https://i.imgur.com/icC8Slk.png)
- We then reboot our machine to enforce the changes.
### Install Kubeadm Packages
- We will use kubeadm packages to set up a k8s cluster.We install the package from official source.
```
sudo apt install -y apt-transport-https
```
- Add gpg key for verifications: 
```
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```
![](https://i.imgur.com/PjoruRQ.png)
- We add the repository for k8s into our source file.
```
cd /etc/apt/
sudo vim sources.list.d/kubernetes.list
```
- We add this line into the source file:
```
deb http://apt.kubernetes.io/ kubernetes-xenial main
```
- Then we update and install k8s manager.
```
sudo apt update
sudo apt install -y kubeadm kubelet kubectl
```
###  Kubernetes Cluster Initialization
- We use the following command to initialize our cluster.
```
sudo kubeadm init --pod-network-cidr=10.244.10.0/16 --apiserver-advertise-address=10.0.15.10 --kubernetes-version "1.11.0"
```
- NOTE: 

-apiserver-advertise-address = determines which IP address Kubernetes should advertise its API server on.
--pod-network-cidr = specify the range of IP addresses for the pod network. We're using the 'flannel' virtual network. If you want to use another pod network such as weave-net or calico, change the range IP address.
- See reference for sources.
- We wait for sometime and check using the command:
```
kubectl get nodes
kubectl get pods --all-namespaces
```
![](https://i.imgur.com/S8nuxoT.png)
- We can add a worker to our node or cluster using the command : 
```
kubeadm join 10.0.15.10:6443 --token daync8.5dcgj6c6xc7l8hay --discovery-token-ca-cert-hash sha256:65a3e69531d323c335613dea1e498656236bba22e6cf3d5c54b21d744ef97dcd
```
- We can check our nodes as well using the command: 
```
kubectl get nodes
```
![](https://i.imgur.com/nXVAX3d.png)
- We can see that our database is recieving messages from the consumer since they are on the same virtual network.
- I created two tables, `string_tbl` and `int_tbl` which from my source code db.py  or cons.py tell which message type to insert in which table.
- For string_tbl:
![](https://i.imgur.com/aDzMQcW.png)


- For int_tbl:
![](https://i.imgur.com/tTdHPtv.png)
## More testing 
- Created an nginx yaml file to test against as well. 
- We will create a directory called nginx.
- We create a yaml called `nginx-production.yaml` and put the following configuration:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
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
        image: nginx:1.14.0
        ports:
        - containerPort: 80
```
- Note : 
    We are to create  new 'production system' named 'nginx-prodcution'.
    with app label as 'nginx' with '3' replicas.
    The 'nginx-production' will have containers named 'nginx', based on 'nginx:1.14.0' docker image, and will expose the default HTTP port 80.
- With kubectl we use the following : 
```
kubectl create -f nginx-deployment.yaml
```
- And the second command : 
```
kubectl get deployments
kubectl describe deployment nginx-deployment
```
- We create kubenetes pods using the following : 

```
kubectl get pods
kubectl describe pods nginx-deployment-6cb5f7bf4f-t5xfh
```
- We create a yaml file named service.yaml
```
vim nginx-service.yaml
```
- And put the following configurations:
```

apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  labels:
    run: nginx-service
spec:
  type: NodePort
  ports:
  - port: 80
    protocol: TCP
  selector:
    app: nginx
```
- After saving and exiting, we type the following : 
```
kubectl create -f nginx-service.yaml
```
- Then we check all available services in the cluster using the command:
```
kubectl get service
kubectl describe service nginx-service
```
![](https://i.imgur.com/GP7tzbG.png)
- Using a simple curl command, we can get the contents of the different applications as seen below.
![](https://i.imgur.com/2kFZqji.png)

### References
- https://hub.docker.com/_/rabbitmq
- https://github.com/dmaze/docker-rabbitmq-example
- https://medium.com/better-programming/introduction-to-message-queue-with-rabbitmq-python-639e397cb668
- https://habr.com/ru/post/434510/
- https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart
- https://www.postgresqltutorial.com/postgresql-insert/
- https://www.postgresqltutorial.com/postgresql-create-table/
- https://www.tutorialspoint.com/postgresql/postgresql_create_table.htm
- https://stackoverflow.com/questions/12906351/importerror-no-module-named-psycopg2#23104715
- https://www.howtoforge.com/tutorial/how-to-install-kubernetes-on-ubuntu/