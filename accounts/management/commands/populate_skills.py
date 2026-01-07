from django.core.management.base import BaseCommand
from accounts.models import Skill
import json
from pathlib import Path


class Command(BaseCommand):
    help = 'Populate the database with skills from discriminative_skills.json'

    def handle(self, *args, **kwargs):
        # Load skills from discriminative_skills.json
        json_path = Path(__file__).resolve().parent.parent.parent.parent / 'ml_models' / 'models' / 'discriminative_skills.json'
        
        try:
            with open(json_path, 'r') as f:
                skills_list = json.load(f)
            
            self.stdout.write(self.style.SUCCESS(f'Loaded {len(skills_list)} skills from {json_path.name}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Could not find {json_path}'))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Error reading JSON file: {e}'))
            return
        
        # Capitalize first letter of each skill for consistency
        skills = [skill.title() for skill in skills_list]
        
        created_count = 0
        existing_count = 0
        
        for skill_name in skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created skill: {skill_name}'))
            else:
                existing_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'\nSummary:'))
        self.stdout.write(self.style.SUCCESS(f'Created: {created_count} new skills'))
        self.stdout.write(self.style.SUCCESS(f'Already existed: {existing_count} skills'))
        self.stdout.write(self.style.SUCCESS(f'Total skills in database: {Skill.objects.count()}'))
