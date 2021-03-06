=======
Brownie
=======

Brownie is a python framework for Ethereum smart contract deployment, testing and interaction.

.. note::

    All code starting with ``$`` is meant to be run on your terminal. Code starting with ``>>>`` is meant to run inside the Brownie console.

.. note::

    This project relies heavily upon Web3.py. This documentation assumes a basic familiarity with it. You may wish to view the `Web3.py docs <https://web3py.readthedocs.io/en/stable/index.html>`__ if you have not used it previously.

Brownie has several uses:

* **Deployment**: Automate the deployment of many contracts onto the blockchain, and any transactions needed to initialize or integrate the contracts.
* **Debugging**: Get detailed information when a transaction reverts, to help you locate the issue quickly.
* **Testing**: Write unit tests in python and evaluate test coverage based on stack trace analysis. We make *no promises*.
* **Interaction**: Write scripts or use the console to interact with your contracts on the main-net, or for quick testing in a local environment.
