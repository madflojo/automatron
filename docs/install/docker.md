Deploying Automatron within Docker is quick and easy and can be done with two simple `docker` commands.

## Starting a Redis container

Since Automatron by default uses `redis` as a datastore we must first start a `redis` container.

```sh
$ sudo docker run -d --restart=always --name redis redis
```

The above `redis` instance will be used as a default datastore for Automatron.

## Starting the Automatron container

Once the `redis` instance is up and running we can start an Automatron instance.

```sh
$ sudo docker run -d --link redis:redis -p 8000:8000 -p 9000:9000 -v /path/to/config:/config --restart=always --name automatron madflojo/automatron
```

In the above `docker run` command we are using `-v` to mount a directory from the host to the container as `/config`. This `/config` directory will be the home to Automatron's configuration files and Runbooks.

## Dashboard

To view the Automatron dashboard simply open up `http://<host ip>:8080` in your favorite browser. As target nodes are identified and runbooks are executed, events will start to be reflected on the dashboard.

With these steps complete, we can now move to [Configuring](/configure.md) Automatron.

!!! tip
    A `docker-compose.yml` file is included in the base repository which can be used to quickly stand up environments using `docker-compose up automatron`.
