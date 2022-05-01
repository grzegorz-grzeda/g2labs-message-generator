# Simple C and python structure generator with serialization
`g2labs-message-generator.py` is a simple script which generates C and python
source files, capable of handling serialization and deserialization of given message definition.

# Installation
The generator needs Jinja2 to work:

`pip3 install Jinja2`

then just execute the script, providing path to the file with the message definition:
`./g2labs-message-generator.py examples/simple/simple_messages.g2msg`

# Examples
Go e.g. to`examples/simple` and just run `make`. It generates the needed source and header files and
compiles the example. Next just run `./simple_test` to check if it works.
The example generates random numbers, places them into the `simple_message` structure and then serialize and
deserialize data. At the end it performs a test if the data is not corrupted.

# Author
&copy; 2022 Grzegorz Grzęda