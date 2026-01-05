# Job ML Platform

A Django-based job matching platform powered by machine learning predictions. This platform connects job seekers with employers and provides AI-driven insights for career decisions and recruitment strategies.

## Features

### For Job Seekers
- **Smart Job Matching**: Browse and apply for jobs with AI-powered recommendations
- **Salary Predictions**: Get estimated salary ranges based on skills and experience
- **Job Title Recommendations**: Discover suitable job titles based on your skill set
- **Remote Work Eligibility**: Check your eligibility for remote positions
- **Degree Requirements**: Understand education requirements for different roles
- **Application Tracking**: Monitor the status of your job applications

### For Employers
- **Job Posting**: Create and manage job listings with admin approval workflow
- **Applicant Management**: Review and manage job applications
- **Benefits Prediction**: Get recommendations for competitive benefits packages
- **Company Growth Predictions**: Access AI insights on company growth potential
- **Revenue Growth Analysis**: Predict revenue growth based on business metrics
- **Campaign Conversion**: Optimize recruitment campaigns with conversion predictions

### Platform Features
- **Role-Based Access Control**: Separate dashboards for job seekers and employers
- **Analytics Dashboard**: Integrated Power BI dashboard for comprehensive insights
- **Machine Learning Integration**: 8 different ML models for various predictions
- **Responsive Design**: Mobile-friendly interface built with Bootstrap 5
- **Secure Authentication**: Custom user model with profile management

## Project Structure

```
WEBSITE/
├── manage.py
├── requirements.txt
├── README.md
│
├── WEBSITE/                    # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                   # User authentication and profiles
│   ├── models.py              # Custom User, EmployerProfile, JobSeekerProfile
│   ├── forms.py               # Authentication and profile forms
│   ├── views.py               # Auth views and role-based routing
│   ├── urls.py
│   ├── permissions.py         # Role-based access decorators
│   ├── admin.py
│   └── templates/accounts/
│
├── jobs/                       # Job posting and application management
│   ├── models.py              # Job and JobApplication models
│   ├── forms.py               # Job creation and application forms
│   ├── views.py               # Job CRUD and application logic
│   ├── urls.py
│   ├── admin.py               # Admin approval workflow
│   └── templates/jobs/
│
├── predictions/                # ML prediction interface
│   ├── forms.py               # Prediction input forms
│   ├── views.py               # Prediction request handlers
│   ├── urls.py
│   └── templates/predictions/
│
├── analytics/                  # Business intelligence integration
│   ├── views.py               # Power BI dashboard embedding
│   ├── urls.py
│   └── templates/analytics/
│
├── ml_models/                  # Machine learning layer
│   ├── models/                # Trained .pkl model files
│   ├── models_loader.py       # Model initialization
│   ├── preprocessing.py       # Feature engineering
│   ├── validators.py          # Input validation
│   ├── utils.py               # Helper functions
│   └── predictors/            # Individual prediction modules
│       ├── salary_predictor.py
│       ├── job_title_predictor.py
│       ├── remote_work_predictor.py
│       ├── degree_predictor.py
│       ├── benefits_predictor.py
│       ├── company_growth_predictor.py
│       ├── revenue_growth_predictor.py
│       └── campaign_conversion_predictor.py
│
├── templates/                  # Global templates
│   ├── base.html
│   ├── navbar.html
│   ├── footer.html
│   ├── home.html
│   └── errors/
│       ├── 403.html
│       └── 404.html
│
└── static/                     # Static assets
    ├── css/
    ├── js/
    └── images/
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd WEBSITE
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the WEBSITE directory:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Machine Learning Models

The platform requires trained ML models to be placed in `ml_models/models/` directory:

- `salary_model.pkl` - Salary prediction model
- `job_title_model.pkl` - Job title recommendation model
- `remote_work_model.pkl` - Remote work eligibility classifier
- `degree_model.pkl` - Degree requirement predictor
- `benefits_model.pkl` - Benefits package predictor
- `company_growth_model.pkl` - Company growth forecaster
- `revenue_growth_model.pkl` - Revenue growth predictor
- `campaign_conversion_model.pkl` - Campaign conversion rate predictor

**Note**: Models must be trained separately using scikit-learn and saved as pickle files.

## Usage

### For Job Seekers
1. Sign up with role "Job Seeker"
2. Complete your profile with skills and experience
3. Browse available jobs or use ML predictions for career insights
4. Apply for jobs and track application status

### For Employers
1. Sign up with role "Employer"
2. Complete company profile
3. Post job listings (requires admin approval)
4. Manage applications from job seekers
5. Access ML predictions for business insights

### For Administrators
1. Log in to admin panel
2. Approve/reject job postings
3. Manage users and profiles
4. Monitor platform activity

## Configuration

### Settings

Key settings in `WEBSITE/settings.py`:
- `AUTH_USER_MODEL = 'accounts.User'` - Custom user model
- `TEMPLATES['DIRS']` - Template directories
- `STATIC_URL` and `MEDIA_URL` - Static and media file paths

### URL Patterns
- `/` - Home page
- `/accounts/` - Authentication and profiles
- `/jobs/` - Job listings and applications
- `/predictions/` - ML prediction interfaces
- `/analytics/` - Analytics dashboard
- `/admin/` - Django admin panel

## Development

### Running Tests
```bash
python manage.py test
```

### Creating New Apps
```bash
python manage.py startapp app_name
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Deployment

### Production Checklist
1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS`
3. Use environment variables for sensitive data
4. Set up a production database (PostgreSQL recommended)
5. Configure static file serving (WhiteNoise or CDN)
6. Use a production server (Gunicorn + Nginx)
7. Enable HTTPS
8. Set up regular backups
9. Configure logging

### Example Gunicorn Command
```bash
gunicorn WEBSITE.wsgi:application --bind 0.0.0.0:8000
```

## Technologies Used

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **ML Framework**: scikit-learn, pandas, numpy
- **Authentication**: Django built-in auth with custom user model
- **Analytics**: Power BI (embedded)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes.

## Support

For issues or questions:
- Create an issue in the repository
- Contact: info@jobmlplatform.com

## Acknowledgments

- Django documentation
- Bootstrap documentation
- scikit-learn documentation
- Power BI documentation
