from django.core.management.base import BaseCommand
from accounts.models import Skill


class Command(BaseCommand):
    help = 'Populate the database with common skills'

    def handle(self, *args, **kwargs):
        skills = [
            # Programming Languages
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin',
            'Go', 'Rust', 'Scala', 'R', 'MATLAB', 'SQL', 'HTML', 'CSS',
            
            # Frameworks & Libraries
            'Django', 'Flask', 'FastAPI', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js',
            'Spring Boot', 'ASP.NET', 'Laravel', 'Ruby on Rails', 'jQuery', 'Bootstrap', 'Tailwind CSS',
            
            # Data Science & ML
            'Machine Learning', 'Deep Learning', 'Neural Networks', 'Natural Language Processing',
            'Computer Vision', 'Data Analysis', 'Data Visualization', 'Statistical Analysis',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'Pandas', 'NumPy', 'Matplotlib',
            'Seaborn', 'Tableau', 'Power BI',
            
            # Databases
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQL Server', 'SQLite',
            'Cassandra', 'DynamoDB', 'Elasticsearch',
            
            # Cloud & DevOps
            'AWS', 'Azure', 'Google Cloud Platform', 'Docker', 'Kubernetes', 'Jenkins',
            'CI/CD', 'Git', 'GitHub', 'GitLab', 'Linux', 'Bash', 'Terraform', 'Ansible',
            
            # Web Development
            'RESTful API', 'GraphQL', 'Microservices', 'Web Services', 'Responsive Design',
            'Progressive Web Apps', 'Single Page Applications', 'Web Security',
            
            # Mobile Development
            'iOS Development', 'Android Development', 'React Native', 'Flutter', 'Xamarin',
            
            # Other Technical Skills
            'Agile', 'Scrum', 'Test-Driven Development', 'Unit Testing', 'Integration Testing',
            'Object-Oriented Programming', 'Functional Programming', 'Design Patterns',
            'System Design', 'Algorithms', 'Data Structures', 'Problem Solving',
            
            # Soft Skills
            'Communication', 'Leadership', 'Team Collaboration', 'Project Management',
            'Time Management', 'Critical Thinking', 'Problem Solving', 'Adaptability',
        ]
        
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
