## Synopsis

This project aims to improve Openstack's Tacker auditability. In other words, our goal is to do a periodical check on Tacker's log files, in order to verify that there hasn't been any security breach or modification of their content. This whole process can also be referred to as immutabilization of secure log files

## Motivation

A short description of the motivation behind the creation and maintenance of the project. This should explain **why** the project exists

## Code Organization

# Components

The immutabilization process has been put in place as a set components, with each one of those doing a specific function. Firstly, there is the secure logger script that takes as input the log file provided by Tacker and generates a secure log file following the mechanisms mentionned in this research work [Immutabilization fo secure logs](https://www.scytl.com/wp-content/uploads/2017/01/Distributed-Immutabilization-of-Secure-Logs_Scytl.pdf). Afterwards, the hash reader component reads the checkpoint hashes in the secure log file and puts them in a specific checkpoint hashes file.
The launcher bash script reads those checkpoint hashes from the generated file, then sends each checkpoint hash in the OP_RETURN output of a Bitcoin transaction. The laucher does also launch the producer script, which the first componenet of a RabbitMQ connected componenets (producder, consumer, validator, client).   
# Installation

Provide code examples and explanations of how to get the project.

## API Reference

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.


## Contributors

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

