# management/commands/load_skills_and_projects.py
from django.core.management.base import BaseCommand
import json
from userportfolio.models import Skill, Project, SuggestedTechnology

class Command(BaseCommand):
    help = 'Load skills and projects from JSON data'

    def handle(self, *args, **options):
        with open('userportfolio/data/projects.json', 'r') as json_file:
            data = json.load(json_file)
            for skill_data in data['skills_and_projects']:
                skill = Skill.objects.create(name=skill_data['skill'])
                for project_data in skill_data['related_projects']:
                    project = Project.objects.create(
                        name=project_data['name'],
                        description=project_data['description'],
                        skill=skill
                    )
                    for tech_name in project_data['suggested_technologies']:
                        suggested_tech = SuggestedTechnology.objects.create(
                            name=tech_name,
                            project=project
                        )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
