from rest_framework import serializers
from .models import Task, TaskSubmission, TaskImage
from employee.models import Employee


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Employee.objects.all()
    )

    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        assigned = validated_data.pop('assigned_to', [])
        task = Task.objects.create(**validated_data)
        task.assigned_to.set(assigned)
        return task

    def update(self, instance, validated_data):
        assigned = validated_data.pop('assigned_to', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if assigned is not None:
            instance.assigned_to.set(assigned)

        return instance

class TaskImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskImage
        fields = "__all__"

class TaskSubmissionSerializer(serializers.ModelSerializer):
    images = TaskImageSerializer(many=True, read_only=True)

    task_name = serializers.SerializerMethodField()
    task_description = serializers.SerializerMethodField()
    submitted_by = serializers.SerializerMethodField()  # <-- CHANGED HERE

    class Meta:
        model = TaskSubmission
        fields = [
            "id",
            "task",
            "task_name",
            "task_description",
            "submitted_by",   # <-- NOW THIS RETURNS NAME
            "submitted_at",
            "status",
            "images"
        ]

    def get_task_name(self, obj):
        return obj.task.task_name if obj.task and obj.task.task_name else None

    def get_task_description(self, obj):
        return obj.task.description if obj.task and obj.task.description else None

    def get_submitted_by(self, obj):
        return obj.submitted_by.name if obj.submitted_by else None
