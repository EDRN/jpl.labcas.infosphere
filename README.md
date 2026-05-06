# 🧠 LabCAS Infosphere

The [LabCAS](https://edrn-labcas.jpl.nasa.gov/) Infosphere is an API that provides information about the Laboratory Catalog and Archive Service for the [Early Detection Research Network](https://edrn.cancer.gov/).


## 💁 Example Usage

To retreive the imaging coverage report using the `curl` command:

    curl --silent --user 'secret:p4ssw0rd' https://edrn-labcas.jpl.nasa.gov/infospshere/imaging

Replace the username `secret` and password `p4ssw0rd` with the correct credentials. You'll see a response similar to:
```json
[
    {
        "collection": "Lung_Team_Project_2",
        "site": "AvinPOWpghrek",
        "event": "1234567",
        "participantId": "00112233455"
    },
    {
        "collection": "Lung_Team_Project_2",
        "site": "AvinPOWpghrek",
        "event": "2345678",
        "participantId": "11223344556"
    },
```
To have the data formatted as CSV, run:

    curl --silent --user 'secret:p4ssw0rd' 'https://edrn-labcas.jpl.nasa.gov/infospshere/imaging?format=csv'

The response will be similar to:
```csv
collection,site,event,participantId
Lung_Team_Project_2,AvinPOWpghrek,1234567,00112233455
Lung_Team_Project_2,AvinPOWpghrek,2345678,11223344556
```

To retreive the Postman collection:

    curl --silent https://edrn-labcas.jpl.nasa.gov/infospshere/docs/postman-collection


## 🎯 Features

This API server currently provides:

- **Health check endpoint**: `GET /ping` returns the current UTC timestamp so clients and operators can quickly verify service availability.
- **Protected imaging endpoint**: `GET /imaging` requires HTTP Basic authentication and validates users against LDAP group membership.
- **Imaging coverage report**: aggregates distinct `(site, event, participantID)` values from Solr and the DMCC API for the `Lung_Team_Project_2` and `Prostate_MRI` collections.
- **Multiple response formats**: `GET /imaging` supports `?format=json` (default) and `?format=csv`.
- **[Postman](https://www.postman.com) specification**. You can retrieve a Postman-compatible specification of the API by following the link from `GET /docs`.

These endpoints are typically available at `https://SERVER/SUBPATH/ENDPOINT`, such as `https://edrn-labcas.jpl.nasa.gov/infosphere/imaging`. The `SUBPATH` may be omitted depending on configuration.


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
    pre-commit install


## 🚀 Usage

Launch the server by running

    .venv/bin/labcas-infosphere

Run it with `--help` to see the options. After installation, you can also run modules with `.venv/bin/python -m jpl.labcas.infosphere.main`. It's recommended to run the server at all times, such as under [Supervisor](https://supervisord.org/) or similar system.

👉 **Note**: The Infosphere uses the DMCC API which requires a client secret. This can be provided using an environment variable, `DMCC_CLIENT_SECRET`. If not specified, you'll be prompted to enter it.

To test locally, issue

    curl --insecure --silent https://localhost:8998/ping

You should get a timestamp.


## 📄 License

Licensed under the Apache 2.0 software license. See `LICENSE.md` for details.


## 🤝 Contributing

[Issues and pull requests](https://github.com/EDRN/jpl.labcas.infosphere/) are welcome on GitHub. See also the EDRN [Code of Conduct](https://github.com/EDRN/.github/blob/main/CODE_OF_CONDUCT.md) and [Contributors' Guide](https://github.com/EDRN/.github/blob/main/CONTRIBUTING.md).


## 👤 Credits

- Developed by Sean Kelly `@nutjob4life`
- QC by Heather Kincaid `@hoodriverheather`

This API was developed in response to [EDRN/EDRN-metadata#180](https://github.com/EDRN/EDRN-metadata/issues/180).


## ©️ Copyright

Copyright © 2026 California Institute of Technology. U.S. Government sponsorship acknowledged.

