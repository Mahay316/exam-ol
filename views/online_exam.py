from flask import Blueprint

exam_bp = Blueprint('exam_bp', __name__)


@exam_bp.route("/<str:exam_id>")
def get_paper(exam_id: str):
    """
    点击试卷链接后给前端返回试卷
    """
    pass


@exam_bp.route("/get_time")
def get_time():
    """
    前端获取时间进行校对
    """


@exam_bp.route("/cache_each_result")
def cache_each_result():
    """
    用form提交某一题目然后缓存起来，交卷后直接用缓存判卷
    """


def check_paper():
    """
    判卷
    """
