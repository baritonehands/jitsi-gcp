# Jitsi on Google Cloud Platform

This is a quick deployment-manager configuration to run Jitsi on Google Cloud Platform.

## Requirements

Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts). Also requires
`openssl` to be installed.

## What is Jitsi?

Jitsi is a multi-platform open-source video conferencing service. https://jitsi.org

## Rationale

The goal with this project was to get your very own Jitsi instance up and running
in Google Cloud Platform as fast as possible, at a low cost. Based on the pricing
calculator in April 2020, the cost of running 24/7 would be about
[$22.26 per month](https://cloud.google.com/products/calculator#id=506e5e09-0808-4b88-afa5-8d12c24d0d78).

It is based on the [Docker Jitsi Quickstart](https://github.com/jitsi/docker-jitsi-meet).

Caveats:
* JVB component is preemptible which means it will be restarted every day, and likely more often.
* Costs could be $4/mo lower with NAT instead of ephemeral external IPs.
* Domain and SSL certificate costs are not included in the estimate.
* Network egress is also not included in the estimate.

### Disclaimer

Use this repo at your own risk and expense. The included Google Cloud deployment is not free to run,
but has been designed to minimize costs. You are responsible for monitoring and configuring
your Google Cloud account for optimal pricing.

## One Time Setup

Add the firewall rules for http and Jitsi's video bridge:

    gcloud deployment-manager deployments create jitsi-firewall --config firewall.yaml

## Create Instances

Run the deployment manager to create instances:

    gcloud deployment-manager deployments create jitsi --template jitsi.jinja --properties jvb_password:`openssl rand -hex 16`,jicofo_password:`openssl rand -hex 16`,jicofo_secret:`openssl rand -hex 16`

**Note**: The openssl commands are required to generate random secure passwords.

Once things are running, you can grab the external IP of the jitsi-web instance from
the console UI, or use gcloud:

    gcloud compute instances describe jitsi-web --format='get(networkInterfaces[0].accessConfigs[0].natIP)'

To destroy, run the delete command:

    gcloud deployment-manager deployments delete jitsi

## LetsEncrypt SSL setup

See [Docker Jitsi Let's Encrypt Config](https://github.com/jitsi/docker-jitsi-meet#lets-encrypt-configuration).

You would add the required configuration to env.yaml. A static IP would also
probably be a good idea for the jitsi-web node. You need to have the DNS set up
pointed at jitsi-web before it comes up in order for Let's Encrypt to work.
