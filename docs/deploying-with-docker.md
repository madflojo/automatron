Deploying Automatron within Docker is quick and easy. Since Automatron by default uses `redis` as a datastore we must first start a `redis` instance.

```console
$ sudo docker run -d --restart=always --name redis redis
```

Once `redis` is up and running you can start an Automatron instance.

```console
$ sudo docker run -d --link redis:redis -v /path/to/config:/config --restart=always --name automatron madflojo/automatron
```