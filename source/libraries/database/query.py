from datetime import datetime, date, time
from enum import Enum

class QueryLib:

    def __init__(self):
        self._from = ''
        self._group = ''
        self._limit = 0
        self._order = ''
        self._joins = []
        self._offset = 0
        self._wheres = []
        self._having = []
        self._columns = []
        self._function = ''

    def delete(self):
        self._function = 'DELETE'

    def truncate(self):
        self._function = 'TRUNCATE'

    def select(self, parameters = []):
        self._function = 'SELECT'
        if isinstance(parameters, str):
            self._columns.append(parameters)
        if isinstance(parameters, list):
            for parameter in parameters:
                self._columns.append(parameter)

    def table(self, table: str):
        self._from = table

    def left(self, table, where):
        self._joins.append(f"LEFT JOIN {table} ON {where}")

    def right(self, table, where):
        self._joins.append(f"RIGHT JOIN {table} ON {where}")

    def inner(self, table, where):
        self._joins.append(f"INNER JOIN {table} ON {where}")

    def where(self, where: str):
        self._wheres.append(where)

    def order(self, orders):
        if isinstance(orders, str):
            self._order = orders
        if isinstance(orders, list):
            self._order = ', '.join(orders)

    def limit(self, limit: int):
        self._limit = limit

    def offset(self, offset: int):
        self._offset = offset

    def group(self, groups):
        if isinstance(groups, str):
            self._group = groups
        if isinstance(groups, list):
            self._group = ', '.join(groups)

    def quote(self, value) -> str:
        if value is None:
            return 'NULL'
        if isinstance(value, str):
            return f"'{value}'"
        if isinstance(value, int):
            return f"{value}"
        if isinstance(value, bool):
            if value:
                return '1'
            else:
                return '0'
        if isinstance(value, float):
            return f"{value}"
        if isinstance(value, Enum):
            return self.quote(value.value)
        if isinstance(value, date):
            return self.quote(value.timestamp())
        if isinstance(value, time):
            return self.quote(value.timestamp())
        if isinstance(value, datetime):
            return self.quote(value.timestamp())
        if isinstance(value, list):
            result = []
            for v in value:
                result.append(self.quote(v))
            return ', '.join(result)
        return 'NULL'

    def operator_or(self, wheres: list[str]) -> str:
        return '(' + ' OR '.join(wheres) + ')'

    def operator_and(self, wheres: list[str]) -> str:
        return '(' + ' AND '.join(wheres) + ')'

    def assemble(self) -> str:
        if self._from == '':
            raise Exception('unknown table')
        if self._function == 'TRUNCATE':
            return f"TRUNCATE {self._from}"
        sql = ''
        # if self._function == 'INSERT':
        #     $columns = array_keys($this->_params['columns']);
        #     $values = $this->quote(array_values($this->_params['columns']));
        #     $sql = "INSERT INTO {$this->_params['from']}";
        #     $sql .= ' (`' . implode('`, `', $columns) . '`)';
        #     $sql .= " VALUES ({$values})";
        if self._function == 'SELECT':
            sql = 'SELECT '
            if len(self._columns) == 0:
                sql += '*'
            else:
                sql += ', '.join(self._columns)
            sql += f" FROM {self._from}"
        # if self._function == 'UPDATE':
        #     $sql = "UPDATE {$this->_params['from']} SET";
        #     foreach ($this->_params['columns'] as $key => $value) {
        #         $sql .= " `{$key}` = {$this->quote($value)},";
        #     }
        #     $sql = rtrim($sql, ',');
        if self._function == 'DELETE':
            sql = f"DELETE FROM {self._from}"
        if len(self._joins) > 0:
            sql += ' ' + ' '.join(self._joins)
        if len(self._wheres) == 0:
            if self._function != 'SELECT':
                raise Exception('unknown where expression')
        else:
            sql += ' WHERE ' + ' AND '.join(self._wheres)
        if self._group:
            sql += f" GROUP BY {self._group}"
        if len(self._having) > 0:
            sql += ' HAVING ' + ' AND '.join(self._having)
        if self._order:
            sql += f" ORDER BY {self._order}"
        if self._limit > 0:
            sql += f" LIMIT {self._limit}"
        if self._offset > 0:
            sql += f" OFFSET {self._offset}"
        return sql