__author__ = 'Joe Linn'

from .abstract import AbstractRiver


class RabbitMQ(AbstractRiver):
    """
    @see: https://github.com/elasticsearch/elasticsearch-river-rabbitmq/blob/master/README.md
    """

    river_type = 'rabbitmq'

    EXCHANGE_DIRECT = 'direct'
    EXCHANGE_FANOUT = 'fanout'

    def __init__(self, client, name, index=None, doc_type=None, bulk_size=100, bulk_timeout='10ms',
                 host='localhost', port=5672, user='guest', password='guest'):
        """
        @param client:
        @type client: pylastica.client.Client
        @param name: name of the river
        @type name: str
        @param index: default index for this river
        @type index: str or pylastica.index.Index
        @param doc_type: default document type for this river
        @type doc_type: str or pylastica.doc_type.DocType
        @param bulk_size: bulk size
        @type bulk_size: int
        @param bulk_timeout: "10ms", for example
        @type bulk_timeout: str
        @param host: RabbitMQ hostname or ip address
        @type host: str
        @param port: RabbitMQ port
        @type port: int
        @param user: RabbitMQ user
        @type user: str
        @param password: RabbitMQ password
        @type password: str
        """
        super(RabbitMQ, self).__init__(client, name, index, doc_type, bulk_size, bulk_timeout)
        self.set_host(host).set_port(port).set_user(user).set_password(password)

    def set_host(self, host):
        """
        Set RabbitMQ host
        @param host: hostname or ip address
        @type host: str
        @return:
        @rtype: self
        """
        return self.set_param('host', host)

    def set_port(self, port):
        """
        Set RabbitMQ port
        @param port: port number
        @type port: int
        @return:
        @rtype: self
        """
        return self.set_param('port', port)

    def set_user(self, user):
        """
        Set RabbitMQ user
        @param user: username
        @type user: str
        @return:
        @rtype: self
        """
        return self.set_param('user', user)

    def set_password(self, password):
        """
        Set RabbitMQ password
        @param password:
        @type password: str
        @return:
        @rtype: self
        """
        return self.set_param('pass', password)

    def set_vhost(self, vhost='/'):
        """
        Set the RabbitMQ vhost
        @param vhost: defaults to /
        @type vhost: str
        @return:
        @rtype: self
        """
        return self.set_param('vhost', vhost)

    def set_queue(self, queue='elasticsearch'):
        """
        Set the RabbitMQ queue name
        @param queue:
        @type queue: str
        @return:
        @rtype: self
        """
        return self.set_param('queue', queue)

    def set_exchange(self, exchange='elasticsearch'):
        """
        Set the RabbitMQ exchange
        @param exchange:
        @type exchange:
        @return:
        @rtype:
        """
        return self.set_param('exchange', exchange)

    def set_routing_key(self, routing_key='elasticsearch'):
        """
        Set the routing key
        @param routing_key:
        @type routing_key: str
        @return:
        @rtype: self
        """
        return self.set_param('routing_key', routing_key)

    def set_exchange_declare(self, declare=True):
        """
        Enable / disable exchange declaration
        @param declare: defaults to True
        @type declare: bool
        @return:
        @rtype: self
        """
        return self.set_param('exchange_declare', bool(declare))

    def set_exchange_type(self, exchange_type='direct'):
        """
        Set exchange type
        @param exchange_type: see EXCHANGE_* class properties for options
        @type exchange_type: str
        @return:
        @rtype: self
        """
        return self.set_param('exchange_type', exchange_type)

    def set_exchange_durable(self, durable=True):
        """
        Enable / disable exchange durability
        @param durable: defaults to True
        @type durable: bool
        @return:
        @rtype: self
        """
        return self.set_param('exchange_durable', bool(durable))

    def set_queue_declare(self, declare=True):
        """
        Enable / disable queue declaration
        @param declare: defaults to True
        @type declare: bool
        @return:
        @rtype: self
        """
        return self.set_param('queue_declare', bool(declare))

    def set_queue_durable(self, durable=True):
        """
        Enable / disable queue durability
        @param durable: defaults to True
        @type durable: bool
        @return:
        @rtype: self
        """
        return self.set_param('queue_durable', bool(durable))

    def set_queue_auto_delete(self, auto=False):
        """
        Enable / disable queue auto deletion
        @param auto: defaults to False
        @type auto: bool
        @return:
        @rtype: self
        """
        return self.set_param('queue_auto_delete', bool(auto))
