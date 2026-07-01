# 🏛️ PaperVault WB

> A centralized, verified academic repository for West Bengal university students and faculty.

[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## 📌 About

**PaperVault WB** is a free, open-access academic platform built specifically for students and faculty across West Bengal's engineering and science colleges. It provides a single, organized destination for:

- 📄 Previous year question papers (semester, internal, practical)
- 📚 Study materials (notes, assignments, lab manuals, placement notes)
- 🤖 AI-powered paper analysis and topic extraction

No login required for students. Faculty members can register, get verified, and start contributing.

> Currently serving **12+ institutions** across West Bengal — and growing.

---

## 🌐 Live URL

🔗 **[https://ranitmondal.pythonanywhere.com](https://ranitmondal.pythonanywhere.com)**

---

## ✨ Features

### For Students
- 🔍 Browse and download verified question papers — completely free
- 🎓 Filter by college, stream, semester, year and exam type
- 📚 Access study materials, notes and placement resources
- 🤖 Use the AI Paper Lab to extract topics, get summaries and generate mock tests

### For Faculty
- 📤 Upload question papers and study materials
- ✏️ Edit and manage your own uploads
- 🔒 Verified account system — admin approval before upload access

### AI Paper Lab
- 📊 Topic Extraction — identifies high-priority recurring topics from past papers
- 📝 Smart Summary — exam-focused summaries with probable questions
- 🧪 Mock Test Generator — auto-generates MCQs from past papers
- 📎 PDF Analysis — upload any PDF and get instant AI analysis

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0 (Python 3.14) |
| Frontend | Bootstrap 5.3, Bootstrap Icons |
| Database | SQLite (dev) / upgradeable to PostgreSQL |
| AI Integration | OpenRouter API (LLM — model configurable via ai_utils.py) |
| PDF Processing | PyPDF2 |
| Deployment | PythonAnywhere |

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- pip
- virtualenv (recommended)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/RanitMondal-2005/PaperVault-WB.git
cd PaperVault-WB/wb_papers

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env and add your SECRET_KEY and OPENROUTER_API_KEY

# 5. Run migrations
python manage.py migrate

# 6. Populate database with colleges and streams
python populate_db.py

# 7. Create superuser (for admin access)
python manage.py createsuperuser

# 8. Run the development server
python manage.py runserver
```

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key-here
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

> Get your OpenRouter API key at [openrouter.ai](https://openrouter.ai)

---

## 📁 Project Structure
## 📁 Project Structure

```
PaperVault-WB/
├── wb_papers/          
├── papers/             
├── materials/          
├── colleges/           
├── users/              
├── templates/          
├── static/             
│   ├── css/
│   └── js/
├── media/              
│   └── college_logos/  
├── populate_db.py      
└── .env.example        
```

---

## 🔐 User Roles

| Role | Permissions |
|---|---|
| **Student** | Browse & download papers and materials (no login needed) |
| **Faculty** | Upload papers & materials, edit own uploads (requires verification) |
| **Admin** | Full access, verify faculty accounts, manage all data |

---

## 🤝 Contributing

For faculty members wanting to contribute papers:
1. Register at the platform
2. Wait for admin verification
3. Start uploading verified papers

For code contributions:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push and open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.
> *Anyone can use, copy, modify and distribute this code — for free — as long as they give credit to the original authors.*

---

## 👨‍💻 Authors

**Ranit Mondal**
- GitHub: [@RanitMondal-2005](https://github.com/RanitMondal-2005)

**Biswajit Samanta**
- GitHub: [@Biswajitsamanta1109](https://github.com/Biswajitsamanta1109)

> Built in collaboration as an academic project for West Bengal students.

---

<div align="center">
  <p>🔗 <strong><a href="https://ranitmondal.pythonanywhere.com">Visit PaperVault WB</a></strong></p>
  <p>Built with ❤️ for West Bengal students</p>
  <p><strong>Free forever. Verified always.</strong></p>
</div>