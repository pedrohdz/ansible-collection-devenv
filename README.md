# ansible-collection-devenv

> [!WARNING]
>
> This clone of the project has been archived.  All future work can be found
> in:
>   - [Avinode/ansible-collection-devenv](https://github.com/Avinode/ansible-collection-devenv)
> My *Ansible* playbook and roles can now be found in:
>   - [pedrohdz/ansible-playbooks-pedrohdz](https://github.com/pedrohdz/ansible-playbooks-pedrohdz)

Clone the project into
`ansible-collection-devenv/ansible_collections/avinode/devenv`.  *Ansible*
collections need to exist in a spcific directory structure while working on
them:

```bash
git clone git@github.com:Avinode/ansible-collection-devenv.git \
    ansible-collection-devenv/ansible_collections/avinode/devenv
```


The set up the project environment:

```bash
cd ansible-collection-devenv/ansible_collections/avinode/devenv
./scripts/setup-local-ansible.sh
```

Run tests:

```bash
cd ansible-collection-devenv/ansible_collections/avinode/devenv
make
```
