from crawler.review_crawler import ReviewCrawler
from crawler.blog_crawler import BlogCrawler
import time



if __name__ == "__main__":
    # start_time = time.time()
    #
    # app = ReviewCrawler()
    # app.get_reviews()
    #
    # # 종료 시간 기록
    # end_time = time.time()
    # # 총 실행 시간 계산
    # total_time = end_time - start_time
    # print(f"식당 리뷰 크롤링 총 실행 시간: {total_time:.2f} 초")
    # # 672.00 초
    blog_app = BlogCrawler()

    # 시작 시간 기록
    start_time = time.time()

    blog_app.get_blogs()

    # 종료 시간 기록
    end_time = time.time()
    # 총 실행 시간 계산
    total_time = end_time - start_time
    print(f"블로그 크롤링 실행 시간: {total_time:.2f} 초")
