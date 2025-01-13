from bs4 import BeautifulSoup
import json
import os

def parse_job_html(directory, file_path):
    full_path = os.path.join(directory, file_path)
    
    with open(full_path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    job_data = {}
    
    def get_field(soup, field_name):
       try:
           element = soup.find('span', string=field_name)
           if element:
               # cleaning addresses
               if field_name == 'Position Address: ':
                   addr_span = element.find_next('span', {'class': 'smallertext'})
                   return addr_span.text.split('\xa0')[0].strip().replace('\n', '').replace('\u2019', "'").replace('\u2022', '').replace('\t', '').replace('\u2013', '-')
               return element.next_sibling.text.strip().replace('\n', '').replace('\u2019', "'").replace('\u2022', '').replace('\t', '').replace('\u2013', '-')
           return "N/A"
       except:
           return "N/A"

    def get_description_field(soup, field_name):
       try:
           header = soup.find('span', string=field_name)
           if header:
               desc = header.find_next('span', {'class': 'smallertext'})
               if desc:
                   return desc.text.strip().capitalize().replace('\n', '').replace('\t', '')
           return "N/A"
       except:
           return "N/A"
    
    try:
        title_element = soup.find('span', {'class': 'largertext'})
        if title_element:
            title = title_element.text.strip()
        else:
            title_element = soup.find('h1') or soup.find('h2') or soup.find('title')
            title = title_element.text.strip() if title_element else "N/A"
        job_data['title'] = title
    except:
        job_data['title'] = "N/A"
    
    job_data['employer'] = get_field(soup, 'Employer: ')
    job_data['company_description'] = get_description_field(soup, 'Division/Location/Company Description:')
    job_data['position_description'] = get_description_field(soup, 'Position Description:')
    job_data['openings'] = get_field(soup, 'Number of Openings: ')
    job_data['qualifications'] = get_description_field(soup, 'Qualifications:')
    job_data['address'] = get_field(soup, 'Position Address: ')
    job_data['transportation'] = get_field(soup, 'Transportation to work: ')
    job_data['travel_required'] = get_field(soup, 'Travel required for position: ')
    job_data['compensation'] = get_field(soup, 'Compensation Status: ')
    job_data['min_gpa'] = get_field(soup, 'Minimum GPA: ').strip("-").strip()
    job_data['citizenship'] = get_field(soup, 'Citizenship Restriction: ')
    job_data['screening'] = get_field(soup, 'Pre-Employment Screening Requirements: ')
    
    return job_data

def process_all_files(directory):
    all_jobs = {}
    title_counts = {}  

    # handle duplicate job titles
    
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            job_data = parse_job_html(directory, filename)
            base_title = job_data['title']
            
            if base_title == "N/A":
                job_id = f"Unknown Position {len(title_counts.get('N/A', [])) + 1}"
            else:
                if base_title not in title_counts:
                    title_counts[base_title] = 1
                    job_id = base_title
                else:
                    title_counts[base_title] += 1
                    job_id = f"{base_title} {title_counts[base_title]}"
            
            all_jobs[job_id] = job_data
    
    with open('all_jobs.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    process_all_files('job_htmls1/')