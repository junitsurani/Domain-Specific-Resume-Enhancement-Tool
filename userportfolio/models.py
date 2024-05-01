from django.db import models

class PDFDocument1(models.Model):
    file = models.FileField(upload_to='pdfs/')
    extracted_text = models.TextField(blank=True)


class Skill(models.Model):
    name = models.CharField(max_length=1000)
    
    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} | {self.skill}"


class SuggestedTechnology(models.Model):
    name = models.CharField(max_length=1000)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} | {self.project}"

class UserAccount(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class ScrapedContent(models.Model):
    content = models.TextField()

  

