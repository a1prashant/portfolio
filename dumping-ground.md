


### Run `Vault` in Container with persistant storage:
```
sudo su -
mkdir -p /srv/vault/config /srv/vault/data /srv/vault/log
chmod 777 /srv/vault/data
docker run --cap-add=IPC_LOCK -v /srv/vault/config:/vault/config -v /srv/vault/data:/vault/data -v /srv/vault/logs:/vault/logs -e 'VAULT_LOCAL_CONFIG={"backend": {"file": {"path": "/vault/file"}}, "default_lease_ttl": "168h", "max_lease_ttl": "720h"}' vault server
```

