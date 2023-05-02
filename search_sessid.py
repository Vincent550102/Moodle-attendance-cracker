import requests
import asyncio

def make_url(base_url,sessid):
    return f'{base_url}?sessid={sessid}'

def find_sessid(base_url, course_name,lower_bound = 200000,upper_bound = 400000):
    '''
    Given input: course name
    Output: sessid
    
    1. Find the latest session id in the Moodle system. If one requests with too large sessid, 
    Moodle responds, "Can't find data record in database table attendance_sessions." 
    This behavior enables binary search for the latest session id.
    
    2. Perform a backward sequential search on sessid until the responded course name is correct.
    '''

    # Binary search
    lower_bound = lower_bound
    upper_bound = upper_bound
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        r = requests.get(make_url(base_url,mid))
        if 'Can\'t find data record in database table attendance_sessions.' in r.text\
            or '在資料表attendance_sessions中找不到資料記錄。' in r.text:
            upper_bound = mid
        else:
            lower_bound = mid + 1
        print(mid)

    # use run_in_executor to avoid blocking the main thread
    # 10 requests a time
    async def check_course_name(sessid):
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, requests.get, make_url(base_url,sessid))
        r = await future
        if r.status_code == 200:
            if course_name in r.text:
                return sessid
            
    async def seq_search(num_workers = 10):
        tasks = []
        sessid = lower_bound
        while sessid > lower_bound - 100:
            for _ in range(num_workers):
                tasks.append(asyncio.ensure_future(check_course_name(sessid)))
                sessid -= 1
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    return result
            tasks = []

    loop = asyncio.get_event_loop()
    sessid = loop.run_until_complete(seq_search())
    if sessid:
        return sessid
            
    raise Exception('No sessid found. Please check the course name.')