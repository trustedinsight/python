import six


class PNMessageResult(object):
    def __init__(self, message, subscription, channel, timetoken, user_metadata=None, issuing_client_id=None):
        assert message is not None

        if subscription is not None:
            assert isinstance(subscription, six.string_types)

        if channel is not None:
            assert isinstance(channel, six.string_types)

        if issuing_client_id is not None:
            assert isinstance(issuing_client_id, six.string_types)

        assert isinstance(timetoken, six.integer_types)

        if user_metadata is not None:
            assert isinstance(user_metadata, object)

        self.message = message
        # DEPRECATED: subscribed_channel and actual_channel properties are deprecated
        # self.subscribed_channel = subscribed_channel <= now known as subscription
        # self.actual_channel = actual_channel <= now known as channel

        self.channel = channel
        self.subscription = subscription

        self.timetoken = timetoken
        self.user_metadata = user_metadata
        self.issuing_client_id = issuing_client_id


class PNPresenceEventResult(object):
    def __init__(self, event, uuid, timestamp, occupancy, subscription, channel,
                 timetoken, state, user_metadata=None):

        assert isinstance(event, six.string_types)
        assert isinstance(uuid, six.string_types)
        assert isinstance(timestamp, six.integer_types)
        assert isinstance(occupancy, six.integer_types)
        assert isinstance(channel, six.string_types)
        assert isinstance(timetoken, six.integer_types)

        if user_metadata is not None:
            assert isinstance(user_metadata, object)

        if state is not None:
            assert isinstance(user_metadata, dict)

        self.event = event
        self.uuid = uuid
        self.timestamp = timestamp
        self.occupancy = occupancy
        self.state = state

        # DEPRECATED: subscribed_channel and actual_channel properties are deprecated
        # self.subscribed_channel = subscribed_channel <= now known as subscription
        # self.actual_channel = actual_channel <= now known as channel
        self.subscription = subscription
        self.channel = channel

        self.timetoken = timetoken
        self.user_metadata = user_metadata


class PNPublishResult(object):
    def __init__(self, envelope, timetoken):
        """
        Representation of publish server response

        :param timetoken: of publish operation
        """
        self.timetoken = timetoken
