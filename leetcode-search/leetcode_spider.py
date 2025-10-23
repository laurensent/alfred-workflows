import json
import os
import urllib.request
import urllib.parse
import urllib.error
from cache_manager import CacheManager
from utils import get_data_dir, save_json_file


class LeetCodeSpider:
    def __init__(self):
        self.url = "https://leetcode.cn/graphql/"
        self.data_dir = get_data_dir()
        self.result_file = self.data_dir / 'result.json'
        self.cache_manager = CacheManager()

    def fetch_problems(self):
        problemset = []
        skip = 0
        limit = 100
        print("Fetching problems...")

        try:
            while True:
                payload = json.dumps({
                    "query": "query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {problemsetQuestionList(categorySlug: $categorySlug limit: $limit skip: $skip filters: $filters ) {hasMore total questions {difficulty frontendQuestionId paidOnly title titleCn titleSlug }}} ",
                    "variables": {
                        "categorySlug": "all-code-essentials",
                        "skip": skip,
                        "limit": limit
                    },
                    "operationName": "problemsetQuestionList"
                })

                req = urllib.request.Request(
                    self.url,
                    data=payload.encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req, timeout=30)

                data = json.loads(response.read().decode('utf-8'))
                questions = data['data']['problemsetQuestionList']['questions']
                hasMore = data['data']['problemsetQuestionList']['hasMore']
                total = data['data']['problemsetQuestionList']['total']

                problemset.extend(questions)
                print(f"Fetched {len(questions)} problems, progress: {skip + len(questions)}/{total}")

                if not hasMore or len(questions) == 0:
                    break
                skip += limit

        except Exception as e:
            raise Exception(f"Network request failed: {str(e)}")

        return problemset

    def process_problems(self, problemset):
        result = []
        difficulty_map = {'EASY': 'Easy', 'MEDIUM': 'Medium', 'HARD': 'Hard'}

        for item in problemset:
            try:
                data = {
                    "arg": item['titleSlug'],
                    "titleUS": f"{item['frontendQuestionId']} {str(item['title'])}",
                    "titleCN": f"{item['frontendQuestionId']} {str(item['titleCn'])}",
                    "subtitleUS": f"{item['difficulty'].title()}",
                    "subtitleCN": f"{difficulty_map[item['difficulty']]} {item['title']}"
                }
                if item['paidOnly']:
                    data['subtitleCN'] = '💰 ' + data['subtitleCN']
                    data['subtitleUS'] = '💰 ' + data['subtitleUS']
                result.append(data)
            except KeyError as e:
                print(f"Failed to process problem: {item.get('frontendQuestionId', 'unknown')}, error: {e}")
                continue
        return result

    def update_problems(self):
        try:
            self.cache_manager.update_cache_info(status='updating')
            problemset = self.fetch_problems()
            print(f"Fetched {len(problemset)} problems in total")

            processed_problems = self.process_problems(problemset)
            print(f"Processed {len(processed_problems)} problems successfully")

            if not save_json_file(self.result_file, processed_problems):
                raise Exception("Failed to save problem data")

            self.cache_manager.update_cache_info(total_problems=len(processed_problems), status='success')
            print(f"✅ Problem data updated successfully, total {len(processed_problems)} problems")
            return True

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Update failed: {error_msg}")
            self.cache_manager.update_cache_info(status='error', error_message=error_msg)
            return False


def main():
    spider = LeetCodeSpider()
    success = spider.update_problems()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
