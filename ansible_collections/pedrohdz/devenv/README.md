> **NOTICE** - This project has been migrated to
> [Avinode/ansible-collection-devenv](https://github.com/Avinode/ansible-collection-devenv).


# ansible-collection-devenv

```bash
python3.9 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install ansible ansible-lint molecule[docker] yamllint
```

Run tests:

```bash
cd ansible_collections/pedrohdz/devenv/

ansible-test sanity --docker default
ansible-test units --docker default

ansible-test integration --docker ubuntu2004 \
    --python-interpreter /usr/bin/python3

ansible-test integration \
    --docker geerlingguy/docker-debian10-ansible:latest \
    --python-interpreter /usr/bin/python3
```
