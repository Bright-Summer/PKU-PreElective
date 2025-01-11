import sys, os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import seaborn as sns

from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel

import ui.Ui_form_main as form_main

class CourseSortFilterProxyModel(QSortFilterProxyModel):       #课程过滤器
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_criteria = []
        self.part_criteria = []

    def set_filter_criteria(self, criteria):
        """
        设置完全匹配过滤条件
        :param criteria: 列表，每个元素是一个元组 (column, value, bool), bool为True表示白名单, False表示黑名单
        """
        self.filter_criteria = criteria
        self.invalidateFilter()

    def set_part_criteria(self, criteria):
        """
        设置部分匹配过滤条件
        :param criteria: 列表，每个元素是一个元组 (column, value, bool), bool为True表示白名单, False表示黑名单
        """
        self.part_criteria = criteria
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        """
        重写 filterAcceptsRow 方法以根据多个列的信息进行筛选
        """
        for column, value, bw in self.filter_criteria:
            item_text = course_data.loc[source_row, column]
            if (item_text == value) ^ bw:
                return False
        for column, value, bw in self.part_criteria:
            item_text = course_data.loc[source_row, column]
            if (value in item_text) ^ bw:
                return False
        return True

def refreshCourse(changed=True):        #更新课程过滤器规则、参数为True则更新学分、冲突选课、课程表
    full_criteria = []
    for index, row in selected_data.iterrows():      #更新过滤器
        full_criteria.append(('序号', row['序号'], False))
    course_proxy.set_filter_criteria(full_criteria)
    global ui
    part_criteria = [('课程名称', ui.CourseNameEdit.text(), True),
                     ('开课单位', ui.CollegeEdit.text(), True),
                     ('课程类型', ui.TypeEdit.text(), True)]
    course_proxy.set_part_criteria(part_criteria)
    ui.CourseTable.resizeColumnsToContents()

    if changed:
        selected_data.to_csv('./data/selected.csv', index=False)
        global timetable_data
        ui.CreditLabel.setText("当前总学分：" + str(sum(map(int, selected_data["学分"]))))
        timetable_data = pd.DataFrame(index=classtime, columns=week)

        for index, row in selected_data.iterrows():                    #更新课程表
            if not isinstance(row['上课时间'], str):
                continue
            info = list(s for s in reversed(row['上课时间'].replace(')', '(').replace(' ', '').split('(')) if s)
            while info:
                singledouble = [0, 1]     #0单周，1双周
                w = info.pop()            #星期
                t_start, t_end = map(timetable_data.index.get_loc, info.pop().split('-'))       #第几节
                if info and info[-1] in '单双':
                    singledouble = [(info.pop() == '双')]
                for t in range(t_start, t_end+1):
                    if not isinstance(timetable_data.loc[classtime[t], w], list):
                        timetable_data.loc[classtime[t], w] = [[],[]]
                    for sd in singledouble:
                        timetable_data.loc[classtime[t], w][sd].append(row['课程名称'])
        plotTable()

        crash = []                                                #更新课程冲突
        for index, row in timetable_data.iterrows():
            for cell in row:
                if isinstance(cell, list):
                    for subcell in cell:
                        if len(subcell) > 1 and tuple(subcell) not in crash:
                            crash.append(tuple(subcell))
        ui.CrashLabel.setText('\n'.join(map(str, crash)))

def loadData(model, df):     #把DataFrame数据传给QTableView的model
        model.clear()

        # 设置表头
        headers = list(df.columns)
        model.setHorizontalHeaderLabels(headers)

        # 填充数据
        for row in range(len(df)):
            items = []
            for column in range(len(df.columns)):
                item = QStandardItem(str(df.iat[row, column]))
                items.append(item)
            model.appendRow(items)

def selectCourse(elem):      #预选课程
    if elem.isValid():
        index = int(course_proxy.data(course_proxy.index(elem.row(), 0), Qt.DisplayRole))-1
        global selected_data
        selected_data = pd.concat([selected_data, course_data.iloc[index].to_frame().T], ignore_index=True)
        loadData(selected_model, selected_data)
        ui.SelectedTable.setColumnHidden(list(selected_data).index('序号'), True)
        ui.SelectedTable.resizeColumnsToContents()
        refreshCourse()

def unselectCourse(elem):    #取消预选
    if elem.isValid():
        global selected_data
        selected_data = selected_data.drop(elem.row()).reset_index(drop=True)
        loadData(selected_model, selected_data)
        ui.SelectedTable.setColumnHidden(list(selected_data).index('序号'), True)
        ui.SelectedTable.resizeColumnsToContents()
        refreshCourse()

def disableColumn():
    for col in ['课程号', '班号', '起止周']:
        for table in [ui.CourseTable, ui.SelectedTable]:
            table.setColumnHidden(list(selected_data).index(col), ui.DisableColumn.isChecked())

