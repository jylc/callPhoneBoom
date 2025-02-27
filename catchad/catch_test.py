import unittest

from catchad.catch import baidu_deep_search


class TestCatch(unittest.TestCase):
    def test_baidu_deep_search(self):
        url='https://zx.xywy.com/bangdan/1718302.html'
        keywords=["在线咨询","联系我们","点击咨询"]
        baidu_deep_search(url,keywords)
        pass
    pass

if __name__ == '__main__':
    unittest.main()