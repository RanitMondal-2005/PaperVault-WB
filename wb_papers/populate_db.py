import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wb_papers.settings')
django.setup()

from colleges.models import College, Stream

def populate():
    colleges_data = [
        {'name': 'Maulana Abul Kalam Azad University of Tech (MAKAUT)', 'slug': 'makaut-main', 'uni': 'MAKAUT'},
        {'name': 'JIS University', 'slug': 'jis-uni', 'uni': 'AUTONOMOUS'},
        {'name': 'Jadavpur University', 'slug': 'ju', 'uni': 'JU'},
        {'name': 'Kalyani Government Engineering College', 'slug': 'kgec', 'uni': 'MAKAUT'},
        {'name': 'Heritage Institute of Technology', 'slug': 'hitk', 'uni': 'AUTONOMOUS'},
        {'name': 'Institute of Engineering and Management', 'slug': 'iem', 'uni': 'AUTONOMOUS'}, 
    ]

    streams = [
        'Computer Science & Engineering', 
        'Information Technology', 
        'Electronics & Communication Engineering', 
        'Mechanical Engineering', 
        'Electrical Engineering'
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
            college.university = c_data['uni']
            college.save()
            print(f"Updated: {college.name}")

if __name__ == '__main__':
    populate()
    print("Database Population Complete.")