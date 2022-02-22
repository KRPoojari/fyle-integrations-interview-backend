from rest_framework import serializers
from .models import Teacher
from apps.students.models import Assignment, GRADE_CHOICES, ASSIGNMENT_STATE_CHOICES


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    """
    Teacher Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate_grade(self, val):
        for key in GRADE_CHOICES:
            if val == key[0]:
                return val
        raise serializers.ValidationError('is not a valid choice.')
        
    def validate(self, attrs): 
        
        if 'content' in attrs:
            raise serializers.ValidationError('Teacher cannot change the content of the assignment')
        if 'student' in attrs:
            raise serializers.ValidationError('Teacher cannot change the student who submitted the assignment')

        if self.context['teacher_id'] != self.instance.teacher.id:
            raise serializers.ValidationError('Teacher cannot grade for other teacher''s assignment')
        
        if self.instance.state == 'DRAFT' and 'grade' in attrs:
            raise serializers.ValidationError('SUBMITTED assignments can only be graded')
        
        if self.instance.state == 'GRADED' and 'grade' in attrs:
            raise serializers.ValidationError('GRADED assignments cannot be graded again')
        
        
        if self.partial:
            return attrs
        return super().validate(attrs)