# Django Project Template

This is a Django-based web application template that provides a solid foundation for building scalable web applications.

## 🚀 Features

- Django-based web application
- User authentication and authorization
- RESTful API support
- Database integration (PostgreSQL recommended)
- Static files handling
- Environment-based settings
- Docker support
- Testing framework

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+
- pip (Python package manager)
- virtualenv or venv
- Git

## 🛠 Installation

1. Clone the repository
```bash
git clone https://github.com/atashyan/cursor-test-repo-2024.git
cd cursor-test-repo-2024
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create superuser (optional)
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

## 🏗 Project Structure

```
project/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── __init__.py
├── static/
└── templates/
```

## 🔧 Configuration

The project uses environment variables for configuration. Copy `.env.example` to `.env` and update the values:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## 🚀 Deployment

Instructions for deploying to various platforms:

### Docker
```bash
docker-compose up --build
```

### Traditional Deployment
1. Set up a production server (e.g., Ubuntu with Nginx)
2. Install required packages
3. Set up a PostgreSQL database
4. Configure Nginx and Gunicorn
5. Set up SSL certificates

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work*

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- Python Community