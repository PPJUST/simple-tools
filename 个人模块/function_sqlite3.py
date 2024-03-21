"""
更新日期：
2024.01.07

功能：
sqlite3的封装
"""
import sqlite3
from typing import Union


class SQLiteDB:
    """
    sqlite3 数据库方法简单封装
    :param file_db: str类型，数据库文件名
    """

    class ConditionList:
        """
        sqlite3条件列表，WHERE 语句的容器
        支持的逻辑运算符: =, >, <, LIKE, NOT...
        字符串值需要额外添加引号"防止报错
        """

        def __init__(self, conj: str = 'add'):
            """
            :param conj: str类型，'add' 表示且，'or' 表示或
            """
            super().__init__()
            self.conj = conj
            self.rules = []

        def add(self, *, column: str, logical_operator: str, value: any):
            """
            添加条件
            :param column: str类型，列名
            :param logical_operator: str类型，逻辑运算符: =, >, <, LIKE, NOT...
            :param value: 任意类型，列对应的值
            """
            rule = f'{column} {logical_operator} "{value}"'
            self.rules.append(rule)

        def get_sql_condition(self):
            """获取sqlite3条件语句"""
            sql_condition = ' WHERE ' + f' {self.conj.upper()} '.join(self.rules)
            return sql_condition

    class OrderDict(dict):
        """
        sqlite3排序字典
        key为列名，value为升序 'ASC'/ 降序 'DESC'
        """

        def __init__(self):
            super().__init__()

        def get_sql_order(self):
            """获取sqlite3排序语句"""
            sql_order = ', '.join([f'{key} {value}' for key, value in self.items()])
            sql_order += ' ORDER BY '

            return sql_order

    def __init__(self, file_db: str = None):
        # 规范文件名
        if file_db:
            if file_db[-3:].lower() != '.db':
                file_db = file_db + '.db'
        else:
            file_db = 'database.db'

        self._conn = sqlite3.connect(file_db)
        self._cur = self._conn.cursor()

    @staticmethod
    def _convert_columns_datatype(columns_datatype: dict, primary_key: str = None) -> dict:
        """
        转换列名-数据类型对应字典
        :param columns_datatype: dict类型，key为列名，value为对应的数据类型
        :param primary_key: str类型，数据表的主键，默认无
        :return: dict类型，原始字典转换数据类型后的字典
        """
        # python的数据类型与sqlite数据库类型对应关系
        convert_dict = {None: 'NULL', int: 'INTEGER', float: 'REAL', str: 'TEXT', bytes: 'BLOB'}

        convert_column_dict = {}
        for column, datatype in columns_datatype.items():
            convert_datatype = convert_dict[datatype]
            convert_column_dict[column] = convert_datatype

        # 插入主键文本
        if primary_key in convert_column_dict:
            convert_column_dict[primary_key] = f'{convert_column_dict[primary_key]} Primary KEY'

        return convert_column_dict

    @staticmethod
    def _get_sql_col_type(columns_datatype: dict):
        """获取列名-数据类型的sql字段"""
        sql_col_type = ', '.join([f"{column} {datatype}" for column, datatype in columns_datatype.items()])

        return sql_col_type

    def create_table(self, table_name: str, columns_datatype: dict, primary_key: str = None):
        """
        创建数据表（自动忽略重复表）
        :param table_name: str类型，数据表名称
        :param columns_datatype: dict类型，key为列名，value为对应的数据类型
        :param primary_key: str类型，数据表的主键，默认无
        """
        # 将列名与数据类型的格式转换为sqlite支持的格式
        columns_datatype_converted = self._convert_columns_datatype(columns_datatype, primary_key)
        sql_col_type = self._get_sql_col_type(columns_datatype_converted)

        # 执行语句，使用'IF NOT EXISTS' 防止存在同名表时报错
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({sql_col_type})"
        print(f'创建数据表sql: {sql}')
        self._cur.execute(sql)
        self._conn.commit()

    def insert_record_single(self, table_name: str, columns_value: dict):
        """
        在数据表中插入单行数据（自动忽略重复值）
        :param table_name: str类型，需要插入数据的数据表名称
        :param columns_value: dict类型，key为列名，value为对应的值
        """
        # 将列名与值的格式转换为sqlite支持的格式
        sql_column = ', '.join([column for column in columns_value.keys()])
        # 对于值的处理，需要都转为字符串，并且引号用"（Windows文件名可以用'而不能用"，用"来定义字符串防止报错）
        sql_value = ", ".join([f'"{value}"' for value in columns_value.values()])

        # 执行语句，使用'OR IGNORE' 来避免插入重复数据
        sql = f'INSERT OR IGNORE INTO {table_name} ({sql_column}) VALUES ({sql_value})'
        print(f'插入记录sql: {sql}')
        self._cur.execute(sql)
        self._conn.commit()

    def update_record(self, table_name: str, columns_value: dict, condition_list: ConditionList = None):
        """
        在数据表中更新行项目数据
        :param table_name: str类型，需要插入数据的数据表名称
        :param columns_value: dict类型，key为列名，value为对应的值
        :param condition_list: 自定义ConditionList类型，筛选条件
        """
        # 将列名与值的格式转换为sqlite支持的格式
        # 引号用"（Windows文件名可以用'而不能用"，用"来定义字符串防止报错）
        sql_col_value = ', '.join([f'{column} = "{value}"' for column, value in columns_value.items()])

        # 组合完整语句
        sql = f"UPDATE {table_name} SET {sql_col_value}"
        if condition_list:
            sql += condition_list.get_sql_condition()
        print(f'更新记录sql: {sql}')
        self._cur.execute(sql)
        self._conn.commit()

    def delete_record(self, table_name: str, condition_list: ConditionList = None):
        """
        在数据表中删除行项目数据
        :param table_name: str类型，需要插入数据的数据表名称
        :param condition_list: 自定义ConditionList类型，筛选条件
        """
        sql = f"DELETE FROM {table_name}"
        if condition_list:
            sql += condition_list.get_sql_condition()
        print(f'删除记录sql: {sql}')
        self._cur.execute(sql)
        self._conn.commit()

    def select_record(self, table_name: str, columns: Union[str, list] = '*', return_format: str = 'dict',
                      condition_list: ConditionList = None, order_dict: OrderDict = None) -> list:
        """
        在数据表查询行项目数据
        :param table_name: str类型，需要插入数据的数据表名称
        :param columns: str或list类型，需要查询的列名，默认为查询全部列
        :param return_format: str类型，返回数据的类型，tuple或dict
        :param condition_list: 自定义ConditionList类型，筛选条件
        :param order_dict: 自定义OrderDict类型，排序条件
        """
        # 组合语句
        if type(columns) is str:
            columns = [columns]
        sql = f'SELECT {", ".join(columns)} FROM {table_name}'

        if condition_list:
            sql += condition_list.get_sql_condition()

        if order_dict:
            sql += order_dict.get_sql_order()
        print(f'查询记录sql: {sql}')

        # 取得返回结果
        data = self._cur.execute(sql)
        columns_name = [i[0] for i in data.description]  # 列名
        original_data = data.fetchall()  # 原始格式为[(每行列值组成的元组), (a1_1,a1_2,a1_3), ...]

        # 调整返回结果的格式
        if return_format == 'tuple':
            return original_data
        else:
            return [dict(zip(columns_name, row)) for row in original_data]  # [{列名:列值...}...]

    def insert_column(self, table_name: str, columns_datatype: dict):
        """
        在数据表中插入新的列
        :param table_name: str类型，数据表名称
        :param columns_datatype: dict类型，key为列名，value为对应的数据类型
        """
        # 将列名与数据类型的格式转换为sqlite支持的格式
        columns_datatype_converted = self._convert_columns_datatype(columns_datatype)
        sql_col_type = self._get_sql_col_type(columns_datatype_converted)

        # 组合语句
        sql = f"ALTER TABLE {table_name} ADD COLUMN {sql_col_type}"
        print(f'插入新列sql: {sql}')
        self._cur.execute(sql)
        self._conn.commit()

    def copy_table(self, original_table_names: str, new_table_name: str):
        """
        复制数据表
        :param original_table_names: str类型，被复制的数据表名称
        :param new_table_name: str类型，新的数据表名称
        """
        # 复制数据表的列名
        sql_frame = f"CREATE TABLE {new_table_name} AS SELECT * FROM {original_table_names} WHERE 0"
        self._cur.execute(sql_frame)
        # 复制数据表的行项目
        sql_record = f"INSERT INTO {new_table_name} SELECT * FROM {original_table_names}"
        self._cur.execute(sql_record)

        self._conn.commit()

    def is_table_exist(self, table_name: str):
        """
        检查数据库中是否存在某个数据表
        :param table_name: str类型，数据表名称
        """
        sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        self._cur.execute(sql)
        if self._cur.fetchone() is not None:
            return True
        else:
            return False

    def get_all_table_name(self):
        """返回数据库中的所有的数据表名称"""
        sql = f"SELECT name FROM sqlite_master WHERE type='table'"
        self._cur.execute(sql)

        return self._cur.fetchone()

    def count_table(self, table_name: str) -> int:
        """
        查询数据表中的行项目个数
        :param table_name: str类型，数据表名称
        """
        sql = f"SELECT COUNT(*) FROM {table_name};"
        self._cur.execute(sql)
        count = self._cur.fetchone()[0]

        return count

    def close(self):
        """关闭数据库连接"""
        self._conn.close()
