from django.db.migrations import serializer
from rest_framework import serializers

from ads.models import User, Location, Ads


class UserListSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    class Meta:
        model = User
        exclude = ("password", "role")




class UserCreateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"

    def is_valid(self, *, raise_exception=False):
        self.locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        for locations in self.locations:
            obj, _ = Location.objects.get_or_create(name=locations)
            user.locations.add(obj)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("role",)

    def is_valid(self, *, raise_exception=False):
        self.locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        for locations in self.locations:
            obj, _ = Location.objects.get_or_create(name=locations)
            user.locations.add(obj)
            user.save()
        return user



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


class AdsListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field="username"
    )
    category = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Ads
        fields = "__all__"


class AdsDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field="username"
    )
    category = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Ads
        fields = "__all__"


class AdsUpdateSerializer(serializers.ModelSerializer):
    pass


class AdsCreateSerializer(serializers.ModelSerializer):
    pass


class AdsDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ["id"]
