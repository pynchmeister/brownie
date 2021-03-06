.. _config:

======================
The Configuration File
======================

Every project has a file ``brownie-config.json`` that holds all the configuration settings. The defaut configuration is as follows.

.. literalinclude:: ../brownie/data/config.json
    :linenos:
    :language: json

When using the Brownie console or writing scripts, you can view and edit configuration settings through the ``config`` dict. Any changes made in this way are temporary and will be reset when you exit Brownie or reset the network.

Settings
========

The following settings are available:

.. py:attribute:: networks

    Defines the available networks. The following properties can be set:

    * ``host``: The address and port of the RPC API you wish to connect to. If using `Infura <https://infura.io/>`__, be sure to obtain and include your own network access token in the address.
    * ``test-rpc``: Optional. If given, this command will be run in a shell when brownie is started. In this way you can initialize Ganache or another local environment automatically when Brownie starts.
    * ``gas_price``: The default gas price for all transactions. If left as false the gas price will be determined using ``web3.eth.gasPrice``.
    * ``gas_limit``: The default gas limit for all transactions. If left as false the gas limit will be determined using ``web3.eth.estimateGas``.
    * ``broadcast_reverting_tx``: Optional. If set to ``false``, transactions that would revert will instead raise a ``VirtualMachineError``.

.. py:attribute:: network_defaults

    Default networks settings, used when specific properties aren't defined for individual networks.

    You **must** specify a ``name`` property. This is the default network to use when brownie is loaded.

.. py:attribute:: solc

    Properties relating to the solc compiler.

    * ``optimize``: Set to true if you wish to use contract optimization.
    * ``runs``: The number of times the optimizer should run.
    * ``version``: The version of solc to use. Should be written as ``v0.x.x``. If the specified version is not present, it will be installed when Brownie loads.

.. py:attribute:: test

    Properties that affect only affect Brownie's configuration when running tests. See Test :ref:`test_settings` for detailed information on the effects and implications of these settings.

    * ``gas_limit``: Replaces the default network gas limit.

    * ``broadcast_reverting_tx``: Replaces the default network setting for broadcasting reverting transactions.

    * ``default_contract_owner``: If ``false``, deployed contracts will not remember the account that they were created by and you will have to supply a ``from`` kwarg for every contract transaction.

.. py:attribute:: logging

    Default logging levels for each brownie mode.

    * ``tx``: Transaction information
    * ``exc``: Exception information

    Valid values range from 0 (nothing) to 2 (detailed). When given as a 2 item list, it corresponds to normal/verbose. When given as a single value, adding the ``--verbose`` tag will do nothing.

.. py:attribute:: colors

    Defines the colors associated with specific data types when using Brownie. Setting a value as an empty string will use the terminal's default color.
