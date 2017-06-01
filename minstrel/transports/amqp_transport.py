class AMQPTransport:

    host = None
    user = None
    password = None

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def write(self, mock):
        pass

        # def amqp_applier(amqp_url: str, exchange_name: str, routing_key: str,
        #                 dicts: Iterable[dict]):
        #     connection = kombu.Connection(amqp_url)
        #     exchange = kombu.Exchange(exchange_name, type='topic')
        #     producer = connection.Producer(exchange=exchange)

        #     for dct in dicts:
        #         producer.publish(
        #             json.dumps(dct),
        #             exchange=exchange,
        #             routing_key=routing_key,
        #         )
