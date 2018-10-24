#!/usr/bin/env python

import os, sys, signal
import argparse
import config

import zmq
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqServerTransport
from tinyrpc.server import RPCServer
from tinyrpc.dispatch import RPCDispatcher

import logging, logger

from driver import create_driver
import api

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JSONRPC server')
    parser.add_argument('--host', default='127.0.0.1', help='host address')
    parser.add_argument('--port', type=int, default=6666, help='host port number')
    parser.add_argument('--logfile', default=None, help='logfile name, default=stderr')
    parser.add_argument('--browser', help='browser name', default='firefox')
    parser.add_argument('--hide_browser', default=True, help='use xvfb to run browser')
    parser.add_argument('-v', '--verbose', action='count', help='be more verbose')
    args = parser.parse_args()

    logger.configure_logger(args.logfile, args.verbose)

    context = zmq.Context()
    dispatcher = RPCDispatcher()
    host = "tcp://" + args.host + ":" + str(args.port)
    transport = ZmqServerTransport.create(context, host)

    rpc_server = RPCServer(transport, JSONRPCProtocol(), dispatcher)
    rpc_server.trace = lambda dir, msg, ctx: logging.debug('%s%s%s', dir, msg, ctx)

    try:
        logging.info('Initializing browser driver ...')
        browser = create_driver(args.browser, args.hide_browser)
        logging.info('Initializing browser driver success')
        logging.info('Registering API')
        api = api.Api(browser, dispatcher)
    except:
        logging.error('Initializing failed')
        sys.exit(1)

    try:
        logging.info('Starting RPC server on ' + host)
        rpc_server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(signal.SIGINT)
    finally:
        logging.shutdown()
