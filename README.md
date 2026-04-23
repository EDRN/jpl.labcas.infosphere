# 🧠 LabCAS Infosphere

The [LabCAS](https://edrn-labcas.jpl.nasa.gov/) Infosphere is an API that provides information about the Laboratory Catalog and Archive Service with privileged and unprivileged access.

This API was developed in response to [EDRN/EDRN-metadata#180](https://github.com/EDRN/EDRN-metadata/issues/180).


## 🎯 Features

This API server currently provides:

- **Health check endpoint**: `GET /ping` returns the current UTC timestamp so clients and operators can quickly verify service availability.
- **Protected imaging endpoint**: `GET /imaging` requires HTTP Basic authentication and validates users against LDAP group membership.
- **Imaging coverage report**: aggregates distinct `(site, event, participantID)` values from Solr and the DMCC API for the `Lung_Team_Project_2` and `Prostate_MRI` collections.
- **Multiple response formats**: `GET /imaging` supports `?format=json` (default) and `?format=csv`.
- **HTTPS by default**: launches with temporary self-signed TLS certificates for encrypted local transport.
- **Configurable runtime options**: command-line flags let you set Solr URL, LDAP connection settings, port, subpath handling, and logging verbosity.


## 📦 Installation

This software requires Python 3.12 or higher but lower than Python 4. To install the released version of the software, create a Python virtual environment and run

    python3 -m venv .venv
    .venv/bin/pip install jpl.labcas.infosphere==VERSION

Substitute `VERSION` for the desired version. Use `.venv/bin/pip` and `.venv/bin/python` so you do not need to activate the environment.

To install from source:

    git clone --quiet https://github.com/EDRN/jpl.labcas.infosphere
    cd jpl.labcas.infosphere
    python3 -m venv .venv
    .venv/bin/pip install --editable .


## 🚀 Usage

Launch the server by running

    .venv/bin/labcas-infosphere

Run it with `--help` to see the options. After installation, you can also run modules with `.venv/bin/python -m jpl.labcas.infosphere.main`.

👉 **Note**: The Infosphere uses the DMCC API which requires a client secret. This can be provided using an environment variable, `DMCC_CLIENT_SECRET`. If not specified, you'll be prompted to enter it.


## 📄 License

Licensed under the Apache 2.0 software license. See `LICENSE.md` for details.


## 🤝 Contributing

Issues and pull requests welcome on GitHub: https://github.com/EDRN/jpl.labcas.infosphere/issues. See also the EDRN [Code of Conduct](https://github.com/EDRN/.github/blob/main/CODE_OF_CONDUCT.md) and [Contributors' Guide](https://github.com/EDRN/.github/blob/main/CONTRIBUTING.md).


## 👤 Authors

- Sean Kelly `@nutjob4life`


## ©️ Copyright

Copyright © 2026 California Institute of Technology. U.S. Government sponsorship acknowledged.

