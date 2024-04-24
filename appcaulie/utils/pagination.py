"""
自定义分页组件
以后如果要使用的话：
1. 先筛选数据：
rowdatalist = models.PrettyNum.objects.all()
2. 实例化分页对象
from appcaulie.utils.pagination import Pagination
page_object = Pagination(request, rowdatalist)
context = {
    'datalist': page_object.page_queryset,
    'page_string': page.object.html()
}
return render(request, './pretty_list.html', context)
3. 前端页面中
<ul class="pagination">
    {{ page_string }}
</ul>
"""
from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_param='page', page_size=10, plus=5):
        """
        :param request: 请求对象
        :param queryset: 筛选出来的符合条件的数据
        :param page_param: 从url中获得的get数据，代表第几页
        :param page_size: 每页显示多少条数据
        :param plus: 当前页面前后分别有多少个页码
        """
        import copy
        query_dic = copy.deepcopy(request.GET)
        query_dic._mutable = True
        self.query_dic = query_dic

        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        self.page_param = page_param

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()

        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = []
        # 首页
        self.query_dic.setlist(self.page_param, [1])
        page_str_list.append(f'<li class="page-item"><a class="page-link" href="?{self.query_dic.urlencode()}">first</a></li>')
        # 上一页
        if self.page > 1:
            self.query_dic.setlist(self.page_param, [self.page - 1])
            prev = f'<li class="page-item"><a class="page-link" href="?{self.query_dic.urlencode()}">prev</a></li>'
        else:
            self.query_dic.setlist(self.page_param, [1])
            prev = f'<li class="page-item"><a class="page-link" href="?{self.query_dic.urlencode()}">next</a></li>'
        page_str_list.append(prev)
        # 一页一页
        for i in range(start_page, end_page + 1):
            if i == self.page:
                self.query_dic.setlist(self.page_param, [i])
                ele = f'<li class="page-item active"><a class="page-link" href="?{self.query_dic.urlencode()}">{i}</a></li>'
            else:
                self.query_dic.setlist(self.page_param, [i])
                ele = f'<li class="page-item"><a class="page-link" href="?{self.query_dic.urlencode()}">{i}</a></li>'
            page_str_list.append(ele)
        # 下一页
        if self.page < self.total_page_count:
            self.query_dic.setlist(self.page_param, [self.page + 1])
            nex = f'<li class="page-item"><a class="page-link" href="?{self.query_dic.urlencode()}">next</a></li>'
        else:
            self.query_dic.setlist(self.page_param, [self.total_page_count])
            nex = f'<li class="page-item"><a class="page-link" href="?{self.query_dic.urlencode()}">next</a></li>'
        page_str_list.append(nex)
        # 尾页
        self.query_dic.setlist(self.page_param, [self.total_page_count])
        page_str_list.append(f'<li class="page-item"><a class="page-link" href="?{self.query_dic.urlencode()}">last</a></li>')

        search_str = """
            <br>
            <div class="input-group mb-3" style="width: 200px">
                <form method="get">
                    <input type="text" class="form-control" placeholder="Recipient's username" aria-label="Recipient's username" aria-describedby="button-addon2" name="page" placeholder="输入页码">
                    <input class="btn btn-outline-secondary" type="submit" id="button-addon2" value="跳转">
                </form>
            </div>
        """
        # page_str_list.append(search_str)
        page_string = mark_safe(''.join(page_str_list))
        return page_string