def plotTable():
    def generateTableElem(data):            #把timetable_data里的元素改成直接绘制的文字
        if isinstance(data, list):
            sido = []
            for cc in data[0]:
                if cc in data[1]:
                    sido.append(cc)
            single = [cc for cc in data[0] if cc not in sido]
            double = [cc for cc in data[1] if cc not in sido]
            return '\n'.join(sido)\
                + (('\n' if sido else '') + '(单)' + '\n(单)'.join(single) if single else '') \
                + (('\n' if sido or single else '') + '(双)' + '\n(双)'.join(double) if double else '') \
                + (' [冲突]' if len(data[0]) > 1 or len(data[1]) > 1 else '')
        else:
            return ''
    
    timetable_figure.clear()
    ax = timetable_figure.add_subplot()
    timetable_figure.subplots_adjust(left = 0)
    tb = timetable_data.apply(lambda x: x.map(generateTableElem))

    ax.axis('tight')
    ax.axis('off')  # 关闭坐标轴

    # 创建表格数据
    cell_text = []
    for index, row in tb.iterrows():
        cell_text.append([row[col] for col in tb.columns])
    # 创建表格
    table = ax.table(cellText=cell_text, colLabels=tb.columns, rowLabels=tb.index,
                      loc='upper left', cellLoc='center')
    # 自定义表格样式
    table.auto_set_font_size(False)
    table.set_fontsize(12)

    # 计算每一列的最大字符宽度，以确定合适的列宽
    max_widths = tb.apply(lambda col: max(0.1, max(max(len(ss) for ss in s.split('\n')) for s in col)/75), axis=0).values
    # 计算每一行的最大字符高度，以确定合适的行高
    max_heights = tb.apply(lambda row: max(0.06, max(s.count('\n')+1 for s in row)/25), axis=1).values
    
    #颜色映射
    nameset = {cname for index, row in tb.iterrows() for cname in row if '[冲突]' not in cname}
    colormap = {cname:cellcolor[i] for i, cname in enumerate(nameset)}
    
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # 表头
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor('steelblue')
            cell.set_height(0.05)  # 表头高度
            cell.set_width(max_widths[j])
        else:
            cell.set_height(max_heights[i-1])  # 设置行高
            if j == -1:  # 时间列
                cell.set_text_props(ha = 'center', weight='bold', color='w')
                cell.set_facecolor('mediumseagreen')
            else:
                cell.set_width(max_widths[j])  # 其他列根据内容宽度调整
                if cname := cell.get_text().get_text():
                    if '[冲突]' in cname:
                        cell.set_facecolor('#D50000')
                        cell.set_text_props(color='w', weight='bold')
                    else:
                        cell.set_facecolor(colormap[cname])

    timetable_canvas.draw_idle()

if __name__ == '__main__':
    course_data = pd.read_csv('./data/course.csv')
    if os.path.exists('./data/selected.csv'):
        selected_data = pd.read_csv('./data/selected.csv')
    else:
        selected_data = pd.DataFrame(columns=course_data.columns)
    week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    classtime = ['第1节', '第2节', '第3节', '第4节', '第5节', '第6节', '第7节', '第8节', '第9节', '第10节', '第11节', '第12节']
    timetable_data = pd.DataFrame(index=classtime, columns=week)
    cellcolor = [[1.0, 0.796, 0.779], [0.8, 0.831, 1.0], [0.73, 1.0, 0.936], [1.0, 0.963, 0.556], [1.0, 0.779, 0.854], [0.93, 0.911, 0.904], [0.556, 0.955, 1.0], [0.963, 0.779, 0.995], [0.866, 1.0, 0.711], [0.862, 0.887, 0.899], [1.0, 0.854, 0.667], [0.868, 0.793, 1.0], [0.739, 0.974, 0.859], [0.946, 0.946, 0.946]]*5
    cellcolor2 = ['lightcyan', 'auqamarine', 'bisque', 'lavenderblush', 'mistyrose', 
                 'lavender', 'xkcd:pale green', 'oldlace', 'xkcd:pale pink', 'lightsalmon',
                 'lightblue', 'auqamarine', 'tan', 'thistle', 'lightgray',
                 'violet', 'yellowgreen', 'gold', 'wheat', 'whitesmoke']*5               #单元格颜色
    plt.rcParams['font.family'] = 'SimHei'                       #字体

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = form_main.Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.setGeometry(100, 100, 2000, 1000)     #初始化窗口

    course_model = QStandardItemModel()             #初始化QTableView控件
    course_proxy = CourseSortFilterProxyModel()
    course_proxy.setSourceModel(course_model)
    course_proxy.setFilterKeyColumn
    loadData(course_model, course_data)
    ui.CourseTable.setModel(course_proxy)
    ui.CourseTable.doubleClicked.connect(selectCourse)

    selected_model = QStandardItemModel()
    loadData(selected_model, selected_data)
    ui.SelectedTable.setModel(selected_model)
    ui.SelectedTable.doubleClicked.connect(unselectCourse)
    for table in [ui.CourseTable, ui.SelectedTable]:
        table.resizeColumnsToContents()
        table.setColumnHidden(list(selected_data).index('序号'), True)

    ui.DisableColumn.stateChanged.connect(disableColumn)

    ui.CourseNameEdit.textChanged.connect(lambda:refreshCourse(False))      #初始化LineEdit
    ui.TypeEdit.textChanged.connect(lambda:refreshCourse(False))
    ui.CollegeEdit.textChanged.connect(lambda:refreshCourse(False))

    timetable_figure = plt.figure()                         #初始化课程表
    timetable_figure.set_tight_layout(True)
    timetable_canvas = FigureCanvas(timetable_figure)
    timetable_canvas.setFixedSize(1200,600)
    ui.ScrollFig.setWidget(timetable_canvas)
    timetable_toolbar = NavigationToolbar(timetable_canvas)
    ui.TimeTableLayout.insertWidget(0, timetable_toolbar)

    refreshCourse()
    
    MainWindow.show()
    sys.exit(app.exec_())