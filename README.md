# aetpi

Asynchronous External Task Processor Interface - the bpmn adoption of asgi

AETPI is a standard for Python asynchronous external task proccessors. Its idea is to provide a protocol specification
that allows to build applications capable to proccess pieces of work for - e.g. bpmn driven - process orchestrators.

This project contains - at the moment - only the reference typehints required to implement the protocol.
A reference implementation and detailed documentation will follow.


## Development

```shell
# setup evn ...
uv sync

# install commit hooks
prek install
```
