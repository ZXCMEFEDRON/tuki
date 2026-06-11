from rest_framework import serializers

from honey.models import Group, Honey, Stock, Order, Feedback


class GroupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Group
        fields = ['id', 'name', 'picture', 'user']


class HoneySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    class Meta:
        model = Honey
        fields = ['id', 'name', 'group', 'picture', 'user']


class StockSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Stock
        fields = ['id', 'name', 'group', 'count', 'user']


class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Order
        fields = ['id', 'name', 'group', 'count', 'user']


class FeedbackSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Feedback
        fields = ['id', 'name', 'group', 'comment', 'picture', 'user']

