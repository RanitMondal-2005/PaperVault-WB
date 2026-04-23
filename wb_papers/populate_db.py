import os
import django

def populate():
    from colleges.models import College, Stream

    colleges_data = [
        {'name': 'Maulana Abul Kalam Azad University of Tech (MAKAUT)', 'slug': 'makaut-main', 'uni': 'MAKAUT'},
        {'name': 'JIS University', 'slug': 'jis-uni', 'uni': 'AUTONOMOUS'},
        {'name': 'Jadavpur University', 'slug': 'ju', 'uni': 'JU'},
        {'name': 'Kalyani Government Engineering College', 'slug': 'kgec', 'uni': 'MAKAUT'},
        {'name': 'Heritage Institute of Technology', 'slug': 'hitk', 'uni': 'AUTONOMOUS'},
        {'name': 'Institute of Engineering and Management', 'slug': 'iem', 'uni': 'AUTONOMOUS'},
        {'name': 'Techno Main Salt Lake', 'slug': 'tiu', 'uni': 'MAKAUT'},
        {'name': 'University of Calcutta', 'slug': 'cu', 'uni': 'CU'},
        {'name': 'Adamas University', 'slug': 'adamas', 'uni': 'AUTONOMOUS'},

    ]

    streams = [
        'Computer Science & Engineering',
        'Information Technology',
        'Electronics & Communication Engineering',
        'Mechanical Engineering',
        'Electrical Engineering',
        'Civil Engineering',
        'Chemical Engineering',
        'Aerospace Engineering',
        'Electrical and Electronics Engineering',
        'Biotechnology',
        'Data Science(DS)',
        'Artificial Intelligence (AI/ML)',
    ]

    for c_data in colleges_data:
        college, created = College.objects.get_or_create(
            slug=c_data['slug'],
            defaults={'name': c_data['name'], 'university': c_data['uni']}
        )
        if created:
            print(f"Added: {college.name}")
            for s_name in streams:
                Stream.objects.get_or_create(college=college, name=s_name)
        else:
            college.name = c_data['name']
            college.university = c_data['uni']
            college.save()
            print(f"Updated: {college.name}")

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wb_papers.settings')
    django.setup()
    populate()
    print("Database Population Complete.")