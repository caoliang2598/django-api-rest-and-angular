from rest_framework import serializers

from .models import User, Post, Photo,Plan, Activity


class UserSerializer(serializers.ModelSerializer):
    plans = serializers.HyperlinkedIdentityField('plans', view_name='userplan-list', lookup_field='username')


    class Meta:
        model = User
        read_only_fields = ('id',)
        write_only_fields = ('password',)
        fields = ('id', 'username', 'first_name', 'last_name', 'sex', 'desc', 'plans')


    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        if attrs.get('password'):
            user.set_password(attrs['password'])
        return user





class PlanSerializer(serializers.ModelSerializer):
    authorName = serializers.Field(source='usr.username')
    authorId = serializers.Field(source='usr.id')

    usr = UserSerializer(required=False)
    usr = serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='username', required=False)
    authorDesc = serializers.Field(source='usr.desc')
    acts = serializers.HyperlinkedIdentityField('activitis', view_name='planactivity-list', lookup_field='')
    class Meta:
        model = Plan
        fields = ('id', 'title', 'des', 'authorName', 'arrTime', 'acts', 'desc', 'authorDesc', 'authorId', 'usr')


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    photos = serializers.HyperlinkedIdentityField('photos', view_name='postphoto-list')
    author = serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='username')
    
    def get_validation_exclusions(self):
        # Need to exclude `user` since we'll add that later based off the request
        exclusions = super(PostSerializer, self).get_validation_exclusions()
        return exclusions + ['author']
    
    class Meta:
        model = Post


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.Field('image.url')
    
    class Meta:
        model = Photo
