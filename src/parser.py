"""Parser functions for Hirist data."""
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from datetime import datetime


def parse_html_description(html_text: str) -> str:
    """Extract clean text from HTML job description."""
    if not html_text:
        return ""
    
    try:
        soup = BeautifulSoup(html_text, 'lxml')
        
        # Remove scripts and styles
        for tag in soup(['script', 'style']):
            tag.decompose()
        
        # Get text
        text = soup.get_text(separator='\n')
        
        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]
        
        return '\n'.join(lines)
    except Exception:
        return html_text


def parse_job_listing(job_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse job listing from API response."""
    company_data = job_data.get('companyData', {}) or {}
    ambition_box = company_data.get('ambitionBoxInfo', {}) or {}
    
    # Parse skills/tags
    skills = []
    for tag in job_data.get('tags', []) or []:
        if tag and isinstance(tag, dict):
            skills.append({
                'name': tag.get('name', ''),
                'mandatory': tag.get('isMandatory', False)
            })
    
    # Parse locations
    locations = []
    for loc in job_data.get('locations', []) or []:
        if loc and isinstance(loc, dict):
            locations.append(loc.get('name', ''))
    
    # Parse timestamps
    created_ms = job_data.get('createdTimeMs')
    posted_date = None
    if created_ms:
        try:
            posted_date = datetime.fromtimestamp(created_ms / 1000).isoformat()
        except (ValueError, OverflowError, OSError):
            posted_date = None
    
    salary_min = job_data.get('minSal', 0) or 0
    salary_max = job_data.get('maxSal', 0) or 0
    salary_hidden = bool(job_data.get('hideSal', 1))
    
    job_id = job_data.get('id')
    job_url = f"https://www.hirist.tech/j/-{job_id}" if job_id else None
    
    return {
        'jobId': job_id,
        'title': job_data.get('title', ''),
        'url': job_url,
        'company': {
            'name': company_data.get('companyName', ''),
            'logo': company_data.get('companyLogoFilePath', ''),
            'rating': ambition_box.get('aggregateRating'),
            'reviews': ambition_box.get('reviewsCount'),
        },
        'experience': {
            'min': job_data.get('min'),
            'max': job_data.get('max')
        },
        'salary': {
            'min': salary_min,
            'max': salary_max,
            'hidden': salary_hidden,
            'currency': 'INR'
        },
        'location': locations,
        'skills': skills,
        'metadata': {
            'posted': posted_date,
            'premium': bool(job_data.get('premium', 0)),
            'workFromHome': bool(job_data.get('workFromHome', 0)),
            'confidential': bool(job_data.get('confidential', 0)),
            'diversityHiring': {
                'femaleCandidate': bool(job_data.get('femaleCandidate', 0)),
                'differentlyAbled': bool(job_data.get('differentlyAbled', 0)),
                'exDefence': bool(job_data.get('exDefence', 0))
            }
        },
        'scrapedAt': datetime.now().isoformat()
    }


def enrich_with_detail(parsed_job: Dict[str, Any], detail_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich job with detail data."""
    if not detail_data:
        return parsed_job
    
    # Parse description
    intro_html = detail_data.get('introText', '')
    parsed_job['description'] = {
        'html': intro_html,
        'text': parse_html_description(intro_html)
    }
    
    # Add recruiter info
    recruiter = detail_data.get('recruiter', {}) or {}
    if recruiter:
        parsed_job['recruiter'] = {
            'name': recruiter.get('recruiterName'),
            'title': recruiter.get('designation'),
            'lastActive': recruiter.get('lastActive')
        }
    
    # Add view/application counts
    if 'metadata' in parsed_job:
        parsed_job['metadata']['views'] = detail_data.get('hits')
        parsed_job['metadata']['applications'] = detail_data.get('applyCount')
        parsed_job['metadata']['category'] = detail_data.get('categoryId')
    
    # Enhanced company info from detail
    company_data = detail_data.get('companyData', {}) or {}
    ambition_box = company_data.get('ambitionBoxInfo', {}) or {}
    
    if ambition_box and 'company' in parsed_job:
        parsed_job['company']['about'] = ambition_box.get('aboutCompany')
        parsed_job['company']['founded'] = ambition_box.get('foundedYear')
        parsed_job['company']['employees'] = ambition_box.get('totalEmployeesIndia')
        parsed_job['company']['headquarters'] = ambition_box.get('hq')
        parsed_job['company']['industry'] = ambition_box.get('primaryIndustry')
    
    return parsed_job
