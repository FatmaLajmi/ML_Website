import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import Skill


class Command(BaseCommand):
    help = 'Load skills from discriminative_skills.json file into the database'

    def handle(self, *args, **options):
        # Path to the JSON file
        json_path = os.path.join(settings.BASE_DIR, 'ml_models', 'models', 'discriminative_skills.json')
        
        # Check if file exists
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_path}'))
            return
        
        # Load skills from JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                skills_data = json.load(f)
            
            # Validate data
            if not isinstance(skills_data, list):
                self.stdout.write(self.style.ERROR('JSON file must contain a list of skills'))
                return
            
            # Track stats
            created_count = 0
            existing_count = 0
            
            # Create skills
            for skill_name in skills_data:
                skill_name = skill_name.strip()
                if not skill_name:
                    continue
                
                # Create or get the skill (case-insensitive check)
                skill, created = Skill.objects.get_or_create(
                    name__iexact=skill_name,
                    defaults={'name': skill_name}
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created skill: {skill_name}'))
                else:
                    existing_count += 1
            
            # Summary
            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.SUCCESS(f'Skills loaded successfully!'))
            self.stdout.write(self.style.SUCCESS(f'Created: {created_count} new skills'))
            self.stdout.write(self.style.SUCCESS(f'Already existed: {existing_count} skills'))
            self.stdout.write(self.style.SUCCESS(f'Total skills in database: {Skill.objects.count()}'))
            self.stdout.write(self.style.SUCCESS('='*50))
            
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Error parsing JSON file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading skills: {e}'))
