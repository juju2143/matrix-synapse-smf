Synapse Simple Machines Forum (SMF) Auth Provider
=================================================

Allows synapse to use SMF 2.1 (or 2.0 with Sorunome's bcrypt mod) forum accounts from its database as a password provider.

Usage
-----

Example synapse config:

.. code:: yaml

   password_providers:
    - module: "smf_auth_provider.SmfAuthProvider"
      config:
        enabled: true
        host: "localhost"
        user: "smf"
        password: "YourMySQLPassword"
        database: "smf"
        db_prefix: "smf_"
	minimum_posts: 0
