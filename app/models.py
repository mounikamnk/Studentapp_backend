from django.db import models
class Question(models.Model):
    CATEGORY_APTITUDE = 'aptitude'
    CATEGORY_JAVA = 'java'
    CATEGORY_REASONING = 'reasoning'
    CATEGORY_PYTHON = 'python'
    CATEGORY_CHOICES = [
        (CATEGORY_APTITUDE, 'Aptitude'),
        (CATEGORY_JAVA, 'Java'),
        (CATEGORY_REASONING, 'Reasoning'),
        (CATEGORY_PYTHON, 'Python'),
    ]

    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)

    # store correct option as 'a'/'b'/'c'/'d'
    correct_option = models.CharField(max_length=1, choices=[
        ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')
    ])

    created_at = models.DateTimeField(auto_now_add=True)

    def correct_text(self):
        return {
            'a': self.option_a,
            'b': self.option_b,
            'c': self.option_c,
            'd': self.option_d
        }[self.correct_option]

    def __str__(self):
        return f"{self.category} - {self.text[:50]}"

