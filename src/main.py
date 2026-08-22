"""Main scraper logic for Hirist.tech jobs."""
import asyncio
import httpx
from apify import Actor
from .utils import fetch_json
from .parser import parse_job_listing, enrich_with_detail


BASE_API_URL = 'https://gladiator.hirist.tech'

# Category mappings
CATEGORY_MAP = {
    'ai-ml': 14,
    'data-analytics-bi': 7,
    'data-engineering': 15,
    'backend-development': 1,
    'frontend-development': 2,
    'full-stack': 16,
    'mobile-applications': 5,
    'emerging-technologies': 9,
    'devops-sre': 3,
    'cybersecurity': 4,
    'quality-assurance': 6,
    'platform-engineering': 8,
    'product-management': 10,
    'business-analysis': 11,
    'ui-design': 12
}


async def get_job_listings(client: httpx.AsyncClient, category_id: int, page: int = 0, size: int = 50):
    """Fetch job listings for a category page."""
    url = f'{BASE_API_URL}/job/category/'
    params = {
        'page': page,
        'categoryId': category_id,
        'size': size
    }
    
    response = await fetch_json(url, params, client)
    if response and 'data' in response:
        return response['data']
    return []


async def get_job_detail(client: httpx.AsyncClient, job_id: int):
    """Fetch detailed job information."""
    url = f'{BASE_API_URL}/job/detail'
    params = {'jobcode': job_id}
    
    response = await fetch_json(url, params, client)
    if response and 'data' in response:
        return response['data']
    return None


async def scrape_category(client: httpx.AsyncClient, category_id: int, max_results: int, include_description: bool):
    """Scrape all jobs from a category up to max_results."""
    jobs_scraped = 0
    page = 0
    page_size = min(50, max_results)  # API max is typically 50
    
    await Actor.log.info(f'Starting scrape for category {category_id}')
    
    while jobs_scraped < max_results:
        await Actor.log.info(f'Fetching page {page} (size: {page_size})...')
        
        listings = await get_job_listings(client, category_id, page, page_size)
        
        if not listings:
            await Actor.log.info(f'No more jobs found on page {page}')
            break
        
        await Actor.log.info(f'Found {len(listings)} jobs on page {page}')
        
        for job_data in listings:
            if jobs_scraped >= max_results:
                break
            
            try:
                # Parse basic job data
                parsed_job = parse_job_listing(job_data)
                
                # Optionally fetch full description
                if include_description and parsed_job.get('jobId'):
                    job_id = parsed_job['jobId']
                    await Actor.log.debug(f'Fetching details for job {job_id}')
                    
                    detail_data = await get_job_detail(client, job_id)
                    if detail_data:
                        parsed_job = enrich_with_detail(parsed_job, detail_data)
                    
                    # Rate limiting after detail fetch
                    await asyncio.sleep(0.5)
                
                # Push to dataset
                await Actor.push_data(parsed_job)
                jobs_scraped += 1
                
                if jobs_scraped % 10 == 0:
                    await Actor.log.info(f'Scraped {jobs_scraped} jobs so far...')
            
            except Exception as e:
                await Actor.log.error(f'Error processing job: {e}')
                continue
        
        # Check if this was the last page
        if len(listings) < page_size:
            await Actor.log.info('Reached last page of results')
            break
        
        page += 1
        
        # Rate limiting between pages
        await asyncio.sleep(0.3)
    
    return jobs_scraped


async def main():
    """Main actor entry point."""
    async with Actor:
        await Actor.log.info('Hirist Tech Scraper starting...')
        
        # Get input
        actor_input = await Actor.get_input() or {}
        
        # Parse input with defaults
        categories = actor_input.get('categories', []) or []
        if not categories:
            # Default to AI/ML if none specified
            categories = ['ai-ml']
        
        max_results = actor_input.get('maxResults', 50)
        include_description = actor_input.get('includeDescription', True)
        search_query = actor_input.get('searchQuery', '')
        location_filter = actor_input.get('location', '')
        
        # Convert category names to IDs
        category_ids = []
        for cat in categories:
            if isinstance(cat, int):
                category_ids.append(cat)
            elif isinstance(cat, str):
                cat_lower = cat.lower().replace(' ', '-').replace('_', '-')
                if cat_lower in CATEGORY_MAP:
                    category_ids.append(CATEGORY_MAP[cat_lower])
                elif cat.isdigit():
                    category_ids.append(int(cat))
        
        if not category_ids:
            await Actor.log.warning('No valid categories found, defaulting to AI/ML (14)')
            category_ids = [14]
        
        await Actor.log.info(f'Config: categories={category_ids}, maxResults={max_results}, includeDescription={include_description}')
        
        if search_query:
            await Actor.log.warning(f'Search query "{search_query}" specified but not supported by API (filtering in results would reduce dataset)')
        
        if location_filter:
            await Actor.log.warning(f'Location filter "{location_filter}" specified but not supported by API')
        
        # Create HTTP client
        async with httpx.AsyncClient(timeout=30.0) as client:
            total_scraped = 0
            
            # Distribute max_results across categories
            results_per_category = max_results // len(category_ids) if len(category_ids) > 1 else max_results
            
            for category_id in category_ids:
                await Actor.log.info(f'=== Scraping category {category_id} ===')
                
                try:
                    count = await scrape_category(
                        client, 
                        category_id, 
                        results_per_category,
                        include_description
                    )
                    total_scraped += count
                    await Actor.log.info(f'Scraped {count} jobs from category {category_id}')
                
                except Exception as e:
                    await Actor.log.error(f'Error scraping category {category_id}: {e}')
                    continue
        
        await Actor.log.info(f'✅ Scraping complete! Total jobs: {total_scraped}')
        
        # Save task metadata
        await Actor.set_value('SAVED-TASK', {
            'actorId': Actor.get_env().get('actor_id'),
            'actorRunId': Actor.get_env().get('actor_run_id'),
            'defaultDatasetId': Actor.get_env().get('default_dataset_id'),
            'startedAt': Actor.get_env().get('started_at'),
            'input': actor_input,
            'stats': {
                'itemsScraped': total_scraped,
                'categoriesProcessed': len(category_ids)
            }
        })


if __name__ == '__main__':
    asyncio.run(main())
