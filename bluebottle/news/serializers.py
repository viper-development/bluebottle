from fluent_contents.rendering import render_placeholder
from django.utils.safestring import mark_safe

from rest_framework import serializers

from bluebottle.bluebottle_drf2.serializers import SorlImageField
from bluebottle.members.serializers import UserPreviewSerializer

from .models import NewsItem


class NewsItemContentsField(serializers.Field):
    def to_native(self, obj):
        request = self.context.get('request', None)
        contents_html = mark_safe(render_placeholder(request, obj).html)
        return contents_html


class NewsItemSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug')
    body = NewsItemContentsField(source='contents')
    main_image = SorlImageField('main_image', '300x200', )
    author = UserPreviewSerializer()

    class Meta:
        model = NewsItem
        fields = ('id', 'title', 'body', 'main_image', 'author',
                  'publication_date', 'allow_comments', 'language')


class NewsItemPreviewSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug')

    class Meta:
        model = NewsItem
        fields = ('id', 'title', 'publication_date')
