#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import sys
import argparse

import zmq
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient

parser = argparse.ArgumentParser(description='JSONRPC client')
parser.add_argument('--host', default='127.0.0.1', help='host address')
parser.add_argument('--port', type=int, default=6666, help='host port number')
parser.add_argument('--city', default='wrocław', help='city name')
args = parser.parse_args()

context = zmq.Context()
host = "tcp://" + args.host + ":" + str(args.port)
rpc = RPCClient(JSONRPCProtocol(), ZmqClientTransport.create(context, host))
rpc_client = rpc.get_proxy(prefix='pogoda.')
print(rpc_client.dajdla(args.city))