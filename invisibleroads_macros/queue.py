import logging
import msgpack
import zmq
from time import sleep


SOCKET_CONTEXT = zmq.Context()


class Pusher(object):

    def __init__(self, socket_url, bind_socket=False):
        self.socket_url = socket_url
        self.socket = SOCKET_CONTEXT.socket(zmq.PUSH)
        connect = self.socket.bind if bind_socket else self.socket.connect
        connect(socket_url)

    def push_packet(self, packet):
        self.socket.send(packet)

    def push_pack(self, pack):
        self.push_packet(msgpack.packb(pack))


class Puller(object):

    def __init__(self, socket_url, bind_socket=False):
        self.socket_url = socket_url
        self.socket = SOCKET_CONTEXT.socket(zmq.PULL)
        connect = self.socket.bind if bind_socket else self.socket.connect
        connect(socket_url)
        logging.info('Listening on %s', socket_url)

    def yield_packet(self, raise_keyboard_interrupt=False):
        try:
            while True:
                yield self.socket.recv()
        except KeyboardInterrupt:
            if raise_keyboard_interrupt:
                raise

    def yield_pack(self, raise_keyboard_interrupt=True):
        for packet in self.yield_packet(raise_keyboard_interrupt):
            yield msgpack.unpackb(packet, use_list=False)


class Publisher(object):

    def __init__(self, socket_url, bind_socket=False):
        self.socket_url = socket_url
        self.socket = SOCKET_CONTEXT.socket(zmq.PUB)
        connect = self.socket.bind if bind_socket else self.socket.connect
        connect(socket_url)
        self.socket.send('')
        sleep(0.1)

    def publish_packet(self, channel, packet):
        self.socket.send('%s %s' % (channel, packet))

    def publish_pack(self, channel, pack):
        self.publish_packet(channel, msgpack.packb(pack))


class Subscriber(object):

    def __init__(self, socket_url, bind_socket=False, channel=''):
        self.socket_url = socket_url
        self.socket = SOCKET_CONTEXT.socket(zmq.SUB)
        self.socket.subscribe = str(channel)
        connect = self.socket.bind if bind_socket else self.socket.connect
        connect(socket_url)
        if channel:
            logging.info('Listening on %s channel=%s', socket_url, channel)
        else:
            logging.info('Listening on %s', socket_url)

    def yield_channel_packet(self, raise_keyboard_interrupt=False):
        try:
            while True:
                channel, packet = self.socket.recv().split(' ', 1)
                yield channel, packet
        except KeyboardInterrupt:
            if raise_keyboard_interrupt:
                raise

    def yield_channel_pack(self, raise_keyboard_interrupt=False):
        for channel, packet in self.yield_channel_packet(
                raise_keyboard_interrupt):
            yield channel, msgpack.unpackb(packet, use_list=False)
