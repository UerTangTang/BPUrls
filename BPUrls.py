import requests

def normalize_url(url):
    # 简单的归一化：如果URL以斜杠结尾，则去除它
    if url.endswith('/'):
        return url[:-1]
    return url

def get_status_code(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while accessing {url}: {e}")
        return None

def batch_process_urls_from_file(input_file, output_file):
    # 使用集合来去重并保持URL的首次出现顺序
    seen_urls = set()
    urls_with_status = []

    with open(input_file, 'r') as file:
        for url in file.read().splitlines():
            normalized_url = normalize_url(url)
            if normalized_url not in seen_urls:
                seen_urls.add(normalized_url)
                status_code = get_status_code(normalized_url)
                if status_code == 200:
                    urls_with_status.append((normalized_url, status_code))

    # 将状态码为200的URL写入新文件
    with open(output_file, 'w') as output:
        for url, status in urls_with_status:
            output.write(f"{url}\n")

# 示例txt文件路径（包含URL的列表）
input_file = 'xidian.edu.cn.txt'
# 输出文件路径（保存状态码为200的站点）
output_file = '200_urls.txt'

# 批量处理URL并保存结果
batch_process_urls_from_file(input_file, output_file)
print("Processing completed. Status 200 URLs saved to", output_file)