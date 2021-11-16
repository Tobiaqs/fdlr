# fdlr
## Setting up development environment
- Check out the repo in, let's say, `~/repos/fdlr`
- Create a folder somewhere called `~/docker/fdlr-dev`
- In `fdlr-dev`, run `ln -s ~/repos/fdlr/config/dev/docker-compose.yml`
- In `fdlr-dev`, create a `.env` based on the relevant `.env.example`

## Setting up production environment
Same steps but substitute `dev` with `prod`.
