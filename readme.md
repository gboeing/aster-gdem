# ASTER Global DEM Data

ASTGTM v003 https://doi.org/10.5067/ASTER/ASTGTM.003

script will download these data from https://search.earthdata.nasa.gov/search?q=C1575726572-LPDAAC_ECS

contains 22,912 granules (est size 368.1 GB)


## postgres

```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt bionic-pgdg main" > /etc/apt/sources.list.d/postgres.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update
sudo apt upgrade
sudo apt autoremove
sudo apt install postgresql-client-12 postgresql-12 pgadmin4 postgis

sudo -u postgres psql
CREATE EXTENSION adminpack;
CREATE DATABASE gisdb;
\connect gisdb;
CREATE SCHEMA postgis;
ALTER DATABASE gisdb SET search_path=public, postgis, contrib;
\connect gisdb;
CREATE EXTENSION postgis SCHEMA postgis;
\q

sudo service postgresql restart

sudo -u postgres psql
SELECT name, setting FROM pg_settings where category='File Locations';
\q

sudo service postgresql stop
sudo chown postgres /mnt/data/pgdata
sudo gedit /etc/postgresql/12/main/postgresql.conf
sudo rsync -av /var/lib/postgresql/12/main/ /mnt/data/pgdata
sudo mv /var/lib/postgresql/12/main /var/lib/postgresql/12/main.bak
sudo service postgresql start

```