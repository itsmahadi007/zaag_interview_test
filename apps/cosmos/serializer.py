from rest_framework import serializers

from apps.cosmos.models import DataModel, RootSample, SubSample, Results, Taxonomy


class DataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataModel
        fields = "__all__"


class RootSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RootSample
        fields = "__all__"


class SubSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSample
        fields = "__all__"


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = "__all__"


class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = "__all__"


class SubSampleDetailsSerializer(serializers.ModelSerializer):
    root_sample = RootSampleSerializer()

    class Meta:
        model = SubSample
        fields = "__all__"


class ResultsDetailsSerializer(serializers.ModelSerializer):
    sub_sample = SubSampleDetailsSerializer()

    class Meta:
        model = Results
        fields = "__all__"


class TaxonomyDetailsSerializer(serializers.ModelSerializer):
    result_of = ResultsDetailsSerializer()

    class Meta:
        model = Taxonomy
        fields = "__all__"


class DataModelDetailsSerializer(serializers.ModelSerializer):
    result_of = ResultsDetailsSerializer()
    taxonomy = TaxonomyDetailsSerializer()

    class Meta:
        model = DataModel
        fields = "__all__"


class TaxonomyDetailsReverseSerializer(serializers.ModelSerializer):
    data_models = DataModelSerializer(many=True)
    class Meta:
        model = Taxonomy
        fields = "__all__"


class ResultsDetailsReverseSerializer(serializers.ModelSerializer):
    taxonomy = TaxonomyDetailsReverseSerializer(many=True)
    data_models = DataModelSerializer(many=True)
    class Meta:
        model = Results
        fields = "__all__"


class SubSampleDetailsReverseSerializer(serializers.ModelSerializer):
    results = ResultsDetailsReverseSerializer(many=True)

    class Meta:
        model = SubSample
        fields = "__all__"


class RootSampleDetailsSerializer(serializers.ModelSerializer):
    sub_samples = SubSampleDetailsReverseSerializer(many=True)

    class Meta:
        model = RootSample
        fields = "__all__"
