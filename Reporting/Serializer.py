from rest_framework import serializers
from SanaPlus.models import Apps_tokens_admin
from .models import (
                    Record_Events,
                    PageRank,
                    Reserve,
                    Sell,
                    visited_Product,
                    Search_Product,
                    Register_user,
                    )



class Apps_tokens_admin_serialize(serializers.ModelSerializer):
    class Meta:
        model = Apps_tokens_admin
        fields = '__all__'


class clicked_serialize(serializers.ModelSerializer):
    class Meta:
        model = Record_Events
        fields = '__all__'




class Page_Ranking_serialize(serializers.ModelSerializer):
    class Meta:
        model = PageRank
        fields = '__all__'


class Reservation_serializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = '__all__'



class Seller_serializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = '__all__'


class Visited_Product_serializer(serializers.ModelSerializer):
    class Meta:
        model = visited_Product
        fields = '__all__'



class Search_Product_serializer(serializers.ModelSerializer):
    class Meta:
        model = Search_Product
        fields = '__all__'


class Register_user_serializer(serializers.ModelSerializer):
    class Meta:
        model = Register_user
        fields = '__all__'



