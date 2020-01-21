# Arena

Connected arena.

## Table of Contents <!-- omit in toc -->

- [Arena](#arena)
  - [Setup](#setup)
  - [Mongodb Registration and Setup](#mongodb-registration-and-setup)
  - [Adding Entrypoints](#adding-entrypoints)
  - [Mongodb Samples](#mongodb-samples)
  - [NNG Samples](#nng-samples)
  - [Digital Ocean](#digital-ocean)
  - [Helm](#helm)
    - [Creating secrets for Kubernetes to access external private resources](#creating-secrets-for-kubernetes-to-access-external-private-resources)
    - [Kubernetes Entity Notes](#kubernetes-entity-notes)
    - [Uninstallation Notes](#uninstallation-notes)

## Setup

1. Run `pip install -e` from root.
2. Run `arena` to start arena. *(This currently does nothing.)*
3. Run `pytest` to execute full test suite.

## Mongodb Registration and Setup

*If this is your first time registering, please validate and update these instructions to match your experience.*

1. Navigate to [User Registration](https://cloud.mongodb.com/user#/atlas/register/accountProfile) and register for an atlas account.
2. Create an Organization.
3. Create a Project.
4. Create a free tier cluster.
5. Create a new user account, as instructed, save the password into your .env file.
6. Add your IP, as instructed, to the whitelist.
7. Good to go! Run the Mongodb Sample with `arena_mongo`.

## Adding Entrypoints

1. Modify `setup.py:setup.entry_points.console_scripts`.
2. Add a new entrypoint to the `arena/__main__.py` file to match.
3. Run `pip install -e .` to compile the entrypoint.

## Mongodb Samples

Note that MongoDB sample will fail unless you have set up an atlas instance.

1. Run `arena_mongo` to trigger the mongo sample path.

## NNG Samples

1. Run `arena_nng` to trigger the nng sample path.

## Digital Ocean

> These instructions are making an assumption that you are utilizing your own Digital Ocean account. Eventuall we should use a Rhythm Collective team account for simplicity.

1. Create an API key on Digital Ocean.

    - <https://cloud.digitalocean.com/account/api/tokens>
    - Generate new token.
    - Copy token to the next command.

2. Authenticate your doctl instance.

    > `doctl auth -t <api key>`

3. Initialize a cluster.

    > `doctl kubernetes cluster create test --count 2 --region sfo2`

4. When done, while we are in Alpha, destroy cluster.

    > `doctl kubernetes cluster delete -t test`

5. Check that the cluster is truly deleted, it will will cost you hourly.

    > `doctl kubernetes cluster list`

## Helm

>These instructions assume you are working on a kubernetes cluster in a cloud service that supports LoadBalancers!

1. Create a directory called `path_programs` somewhere reasonable, add `path_programs` to your user path variable.
2. Download [Helm](https://github.com/helm/helm/releases), place the executable in `path_programs` and rename to `helm.exe`.
3. Download [SOPS](https://github.com/mozilla/sops/releases), place the executable in `path_programs` and rename to `sops.exe`.
4. Download [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-windows), place the executable in `path_programs` and rename to `kubectl.exe`.
5. Download [kubeseal](https://github.com/bitnami-labs/sealed-secrets/releases), plase executable in `path_programs` and rename to `kubeseal.exe`.

6. Install kubeseal on the cluster.

   > ```bash
   > helm install --namespace kube-system --name my-release stable/sealed-secrets
   > ```

7. Create the cert-manager namespace. `kubectl create namespace cert-manager`.
8. Navigate to `helmstuff/arena`.
9. Install Kong

    > ``` bash
    > helm repo add kong https://charts.konghq.com
    > helm repo update
    > kubectl create namespace kong
    > helm install kong kong/kong --namespace kong --version 1.0.0 --values config/kong-values.yaml
    > ```

10. Validate Kong _LoadBalancer_ is set up.

    > **Wait for External IP to change from \<pending\> to an address!**
    >
    > ``` bash
    > kubectl get all --namespace kong
    > ```
    >
    > **Wait for External IP to change from \<pending\> to an address!**

11. Set up the DNS records.

    >
    > ``` bash
    > doctl compute domain records create --record-type A --record-name proxy --record-data <load-balancer-ip> rhythmcollective.online
    > ```
    >
    > ``` bash
    > doctl compute domain records create --record-type CNAME --record-name arena --record-data proxy.rhythmcollective.online arena.rhythmcollective.online
    > ```
    >

12. Install cert-manager.

    > ``` bash
    > kubectl apply --validate=false -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.12/deploy/manifests/00-crds.yaml
    > kubectl create namespace cert-manager
    > helm repo add jetstack https://charts.jetstack.io
    > helm repo update
    > helm install cert-manager --namespace cert-manager --version v0.12.0 jetstack/cert-manager
    > ```

13. Run `helm install arena .` to roll out arena for the first time.

### Creating secrets for Kubernetes to access external private resources

> ``` bash
> kubeseal --fetch-cert \
> --controller-name=arena \
> --controller-namespace=arena \ # I think this is wrong.
> pub-cert.pem
> ```

### Kubernetes Entity Notes

> ``` bash
> kubectl describe service/arena-rhythmcollective-online
> kubectl describe ingress/arena-rhythmcollective-online
> kubectl get pods --namespace cert-manager #The shorest name.
> kubectl logs <cert-manager pod name from above> -n cert-manager
> ```

### Uninstallation Notes

> ``` bash
> helm uninstall arena
> helm uninstall kong -n kong
> helm uninstall cert-manager -n cert-manager
> ```
