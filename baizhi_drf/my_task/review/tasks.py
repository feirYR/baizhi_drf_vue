from django_redis import get_redis_connection
from rest_framework.response import Response

from baizhi_drf.util.send_msg import SMSSend
from my_task.main import app



@app.task(name='commit_review')
def commit_review(course_id, review, pipeline):
    # redis_connection = get_redis_connection('review')
    # pipeline = redis_connection.pipeline()

    print('发表评论')
    return  '发表评论'

# @app.task(name='show_review')
# def show_review(course_id):
#     redis_connection = get_redis_connection('review')
#     result = redis_connection.lrange('review_%s' % course_id, 0, -1)
#     print(11111111)
#     print(result)
#     # return '获取评论成功'
#     # return Response({'message': '获取评论成功', 'review': result.get()})
#     # return Response({'message': '获取评论成功', 'review': result})
#     return result


# @app.task(name='send_sms')
# def send_sms(phone, code):
#     sms = SMSSend('ad7362d2880d845592b1fcd591399eb9')
#     status=sms.send_msg(phone, code)
#     if status:
#         return '发送成功'
#     return '发送失败'