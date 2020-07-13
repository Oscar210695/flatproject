from rest_framework import serializers
from .models import Merges, Status, Branches

class StatusSerializerClass(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"

class BranchSerializerClass(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = "__all__"
      
class MergeSerializerClass(serializers.ModelSerializer):
  class Meta:
    model = Merges
    fields = ['id', 'title', 'description', 'compare_branch', 'base_branch', 'status', 'author', 'email']

  def to_representation(self, instance):
        self.fields['compare_branch'] = BranchSerializerClass(read_only=True)
        self.fields['base_branch'] = BranchSerializerClass(read_only=True)
        self.fields['status'] = StatusSerializerClass(read_only=True)
        return super(MergeSerializerClass, self).to_representation(instance)
