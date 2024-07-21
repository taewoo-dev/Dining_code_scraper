from typing import Optional


def excute_query(conn, sql: str, *values: Optional[tuple]) -> Optional[list]:
    """
    parameter:
        conn: 연결한 데이터 베이스 객체
        sql: 원하는 쿼리
        values: 쿼리에 전달되는 변수
    """

    with conn.cursor() as cursor:
        cursor.execute(sql, values) # 쿼리 실행

        if sql.strip().upper().startswith("SELECT"): # select의 경우 결과가져와 보여준다
            return cursor.fetchall()
        else: # 나머지의 경우 변경사항을 커밋
            conn.commit()